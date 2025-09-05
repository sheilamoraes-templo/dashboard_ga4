import os
from pathlib import Path

# Configurações do GA4
GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "476192590")  # Classplay - propriedade correta
GA4_CREDENTIALS_PATH = os.getenv("GA4_CREDENTIALS_PATH", "credenciais_google_ga4.json")

# Configurações do Flask
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dashboard_ga4_secret_key_2024")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))

# Configurações de Email (mantido para compatibilidade)
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "seu_email@gmail.com")  # Configure seu email
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "sua_senha_app")  # Configure sua senha de app

# Configurações do Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "SEU_BOT_TOKEN_AQUI")  # Configure seu Bot Token do Slack
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL", "#analytics")  # Canal onde enviar as atualizações
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL", "SEU_WEBHOOK_URL_AQUI")  # Webhook URL (alternativa)

# Configurações de IA (OpenRouter)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "SUA_CHAVE_OPENROUTER_AQUI")  # Configure sua chave OpenRouter
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Configurações do Google Gemini (fallback)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "sua_chave_gemini_aqui")  # Configure sua chave do Google AI Studio

# Configurações de Relatórios
REPORT_FREQUENCY = "daily"  # daily, weekly, monthly
REPORT_RECIPIENTS = ["destinatario@email.com"]  # Lista de emails (mantido para compatibilidade)
SLACK_REPORTS_ENABLED = True  # Habilitar relatórios no Slack

# Configurações de Cache
CACHE_DURATION = 3600  # 1 hora em segundos
DATA_CACHE_PATH = "data/cache/"

# Métricas padrão para extrair
DEFAULT_METRICS = [
    "totalUsers",
    "sessions",
    "screenPageViews",
    "averageSessionDuration",
    "bounceRate"
]

DEFAULT_DIMENSIONS = [
    "date",
    "pageTitle",
    "pagePath",
    "deviceCategory",
    "country"
]
