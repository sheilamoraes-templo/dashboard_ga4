# src/report_catalog.py
# Catálogo declarativo: qual CSV baixar e como tratar
# - Cada chave em REPORTS vira um CSV/Parquet em data/<filename>.{csv,parquet}
# - Campos especiais:
#     compare_periods: True  -> baixa período atual e anterior e devolve lado a lado (cur, prev, diff, pct)
#     postprocess:   "..."   -> normalizações específicas (ex.: daily, pages, devices, weekday_heatmap etc.)
#     special:       "video" -> usa rotina de vídeo (start/progress/complete) com título/% (ou customEvent)
#     filter_in:     {"dimension": "country", "values": ["Brazil","Brasil"]}
#     filter_contains: {"dimension": "pagePath", "contains": "/classes"}   # "contains" case-insensitive

from typing import Dict, Any

REPORTS: Dict[str, Dict[str, Any]] = {

    # ---------- KPIs / Séries ----------
    # Série diária base do dashboard (users/sessions/pageviews)
    "kpis_daily": {
        "filename": "kpis_daily",
        "dimensions": ["date"],
        "metrics": ["totalUsers", "sessions", "screenPageViews"],
        "postprocess": "daily"
    },

    # Totais comparados (último período X período anterior) — para cards com Δ
    "users_compare": {
        "filename": "users_compare",
        "dimensions": ["date"],
        "metrics": ["totalUsers"],
        "postprocess": "compare_sum",
        "compare_periods": True
    },
    "sessions_compare": {
        "filename": "sessions_compare",
        "dimensions": ["date"],
        "metrics": ["sessions"],
        "postprocess": "compare_sum",
        "compare_periods": True
    },
    "pageviews_compare": {
        "filename": "pageviews_compare",
        "dimensions": ["date"],
        "metrics": ["screenPageViews"],
        "postprocess": "compare_sum",
        "compare_periods": True
    },
    "avg_session_duration_compare": {
        "filename": "avg_session_duration_compare",
        "dimensions": ["date"],
        "metrics": ["averageSessionDuration"],
        "postprocess": "compare_avg_duration",
        "compare_periods": True
    },

    # ---------- Páginas / "classes" ----------
    # Páginas mais acessadas (ranking atual)
    "pages_top": {
        "filename": "pages_top",
        "dimensions": ["pagePath"],
        "metrics": ["screenPageViews"],
        "order_by_metric": "screenPageViews",
        "limit": 100000,
        "postprocess": "pages"
    },

    # Páginas mais acessadas — COMPARANDO períodos lado a lado (links)
    "pages_top_compare": {
        "filename": "pages_top_compare",
        "dimensions": ["pagePath"],
        "metrics": ["screenPageViews"],
        "order_by_metric": "screenPageViews",
        "limit": 100000,
        "postprocess": "pages_compare",
        "compare_periods": True
    },

    # "classes": se quiser focar numa seção (ex.: /classes)
    "classes_pages_compare": {
        "filename": "classes_pages_compare",
        "dimensions": ["pagePath"],
        "metrics": ["screenPageViews"],
        "order_by_metric": "screenPageViews",
        "limit": 100000,
        "postprocess": "pages_compare",
        "compare_periods": True,
        "filter_contains": {"dimension": "pagePath", "contains": "/classes"}
    },

    # ---------- Primeiro acesso ----------
    # Quantidade por fonte/meio/campanha — ranking atual
    "first_user_acquisition": {
        "filename": "first_user_acquisition",
        "dimensions": ["firstUserSource", "firstUserMedium", "firstUserCampaignName"],
        "metrics": ["totalUsers"],
        "order_by_metric": "totalUsers",
        "limit": 100000,
        "postprocess": "first_user"
    },

    # ---------- Dias com mais usuários ----------
    # "Dias com mais usuários" (top N ordenado)
    "days_with_most_users": {
        "filename": "days_with_most_users",
        "dimensions": ["date"],
        "metrics": ["totalUsers"],
        "postprocess": "days_top"   # ordena e devolve top N (configuramos no postprocess)
    },

    # ---------- Vídeo ----------
    # Eventos de vídeo, com título e percent quando possível
    "video_events": {
        "filename": "video_events",
        "special": "video"  # usa a rotina especial do cliente (start/progress/complete)
    },
    "video_start": {
        "filename": "video_start",
        "special": "video_specific",
        "event_names": ["video_start"]
    },
    "video_progress": {
        "filename": "video_progress",
        "special": "video_specific",
        "event_names": ["video_progress"]
    },
    "video_complete": {
        "filename": "video_complete",
        "special": "video_specific",
        "event_names": ["video_complete"]
    },

    # ---------- Dias da semana ----------
    # "Dias da semana com mais acessos, ao longo das últimas semanas"
    # Gera uma tabela (semana × dia_da_semana) para heatmap
    "weekday_heatmap": {
        "filename": "weekday_heatmap",
        "dimensions": ["date"],  # pegamos a diária e calculamos o dia da semana no postprocess
        "metrics": ["totalUsers"],
        "postprocess": "weekday_heatmap"
    },

    # ---------- Dispositivos (opcional) ----------
    "devices": {
        "filename": "devices",
        "dimensions": ["deviceCategory"],
        "metrics": ["totalUsers"],
        "postprocess": "devices"
    },
}
