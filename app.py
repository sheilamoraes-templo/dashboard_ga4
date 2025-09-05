from flask import Flask, render_template, jsonify, request, send_from_directory, Response
from flask_cors import CORS
import plotly.graph_objs as go
import plotly.utils
import json
from datetime import datetime, timedelta
import pandas as pd
import os
import io
import zipfile

from src.report_catalog import REPORTS
from src.ga4_client import GA4Client
from src.ai_analyzer import AIAnalyzer
from src.email_sender import EmailSender
from src.slack_client import SlackClient
from src.automation import AutomationManager
from src.agent_llm import ask_llm
from config.settings import FLASK_SECRET_KEY, FLASK_DEBUG, FLASK_HOST, FLASK_PORT

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
CORS(app)

# Configurar diretório de dados
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _save_csv(df: pd.DataFrame, base: str):
    """Salva DataFrame como CSV (e Parquet se disponível)"""
    if df is None or df.empty:
        return None
    csv_path = os.path.join(DATA_DIR, f"{base}.csv")
    
    try:
        df.to_csv(csv_path, index=False)
        print(f"✅ Arquivo CSV salvo: {csv_path}")
        
        # Tentar salvar Parquet se pyarrow estiver disponível
        try:
            pq_path = os.path.join(DATA_DIR, f"{base}.parquet")
            df.to_parquet(pq_path, index=False)
            print(f"✅ Arquivo Parquet salvo: {pq_path}")
        except ImportError:
            print(f"⚠️ Parquet não disponível (pyarrow não instalado)")
        
        return csv_path
    except Exception as e:
        print(f"❌ Erro ao salvar {base}: {e}")
        return None

# Inicializar componentes (lazy loading)
ga4_client = None
ai_analyzer = None
email_sender = None
slack_client = None
automation_manager = None

def get_ga4_client():
    global ga4_client
    if ga4_client is None:
        ga4_client = GA4Client()
    return ga4_client

def get_ai_analyzer():
    global ai_analyzer
    if ai_analyzer is None:
        ai_analyzer = AIAnalyzer()
    return ai_analyzer

def get_email_sender():
    global email_sender
    if email_sender is None:
        email_sender = EmailSender()
    return email_sender

def get_slack_client():
    global slack_client
    if slack_client is None:
        slack_client = SlackClient()
    return slack_client

def get_automation_manager():
    global automation_manager
    if automation_manager is None:
        automation_manager = AutomationManager()
    return automation_manager

@app.route('/')
def dashboard():
    """Página principal do dashboard"""
    return render_template('dashboard_analytics.html')

@app.route('/test')
def test_simple():
    """Teste simples para debug"""
    return render_template('test_simple.html')

@app.route('/debug')
def dashboard_debug():
    """Dashboard de debug para identificar problemas"""
    return render_template('dashboard_debug.html')

@app.route('/dashboard-old')
def dashboard_old():
    """Dashboard original (mantido para compatibilidade)"""
    return render_template('dashboard.html')

