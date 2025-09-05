"""
Configuração do Pipeline GA4
Arquivo de configuração para facilitar o uso do pipeline
"""

# Configurações do Pipeline GA4
PIPELINE_CONFIG = {
    # Períodos padrão
    "default_days": 30,
    "quick_days": 7,
    "max_days": 90,
    
    # Limites de dados
    "top_pages_limit": 50,
    "video_events_limit": 100,
    
    # Configurações de cache
    "cache_ttl_minutes": 30,
    
    # Arquivos de saída
    "output_files": {
        "kpis_daily": "kpis_daily.csv",
        "pages_top": "pages_top.csv", 
        "devices": "devices.csv",
        "first_user_acquisition": "first_user_acquisition.csv",
        "video_events": "video_events.csv",
        "weekly_comparison": "weekly_comparison.csv",
        "days_with_most_users": "days_with_most_users.csv"
    },
    
    # Métricas específicas solicitadas
    "required_metrics": [
        "users",
        "sessions", 
        "screenPageViews",
        "averageSessionDuration",
        "bounceRate"
    ],
    
    # Eventos de vídeo específicos
    "video_events": [
        "video_start",
        "video_progress", 
        "video_complete"
    ],
    
    # Dimensões para análise temporal
    "temporal_dimensions": [
        "date",
        "yearWeek",
        "dayOfWeek"
    ],
    
    # Dimensões para análise de aquisição
    "acquisition_dimensions": [
        "firstUserSource",
        "firstUserMedium",
        "firstUserCampaign"
    ]
}

# Comandos de execução
EXECUTION_COMMANDS = {
    "pipeline_padrao": "python ga4_pipeline.py --days 30",
    "pipeline_rapido": "python ga4_pipeline.py --quick", 
    "pipeline_completo": "python ga4_pipeline.py --full --days 30",
    "download_direto": "python download_ga4_data.py",
    "menu_interativo": "python run_pipeline.py",
    "dashboard": "streamlit run streamlit_dashboard.py"
}

# Instruções de uso
USAGE_INSTRUCTIONS = """
🚀 PIPELINE GA4 - INSTRUÇÕES DE USO

📋 COMANDOS DISPONÍVEIS:

1. Pipeline Padrão (30 dias):
   python ga4_pipeline.py --days 30

2. Pipeline Rápido (7 dias):
   python ga4_pipeline.py --quick

3. Pipeline Completo (30 dias):
   python ga4_pipeline.py --full --days 30

4. Download Direto:
   python download_ga4_data.py

5. Menu Interativo:
   python run_pipeline.py

6. Executar Dashboard:
   streamlit run streamlit_dashboard.py

📊 DADOS BAIXADOS:

✅ Métricas Principais:
   - Usuários, Sessões, Pageviews
   - Duração média de sessão
   - Taxa de rejeição

✅ Top Páginas e Links:
   - Páginas mais acessadas
   - Links mais clicados
   - Análise de tráfego por página

✅ Breakdown por Dispositivo:
   - Desktop, Mobile, Tablet
   - Distribuição de usuários

✅ Primeiros Acessos:
   - Source/Medium de aquisição
   - Novos usuários por fonte
   - Análise de canais

✅ Eventos de Vídeo:
   - video_start
   - video_progress
   - video_complete

✅ Análise Temporal:
   - Dias com mais usuários
   - Comparação semanal
   - Tendências temporais

📁 ARQUIVOS GERADOS:
   - kpis_daily.csv
   - pages_top.csv
   - devices.csv
   - first_user_acquisition.csv
   - video_events.csv
   - weekly_comparison.csv
   - days_with_most_users.csv

🔧 PRÉ-REQUISITOS:
   - Credenciais GA4 em 'credenciais_google_ga4.json'
   - Propriedade GA4 configurada
   - Python 3.8+ com dependências instaladas

🌐 APÓS O DOWNLOAD:
   Execute: streamlit run streamlit_dashboard.py
   Acesse: http://localhost:8501
"""
