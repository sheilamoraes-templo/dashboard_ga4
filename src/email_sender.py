import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config.settings import (
    EMAIL_SMTP_SERVER, 
    EMAIL_SMTP_PORT, 
    EMAIL_SENDER, 
    EMAIL_PASSWORD,
    REPORT_RECIPIENTS
)

class EmailSender:
    def __init__(self):
        """Inicializa o sender de email"""
        self.smtp_server = EMAIL_SMTP_SERVER
        self.smtp_port = EMAIL_SMTP_PORT
        self.sender_email = EMAIL_SENDER
        self.sender_password = EMAIL_PASSWORD
        
    def send_report_email(self, subject, html_content, recipients=None):
        """Envia email com relatório"""
        try:
            if not recipients:
                recipients = REPORT_RECIPIENTS
                
            if not self.sender_email or self.sender_email == "seu_email@gmail.com":
                print("⚠️ Configuração de email não definida. Configure EMAIL_SENDER e EMAIL_PASSWORD em config/settings.py")
                return False
            
            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(recipients)
            
            # Adicionar conteúdo HTML
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                
            print(f"✅ Email enviado com sucesso para {len(recipients)} destinatário(s)")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar email: {e}")
            return False
    
    def send_daily_report(self, metrics_data, daily_data=None, top_pages=None):
        """Envia relatório diário"""
        from src.ai_analyzer import AIAnalyzer
        
        try:
            # Gerar conteúdo com IA
            ai_analyzer = AIAnalyzer()
            html_content = ai_analyzer.generate_email_content(metrics_data, daily_data, top_pages)
            
            # Enviar email
            subject = f"📊 Relatório GA4 Diário - {datetime.now().strftime('%d/%m/%Y')}"
            return self.send_report_email(subject, html_content)
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório diário: {e}")
            return False
    
    def send_weekly_report(self, metrics_data, daily_data=None, top_pages=None):
        """Envia relatório semanal"""
        from src.ai_analyzer import AIAnalyzer
        
        try:
            # Gerar conteúdo com IA
            ai_analyzer = AIAnalyzer()
            html_content = ai_analyzer.generate_email_content(metrics_data, daily_data, top_pages)
            
            # Enviar email
            subject = f"📊 Relatório GA4 Semanal - {datetime.now().strftime('%d/%m/%Y')}"
            return self.send_report_email(subject, html_content)
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório semanal: {e}")
            return False
    
    def test_email_config(self):
        """Testa a configuração de email"""
        try:
            if not self.sender_email or self.sender_email == "seu_email@gmail.com":
                print("❌ Email não configurado")
                return False
                
            # Teste simples
            test_content = """
            <html>
            <body>
                <h2>🧪 Teste de Configuração de Email</h2>
                <p>Se você recebeu este email, a configuração está funcionando corretamente!</p>
                <p>Data do teste: """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
            </body>
            </html>
            """
            
            subject = "🧪 Teste - Dashboard GA4"
            return self.send_report_email(subject, test_content)
            
        except Exception as e:
            print(f"❌ Erro no teste de email: {e}")
            return False