@app.route('/api/metrics')
def get_metrics():
    """API para obter métricas básicas"""
    try:
        days = request.args.get('days', 30, type=int)
        metrics = get_ga4_client().get_basic_metrics(days=days)
        
        if metrics:
            return jsonify({
                'success': True,
                'data': metrics,
                'period': f'Últimos {days} dias'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Não foi possível obter métricas'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/daily-chart')
def get_daily_chart():
    """API para obter dados do gráfico diário"""
    try:
        days = request.args.get('days', 30, type=int)
        daily_data = get_ga4_client().get_daily_metrics(days=days)
        
        if daily_data is not None and not daily_data.empty:
            # PATCH A: Garantir data ISO para o JavaScript
            return daily_data.to_json(orient='records', date_format='iso'), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({
                'success': False,
                'error': 'Não foi possível obter dados diários'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/top-pages')
def get_top_pages():
    """API para obter páginas mais visitadas"""
    try:
        days = request.args.get('days', 30, type=int)
        limit = request.args.get('limit', 10, type=int)
        top_pages = get_ga4_client().get_top_pages(days=days, limit=limit)
        
        if top_pages is not None and not top_pages.empty:
            # PATCH B: Garantir chaves padronizadas
            if 'pagePath' in top_pages.columns:
                top_pages = top_pages.rename(columns={'pagePath': 'page'})
            if 'screenPageViews' in top_pages.columns:
                top_pages = top_pages.rename(columns={'screenPageViews': 'pageviews'})
            
            return jsonify({
                'success': True,
                'data': top_pages.to_dict('records')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Não foi possível obter dados das páginas'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/device-breakdown')
def get_device_breakdown():
    """API para obter breakdown por dispositivo"""
    try:
        days = request.args.get('days', 30, type=int)
        device_data = get_ga4_client().get_device_breakdown(days=days)
        
        if device_data is not None and not device_data.empty:
            # PATCH C: Converter strings para números
            if 'users' in device_data.columns:
                device_data['users'] = pd.to_numeric(device_data['users'], errors='coerce').fillna(0)
            if 'deviceCategory' in device_data.columns:
                device_data = device_data.rename(columns={'deviceCategory': 'device'})
            
            return jsonify({
                'success': True,
                'data': device_data.to_dict('records')
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Não foi possível obter dados de dispositivos'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/ai-insights')
def get_ai_insights():
    """API para obter insights de IA"""
    try:
        days = request.args.get('days', 30, type=int)
        metrics = get_ga4_client().get_basic_metrics(days=days)
        
        if metrics:
            insights = get_ai_analyzer().analyze_metrics(metrics)
            return jsonify({
                'success': True,
                'insights': insights
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Não foi possível obter métricas para análise'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/send-test-email')
def send_test_email():
    """API para enviar email de teste"""
    try:
        success = get_email_sender().test_email_config()
        return jsonify({
            'success': success,
            'message': 'Email de teste enviado' if success else 'Falha ao enviar email'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/test-slack')
def test_slack():
    """API para testar conexão com Slack"""
    try:
        success = get_slack_client().test_connection()
        return jsonify({
            'success': success,
            'message': 'Conexão Slack testada com sucesso' if success else 'Falha na conexão Slack'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/send-slack-report')
def send_slack_report():
    """API para enviar relatório manual via Slack"""
    try:
        report_type = request.args.get('type', 'daily')
        days = 1 if report_type == 'daily' else (7 if report_type == 'weekly' else 30)
        
        # Obter dados
        metrics = get_ga4_client().get_basic_metrics(days=days)
        daily_data = get_ga4_client().get_daily_metrics(days=days)
        top_pages = get_ga4_client().get_top_pages(days=days, limit=10)
        insights = get_ai_analyzer().analyze_metrics(metrics)
        
        if report_type == 'daily':
            success = get_slack_client().send_daily_report(metrics, daily_data, top_pages, insights)
        elif report_type == 'weekly':
            success = get_slack_client().send_weekly_report(metrics, daily_data, top_pages, insights)
        elif report_type == 'monthly':
            success = get_slack_client().send_monthly_report(metrics, daily_data, top_pages, insights)
        else:
            return jsonify({
                'success': False,
                'error': 'Tipo de relatório inválido'
            })
        
        return jsonify({
            'success': success,
            'message': f'Relatório {report_type} enviado via Slack' if success else f'Falha ao enviar relatório {report_type}'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/send-report')
def send_manual_report():
    """API para enviar relatório manual"""
    try:
        report_type = request.args.get('type', 'daily')
        get_automation_manager().send_manual_report(report_type)
        return jsonify({
            'success': True,
            'message': f'Relatório {report_type} enviado'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/automation/start')
def start_automation():
    """API para iniciar automação"""
    try:
        get_automation_manager().start_scheduler()
        return jsonify({
            'success': True,
            'message': 'Automação iniciada'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/automation/stop')
def stop_automation():
    """API para parar automação"""
    try:
        get_automation_manager().stop_scheduler()
        return jsonify({
            'success': True,
            'message': 'Automação parada'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/automation/status')
def get_automation_status():
    """API para obter status da automação"""
    try:
        status = get_automation_manager().get_scheduler_status()
        return jsonify({
            'success': True,
            'status': status
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/first-user-acquisition')
def api_first_user_acquisition():
    """API para obter dados de aquisição de primeiro acesso"""
    try:
        days = int(request.args.get('days', 30))
        df = get_ga4_client().first_user_acquisition(days)
        
        # PATCH D: Logs úteis
        print(f"[first-user-acquisition] rows={len(df)} days={days}")
        
        return df.to_json(orient='records'), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/video-events')
def api_video_events():
    """API para obter eventos de vídeo"""
    try:
        days = int(request.args.get('days', 30))
        df = get_ga4_client().video_events(days)
        
        # PATCH D: Logs úteis
        print(f"[video-events] rows={len(df)} days={days}")
        
        return df.to_json(orient='records', date_format='iso'), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh-data', methods=['POST'])
def api_refresh_data():
    """Busca via GA4 API e grava CSVs/Parquet usando catálogo de relatórios."""
    try:
        days = int(request.args.get('days', 30))
        reports_param = request.args.get('reports', '')
        
        # Se não especificado, usa relatórios padrão do dashboard
        if not reports_param:
            keys = ['kpis_daily', 'pages_top', 'first_user_acquisition', 'video_events', 'devices']
        else:
            keys = [k.strip() for k in reports_param.split(',')]
        
        print(f"🔄 Iniciando refresh de dados para {days} dias...")
        print(f"📋 Relatórios solicitados: {keys}")
        
        ga4_client = get_ga4_client()
        files_generated = []
        
        for key in keys:
            if key not in REPORTS:
                print(f"⚠️ Relatório '{key}' não encontrado no catálogo")
                continue
                
            spec = REPORTS[key]
            fname = spec["filename"]
            print(f"📊 Processando: {key} -> {fname}")
            
            try:
                if spec.get("special") == "video":
                    df = ga4_client.video_events(days)
                    
                elif spec.get("special") == "video_specific":
                    df = ga4_client.video_events_specific(days, spec.get("event_names", []))
                    
                elif spec.get("compare_periods"):
                    # Baixa período atual e anterior, depois junta
                    cur, prev = ga4_client.run_compare_periods(
                        days=days,
                        dimensions=spec["dimensions"],
                        metrics=spec["metrics"],
                        filter_in=spec.get("filter_in"),
                        filter_contains=spec.get("filter_contains"),
                        order_by_metric=spec.get("order_by_metric"),
                        limit=spec.get("limit", 100000),
                    )
                    
                    # Pós-process de cada período
                    if spec.get("postprocess") == "pages_compare":
                        cur_pp = ga4_client.postprocess("pages", cur.copy() if cur is not None else cur)
                        prev_pp = ga4_client.postprocess("pages", prev.copy() if prev is not None else prev)
                        
                        # Join por page
                        df = pd.merge(
                            cur_pp.rename(columns={"pageviews": "pageviews_cur"}),
                            prev_pp.rename(columns={"pageviews": "pageviews_prev"}),
                            how="outer", on="page"
                        ).fillna(0)
                        df["diff"] = df["pageviews_cur"] - df["pageviews_prev"]
                        df["pct"] = df.apply(lambda r: (r["diff"] / r["pageviews_prev"] * 100.0) if r["pageviews_prev"] else None, axis=1)
                        df = df.sort_values("pageviews_cur", ascending=False)
                        
                    elif spec.get("postprocess") == "compare_sum":
                        # Soma métrica no período cur x prev
                        m = spec["metrics"][0]
                        cur_sum = pd.to_numeric(cur[m], errors="coerce").fillna(0).sum() if (cur is not None and m in cur) else 0
                        prev_sum = pd.to_numeric(prev[m], errors="coerce").fillna(0).sum() if (prev is not None and m in prev) else 0
                        diff = cur_sum - prev_sum
                        pct = (diff / prev_sum * 100.0) if prev_sum else None
                        df = pd.DataFrame([{"metric": m, "cur": cur_sum, "prev": prev_sum, "diff": diff, "pct": pct}])
                        
                    elif spec.get("postprocess") == "compare_avg_duration":
                        m = "averageSessionDuration"
                        # Média ponderada por sessões em cada período
                        def avg_dur(frame):
                            if frame is None or frame.empty: return 0.0
                            if "sessions" in frame.columns and frame["sessions"].astype(float).sum() > 0:
                                return float((pd.to_numeric(frame[m], errors="coerce").fillna(0) * pd.to_numeric(frame["sessions"], errors="coerce").fillna(0)).sum() /
                                             pd.to_numeric(frame["sessions"], errors="coerce").fillna(0).sum())
                            return float(pd.to_numeric(frame[m], errors="coerce").fillna(0).mean())
                        cur_avg, prev_avg = avg_dur(cur), avg_dur(prev)
                        diff = cur_avg - prev_avg
                        pct = (diff / prev_avg * 100.0) if prev_avg else None
                        df = pd.DataFrame([{"metric": m, "cur": round(cur_avg,2), "prev": round(prev_avg,2), "diff": round(diff,2), "pct": pct}])
                        
                    else:
                        # Fallback: devolve dois blocos com tag period
                        cur["period"] = "current"
                        prev["period"] = "previous"
                        df = pd.concat([cur, prev], ignore_index=True)
                        
                else:
                    # Relatório simples (um período)
                    df = ga4_client.run_generic(
                        days=days,
                        dimensions=spec["dimensions"],
                        metrics=spec["metrics"],
                        filter_in=spec.get("filter_in"),
                        filter_contains=spec.get("filter_contains"),
                        order_by_metric=spec.get("order_by_metric"),
                        limit=spec.get("limit", 100000),
                    )
                    df = ga4_client.postprocess(spec.get("postprocess", ""), df)
                
                # Salva o arquivo
                path = _save_csv(df, fname)
                if path:
                    files_generated.append(os.path.basename(path))
                    print(f"✅ {fname}.csv gerado com sucesso")
                else:
                    print(f"⚠️ Falha ao gerar {fname}.csv")
                    
            except Exception as e:
                print(f"❌ Erro ao processar {key}: {e}")
                continue
        
        ts = datetime.now().isoformat(timespec="seconds")
        print(f"✅ Refresh concluído! {len(files_generated)} arquivos gerados.")
        
        return jsonify({
            "success": True,
            "files": files_generated,
            "refreshed_at": ts,
            "message": f"Dados atualizados com sucesso! {len(files_generated)} arquivos CSV gerados.",
            "reports_processed": keys
        })
        
    except Exception as e:
        print(f"❌ Erro no refresh: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "message": f"Erro ao atualizar dados: {e}"
        }), 500

@app.route('/api/report')
def api_report():
    """
    GET /api/report?name=<report_key>
    Ex.: /api/report?name=pages_top_compare
         /api/report?name=weekday_heatmap
         /api/report?name=users_compare
    Lê data/<filename>.csv do catálogo e devolve JSON.
    """
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "missing ?name="}), 400

    # mapeia a key do catálogo para o filename salvo
    try:
        from src.report_catalog import REPORTS
        if name not in REPORTS:
            return jsonify({"error": f"unknown report '{name}'"}), 404
        filename = REPORTS[name]["filename"] + ".csv"
    except Exception:
        # fallback: assume que 'name' já é filename sem extensão
        filename = f"{name}.csv"

    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return jsonify({"error": f"file not found: {filename}. Gere com /api/refresh-data primeiro."}), 404

    # lê CSV e retorna JSON
    df = pd.read_csv(path)
    # normalização simples
    if "date" in df.columns:
        # tenta converter pra ISO; se vier iso já, fica igual
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.to_json(orient="records", date_format="iso"), 200, {"Content-Type": "application/json"}

@app.route('/api/reports-catalog')
def api_reports_catalog():
    """Lista todos os relatórios disponíveis no catálogo"""
    try:
        catalog = {}
        for key, spec in REPORTS.items():
            catalog[key] = {
                "filename": spec["filename"],
                "description": spec.get("description", ""),
                "dimensions": spec.get("dimensions", []),
                "metrics": spec.get("metrics", []),
                "compare_periods": spec.get("compare_periods", False),
                "special": spec.get("special", ""),
                "postprocess": spec.get("postprocess", "")
            }
        
        return jsonify({
            "success": True,
            "catalog": catalog,
            "total_reports": len(REPORTS)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    """Download de arquivo da pasta data/"""
    try:
        return send_from_directory(DATA_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Arquivo não encontrado: {e}"}), 404

@app.route('/api/zip-data')
def api_zip_data():
    """Gera ZIP com todos os CSVs"""
    try:
        mem = io.BytesIO()
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
        
        if not csv_files:
            return jsonify({"error": "Nenhum arquivo CSV encontrado"}), 404
        
        with zipfile.ZipFile(mem, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
            for filename in csv_files:
                file_path = os.path.join(DATA_DIR, filename)
                zf.write(file_path, arcname=filename)
        
        mem.seek(0)
        
        return Response(
            mem.getvalue(),
            mimetype='application/zip',
            headers={'Content-Disposition': 'attachment; filename=ga4_exports.zip'}
        )
        
    except Exception as e:
        return jsonify({"error": f"Erro ao gerar ZIP: {e}"}), 500

@app.route('/api/debug')
def api_debug():
    """API de debug para diagnóstico completo"""
    out = {}
    try:
        import pandas as pd
        ga4_client = get_ga4_client()
        
        # Testar cada método
        d = ga4_client.get_daily_metrics(30)
        p = ga4_client.get_top_pages(30, 10)
        dv = ga4_client.get_device_breakdown(30)
        ac = ga4_client.first_user_acquisition(30)
        ve = ga4_client.video_events(30)
        
        # Contar linhas
        out["daily_rows"] = 0 if d is None else len(d)
        out["pages_rows"] = 0 if p is None else len(p)
        out["device_rows"] = 0 if dv is None else len(dv)
        out["acq_rows"] = 0 if ac is None else len(ac)
        out["video_rows"] = 0 if ve is None else len(ve)
        
        # Mostrar primeiras linhas
        out["daily_head"] = [] if d is None else d.head(3).to_dict(orient='records')
        out["pages_head"] = [] if p is None else p.head(3).to_dict(orient='records')
        out["device_head"] = [] if dv is None else dv.head(3).to_dict(orient='records')
        out["acq_head"] = [] if ac is None else ac.head(3).to_dict(orient='records')
        out["video_head"] = [] if ve is None else ve.head(3).to_dict(orient='records')
        
        # Informações sobre colunas
        out["daily_columns"] = list(d.columns) if d is not None else []
        out["pages_columns"] = list(p.columns) if p is not None else []
        out["device_columns"] = list(dv.columns) if dv is not None else []
        out["acq_columns"] = list(ac.columns) if ac is not None else []
        out["video_columns"] = list(ve.columns) if ve is not None else []
        
    except Exception as e:
        out["error"] = str(e)
    
    return jsonify(out)

@app.route('/test-csv')
def test_csv():
    """Página de teste para funcionalidade CSV"""
    return render_template('test_csv.html')

@app.route('/api/test-connection')
def test_connection():
    """API para testar conexão com GA4"""
    try:
        success = get_ga4_client().test_connection()
        return jsonify({
            'success': success,
            'message': 'Conexão testada com sucesso' if success else 'Falha na conexão'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/agent-llm', methods=['POST'])
def api_agent_llm():
    """API para Agent com LLM via OpenRouter"""
    try:
        payload = request.get_json(silent=True) or {}
        q = (payload.get("q") or "").strip()
        if not q:
            return jsonify({"ok": False, "error": "Pergunta vazia."}), 400
        
        resp = ask_llm(q)
        return jsonify(resp), (200 if resp.get("ok") else 500)
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": f"Erro interno do Agent: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Dashboard GA4...")
    print(f"📊 Acesse: http://{FLASK_HOST}:{FLASK_PORT}")
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)
