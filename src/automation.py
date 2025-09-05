from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import logging
from src.ga4_client import GA4Client
from src.email_sender import EmailSender
from src.slack_client import SlackClient
from src.ai_analyzer import AIAnalyzer
from config.settings import REPORT_FREQUENCY, SLACK_REPORTS_ENABLED

class AutomationManager:
    def __init__(self):
        """Inicializa o gerenciador de automação"""
        self.scheduler = BackgroundScheduler()
        self.ga4_client = GA4Client()
        self.email_sender = EmailSender()
        self.slack_client = SlackClient()
        self.ai_analyzer = AIAnalyzer()
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def start_scheduler(self):
        """Inicia o agendador de tarefas"""
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                self.logger.info("✅ Agendador iniciado com sucesso")
                
                # Configurar jobs baseado na frequência
                self._setup_jobs()
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar agendador: {e}")
    
    def stop_scheduler(self):
        """Para o agendador de tarefas"""
        try:
            if self.scheduler.running:
                self.scheduler.shutdown()
                self.logger.info("🛑 Agendador parado")
        except Exception as e:
            self.logger.error(f"❌ Erro ao parar agendador: {e}")
    
    def _setup_jobs(self):
        """Configura os jobs agendados"""
        try:
            # Limpar jobs existentes
            self.scheduler.remove_all_jobs()
            
            # Configurar baseado na frequência
            if REPORT_FREQUENCY == "daily":
                # Relatório diário às 8h
                self.scheduler.add_job(
                    self._send_daily_report,
                    CronTrigger(hour=8, minute=0),
                    id='daily_report',
                    name='Relatório Diário GA4'
                )
                self.logger.info("📅 Relatório diário agendado para 8h")
                
            elif REPORT_FREQUENCY == "weekly":
                # Relatório semanal às 9h de segunda-feira
                self.scheduler.add_job(
                    self._send_weekly_report,
                    CronTrigger(day_of_week='mon', hour=9, minute=0),
                    id='weekly_report',
                    name='Relatório Semanal GA4'
                )
                self.logger.info("📅 Relatório semanal agendado para segunda-feira às 9h")
                
            elif REPORT_FREQUENCY == "monthly":
                # Relatório mensal no primeiro dia do mês às 10h
                self.scheduler.add_job(
                    self._send_monthly_report,
                    CronTrigger(day=1, hour=10, minute=0),
                    id='monthly_report',
                    name='Relatório Mensal GA4'
                )
                self.logger.info("📅 Relatório mensal agendado para o primeiro dia do mês às 10h")
                
        except Exception as e:
            self.logger.error(f"❌ Erro ao configurar jobs: {e}")
    
    def _send_daily_report(self):
        """Envia relatório diário"""
        try:
            self.logger.info("📊 Iniciando relatório diário...")
            
            # Obter dados
            metrics = self.ga4_client.get_basic_metrics(days=1)
            daily_data = self.ga4_client.get_daily_metrics(days=7)  # Últimos 7 dias para contexto
            top_pages = self.ga4_client.get_top_pages(days=1, limit=5)
            
            if metrics:
                # Gerar insights de IA
                insights = self.ai_analyzer.analyze_metrics(metrics)
                
                # Enviar via Slack (prioritário)
                slack_success = False
                if SLACK_REPORTS_ENABLED:
                    slack_success = self.slack_client.send_daily_report(metrics, daily_data, top_pages, insights)
                
                # Fallback para email se Slack falhar
                email_success = False
                if not slack_success:
                    email_success = self.email_sender.send_daily_report(metrics, daily_data, top_pages)
                
                if slack_success:
                    self.logger.info("✅ Relatório diário enviado via Slack com sucesso")
                elif email_success:
                    self.logger.info("✅ Relatório diário enviado via email com sucesso")
                else:
                    self.logger.error("❌ Falha ao enviar relatório diário (Slack e Email)")
            else:
                self.logger.error("❌ Não foi possível obter dados para relatório diário")
                
        except Exception as e:
            self.logger.error(f"❌ Erro no relatório diário: {e}")
    
    def _send_weekly_report(self):
        """Envia relatório semanal"""
        try:
            self.logger.info("📊 Iniciando relatório semanal...")
            
            # Obter dados
            metrics = self.ga4_client.get_basic_metrics(days=7)
            daily_data = self.ga4_client.get_daily_metrics(days=7)
            top_pages = self.ga4_client.get_top_pages(days=7, limit=10)
            
            if metrics:
                # Gerar insights de IA
                insights = self.ai_analyzer.analyze_metrics(metrics)
                
                # Enviar via Slack (prioritário)
                slack_success = False
                if SLACK_REPORTS_ENABLED:
                    slack_success = self.slack_client.send_weekly_report(metrics, daily_data, top_pages, insights)
                
                # Fallback para email se Slack falhar
                email_success = False
                if not slack_success:
                    email_success = self.email_sender.send_weekly_report(metrics, daily_data, top_pages)
                
                if slack_success:
                    self.logger.info("✅ Relatório semanal enviado via Slack com sucesso")
                elif email_success:
                    self.logger.info("✅ Relatório semanal enviado via email com sucesso")
                else:
                    self.logger.error("❌ Falha ao enviar relatório semanal (Slack e Email)")
            else:
                self.logger.error("❌ Não foi possível obter dados para relatório semanal")
                
        except Exception as e:
            self.logger.error(f"❌ Erro no relatório semanal: {e}")
    
    def _send_monthly_report(self):
        """Envia relatório mensal"""
        try:
            self.logger.info("📊 Iniciando relatório mensal...")
            
            # Obter dados
            metrics = self.ga4_client.get_basic_metrics(days=30)
            daily_data = self.ga4_client.get_daily_metrics(days=30)
            top_pages = self.ga4_client.get_top_pages(days=30, limit=15)
            
            if metrics:
                # Gerar insights de IA
                insights = self.ai_analyzer.analyze_metrics(metrics)
                
                # Enviar via Slack (prioritário)
                slack_success = False
                if SLACK_REPORTS_ENABLED:
                    slack_success = self.slack_client.send_monthly_report(metrics, daily_data, top_pages, insights)
                
                # Fallback para email se Slack falhar
                email_success = False
                if not slack_success:
                    email_success = self.email_sender.send_weekly_report(metrics, daily_data, top_pages)  # Reutiliza função semanal
                
                if slack_success:
                    self.logger.info("✅ Relatório mensal enviado via Slack com sucesso")
                elif email_success:
                    self.logger.info("✅ Relatório mensal enviado via email com sucesso")
                else:
                    self.logger.error("❌ Falha ao enviar relatório mensal (Slack e Email)")
            else:
                self.logger.error("❌ Não foi possível obter dados para relatório mensal")
                
        except Exception as e:
            self.logger.error(f"❌ Erro no relatório mensal: {e}")
    
    def send_manual_report(self, report_type="daily"):
        """Envia relatório manual"""
        try:
            self.logger.info(f"📊 Enviando relatório manual ({report_type})...")
            
            if report_type == "daily":
                self._send_daily_report()
            elif report_type == "weekly":
                self._send_weekly_report()
            elif report_type == "monthly":
                self._send_monthly_report()
            else:
                self.logger.error(f"❌ Tipo de relatório inválido: {report_type}")
                
        except Exception as e:
            self.logger.error(f"❌ Erro no relatório manual: {e}")
    
    def get_scheduler_status(self):
        """Retorna status do agendador"""
        return {
            'running': self.scheduler.running,
            'jobs': [job.name for job in self.scheduler.get_jobs()],
            'next_run': [job.next_run_time for job in self.scheduler.get_jobs()]
        }
