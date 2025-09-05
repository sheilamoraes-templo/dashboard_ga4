# src/agent_llm.py
import os, json, re, time, pandas as pd
from typing import Any, Dict, List, Tuple

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Ordem de preferência de modelos (ajuste se quiser)
PREFERRED_MODELS = [
    "google/gemini-2.5-flash",
    "google/gemini-2.0-pro-exp",
    "anthropic/claude-3.5-sonnet",
]

# Limite padrão de linhas que retornamos para o front (tabela)
ROW_LIMIT = 300

# ===== Helpers =====

def _catalog_keys() -> List[str]:
    from src.report_catalog import REPORTS
    return list(REPORTS.keys())

def _catalog_filenames() -> Dict[str, str]:
    from src.report_catalog import REPORTS
    return {k: v["filename"] for k, v in REPORTS.items()}

def _load_csv_by_key(key: str) -> pd.DataFrame:
    from src.report_catalog import REPORTS
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    filename = REPORTS[key]["filename"] + ".csv"
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {filename}. Gere com /api/refresh-data.")
    df = pd.read_csv(path)
    # normalizações leves
    if "date" in df.columns:
        try: df["date"] = pd.to_datetime(df["date"], errors="coerce")
        except Exception: pass
    return df

def _choose_model(preferred=PREFERRED_MODELS) -> str:
    # aqui poderíamos consultar /models da OpenRouter; para simplicidade, só retornamos o primeiro da lista
    return preferred[0]

def _strict_json(s: str) -> Dict[str, Any]:
    # extrai primeiro bloco JSON da resposta do LLM
    # aceita markdown code fences ou texto cru
    m = re.search(r"\{.*\}", s, flags=re.DOTALL)
    if not m:
        raise ValueError("LLM não retornou JSON.")
    text = m.group(0)
    return json.loads(text)

def _call_openrouter(model: str, system_prompt: str, user_prompt: str, timeout: int = 60) -> str:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("Defina OPENROUTER_API_KEY no ambiente.")
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # (opcional) identify your app/site: https://openrouter.ai/docs#headers
        "HTTP-Referer": "https://templo-dashboard.local",
        "X-Title": "Templo GA4 Dashboard Agent",
    }
    payload = {
        "model": model,
        "temperature": 0.0,
        "response_format": { "type": "json_object" },  # força JSON
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    import requests
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=timeout)
    if r.status_code >= 400:
        raise RuntimeError(f"OpenRouter HTTP {r.status_code}: {r.text[:2000]}")
    data = r.json()
    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        raise RuntimeError(f"Resposta inesperada do OpenRouter: {data}")

# ===== Core Agent =====

SYSTEM_PROMPT = """Você é um orquestrador de relatórios. Recebe uma pergunta de negócio e responde SOMENTE com JSON no formato abaixo (sem texto extra):

{
  "reports": ["<uma ou mais chaves de relatório>"],
  "filters": {
    "contains": {"dimension": "pagePath", "value": "/classes"},
    "in": {"dimension": "country", "values": ["Brazil", "Brasil"]}
  },
  "days": 30,
  "chart": "table|bar|barh|lines|heatmap|combo|delta",
  "limit": 50,
  "notes": "breve justificativa do plano"
}

REGRAS IMPORTANTES:
- Use APENAS chaves de relatório desta lista (case-sensitive): {CATALOG}
- Se a pergunta falar em "comparar períodos", prefira *reports* com sufixo *_compare* quando existir.
- Se a pergunta mencionar "classes" (ou seção específica), adicione filters.contains em pagePath.
- Se não souber, use "kpis_daily" e "chart":"lines".
- Não invente métricas. Não coloque comentários fora do JSON.
"""

def build_user_prompt(question: str) -> str:
    return f"Pergunta: {question}\nConsidere que os CSVs já existem e que você só precisa planejar quais relatórios ler."

def plan(question: str, model: str | None = None) -> Dict[str, Any]:
    model = model or _choose_model()
    system = SYSTEM_PROMPT.replace("{CATALOG}", ", ".join(_catalog_keys()))
    out = _call_openrouter(model, system, build_user_prompt(question))
    plan_json = _strict_json(out)

    # validações mínimas
    reports = plan_json.get("reports") or []
    if not isinstance(reports, list) or not reports:
        reports = ["kpis_daily"]
    # filtra apenas relatórios conhecidos
    allowed = set(_catalog_keys())
    reports = [r for r in reports if r in allowed] or ["kpis_daily"]
    plan_json["reports"] = reports

    # sane default
    if plan_json.get("chart") not in ["table","bar","barh","lines","heatmap","combo","delta"]:
        plan_json["chart"] = "table"

    # limita linhas
    lim = plan_json.get("limit")
    if not isinstance(lim, int) or lim <= 0 or lim > ROW_LIMIT:
        plan_json["limit"] = min(ROW_LIMIT, 100)

    return plan_json

def execute(plan_json: Dict[str, Any]) -> Dict[str, Any]:
    reports: List[str] = plan_json["reports"]
    limit: int = plan_json["limit"]
    chart: str = plan_json["chart"]

    data_out: Dict[str, List[Dict[str, Any]]] = {}
    for key in reports:
        try:
            df = _load_csv_by_key(key)
            # cortes simples no lado do servidor: limit
            if not df.empty:
                data_out[key] = df.head(limit).to_dict(orient="records")
            else:
                data_out[key] = []
        except Exception as e:
            data_out[key] = []
            # anexa o erro para o front opcionalmente
            plan_json.setdefault("_errors", {})[key] = str(e)

    # resumo curto (heurístico e determinístico)
    summary = _summarize(reports, data_out)

    return {
        "ok": True,
        "model": plan_json.get("_model"),
        "plan": plan_json,
        "summary": summary,
        "data": data_out,
        "chart": chart,
    }

def _summarize(reports: List[str], data_out: Dict[str, List[Dict[str, Any]]]) -> str:
    try:
        if "pages_top_compare" in reports and data_out.get("pages_top_compare"):
            rows = data_out["pages_top_compare"][:3]
            items = []
            for r in rows:
                cur = float(r.get("pageviews_cur", 0) or 0)
                prev = float(r.get("pageviews_prev", 0) or 0)
                if prev > 0:
                    pct = (cur - prev) / prev * 100.0
                    items.append(f"{r.get('page', '')} ({pct:+.1f}%)")
                else:
                    items.append(f"{r.get('page', '')} (+{int(cur)})")
            return "Top páginas em alta: " + "; ".join(items)
        if "first_user_acquisition" in reports and data_out.get("first_user_acquisition"):
            rows = data_out["first_user_acquisition"][:3]
            items = [f"{r.get('source','(not set)')}/{r.get('medium','(not set)')} — {int(float(r.get('users',0)))}" for r in rows]
            return "Principais origens (primeiro acesso): " + "; ".join(items)
        if "days_with_most_users" in reports and data_out.get("days_with_most_users"):
            r = data_out["days_with_most_users"][0]
            return f"Dia de pico: {r.get('date','?')} com {int(float(r.get('users',0)))} usuários."
        if any(k.endswith("_compare") for k in reports):
            for k in reports:
                if data_out.get(k):
                    r = data_out[k][0]
                    cur, prev = float(r.get("cur",0)), float(r.get("prev",0))
                    pct = None if prev==0 else (cur-prev)/prev*100.0
                    pct_s = "—" if pct is None else f"{pct:+.1f}%"
                    metric = r.get("metric", k.replace("_compare",""))
                    return f"{metric}: {int(cur)} (Δ {pct_s})."
        if "kpis_daily" in reports and data_out.get("kpis_daily"):
            n = len(data_out["kpis_daily"])
            return f"Série diária carregada ({n} registros)."
    except Exception:
        pass
    return "Plano executado. Dados prontos."

def ask_llm(question: str, preferred_models: List[str] | None = None) -> Dict[str, Any]:
    # tenta rodar com o primeiro modelo preferido; se falhar, tenta os demais
    models = preferred_models or PREFERRED_MODELS
    last_err = None
    for m in models:
        try:
            plan_json = plan(question, model=m)
            plan_json["_model"] = m
            return execute(plan_json)
        except Exception as e:
            last_err = e
            continue
    return {"ok": False, "error": f"Falha no Agent LLM: {last_err}"}
