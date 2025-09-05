import requests
import json
from datetime import datetime
from config.settings import SLACK_BOT_TOKEN, SLACK_CHANNEL, SLACK_WEBHOOK_URL, SLACK_REPORTS_ENABLED

class SlackClient:
    def __init__(self):
        """Inicializa o cliente Slack"""
        self.bot_token = SLACK_BOT_TOKEN
        self.channel = SLACK_CHANNEL
        self.webhook_url = SLACK_WEBHOOK_URL
        self.enabled = SLACK_REPORTS_ENABLED
        
        # Verificar se as configurações estão válidas
        self.use_webhook = self.webhook_url and self.webhook_url != "https://hooks.slack.com/services/sua_webhook_aqui"
        self.use_bot_token = self.bot_token and self.bot_token != "xoxb-sua_chave_slack_aqui"
        
        if not self.enabled:
            print("⚠️ Relatórios Slack desabilitados")
        elif not (self.use_webhook or self.use_bot_token):
            print("⚠️ Slack não configurado - configure SLACK_BOT_TOKEN ou SLACK_WEBHOOK_URL")
        else:
            print("✅ Cliente Slack inicializado")
    
    def send_message(self, text, blocks=None):
        """Envia mensagem para o canal Slack"""
        if not self.enabled:
            print("📵 Slack desabilitado - mensagem não enviada")
            return False
            
        try:
            if self.use_webhook:
                return self._send_via_webhook(text, blocks)
            elif self.use_bot_token:
                return self._send_via_bot_token(text, blocks)
            else:
                print("❌ Nenhum método de envio Slack configurado")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem Slack: {e}")
            return False
    
    def _send_via_webhook(self, text, blocks=None):
        """Envia mensagem via Webhook"""
        payload = {
            "text": text,
            "channel": self.channel.replace("#", ""),
        }
        
        if blocks:
            payload["blocks"] = blocks
        
        response = requests.post(self.webhook_url, json=payload)
        
        if response.status_code == 200:
            print("✅ Mensagem enviada via Webhook Slack")
            return True
        else:
            print(f"❌ Erro Webhook Slack: {response.status_code} - {response.text}")
            return False
    
    def _send_via_bot_token(self, text, blocks=None):
        """Envia mensagem via Bot Token"""
        url = "https://slack.com/api/chat.postMessage"
        
        headers = {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "channel": self.channel,
            "text": text
        }
        
        if blocks:
            payload["blocks"] = blocks
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("ok"):
                print("✅ Mensagem enviada via Bot Token Slack")
                return True
            else:
                print(f"❌ Erro Bot Token Slack: {result.get('error', 'Erro desconhecido')}")
                return False
        else:
            print(f"❌ Erro HTTP Bot Token Slack: {response.status_code}")
            return False
    
    def send_metrics_report(self, metrics_data, daily_data=None, top_pages=None, insights=None):
        """Envia relatório de métricas para o Slack"""
        try:
            # Criar blocos do Slack para formatação rica
            blocks = self._create_metrics_blocks(metrics_data, daily_data, top_pages, insights)
            
            # Texto simples como fallback
            text = self._create_simple_report_text(metrics_data)
            
            return self.send_message(text, blocks)
            
        except Exception as e:
            print(f"❌ Erro ao criar relatório Slack: {e}")
            return False
    
    def _create_metrics_blocks(self, metrics_data, daily_data=None, top_pages=None, insights=None):
        """Cria blocos formatados para Slack"""
        blocks = []
        
        # Cabeçalho
        blocks.append({
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"📊 Relatório GA4 - {datetime.now().strftime('%d/%m/%Y')}"
            }
        })
        
        # Divisor
        blocks.append({"type": "divider"})
        
        # Métricas principais
        metrics_text = f"""*📈 Métricas Principais (Últimos 30 dias)*
• *Usuários:* {metrics_data.get('totalUsers', 'N/A'):,}
• *Sessões:* {metrics_data.get('sessions', 'N/A'):,}
• *Visualizações:* {metrics_data.get('screenPageViews', 'N/A'):,}
• *Duração Média:* {float(metrics_data.get('averageSessionDuration', 0))/60:.1f} min
• *Taxa de Rejeição:* {float(metrics_data.get('bounceRate', 0)):.1f}%"""
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": metrics_text
            }
        })
        
        # Insights de IA
        if insights:
            blocks.append({"type": "divider"})
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🤖 Análise de IA*\n{insights[:500]}{'...' if len(insights) > 500 else ''}"
                }
            })
        
        # Top páginas
        if top_pages is not None and not top_pages.empty:
            blocks.append({"type": "divider"})
            pages_text = "*🔥 Páginas Mais Visitadas*\n"
            for i, (_, row) in enumerate(top_pages.head(3).iterrows()):
                pages_text += f"{i+1}. *{row['page_title']}* - {row['pageviews']:,} visualizações\n"
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": pages_text
                }
            })
        
        # Rodapé
        blocks.append({"type": "divider"})
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Relatório gerado automaticamente pelo Dashboard GA4 • {datetime.now().strftime('%d/%m/%Y %H:%M')}"
                }
            ]
        })
        
        return blocks
    
    def _create_simple_report_text(self, metrics_data):
        """Cria texto simples para fallback"""
        return f"""📊 *Relatório GA4 - {datetime.now().strftime('%d/%m/%Y')}*

📈 *Métricas Principais:*
• Usuários: {metrics_data.get('totalUsers', 'N/A'):,}
• Sessões: {metrics_data.get('sessions', 'N/A'):,}
• Visualizações: {metrics_data.get('screenPageViews', 'N/A'):,}
• Duração Média: {float(metrics_data.get('averageSessionDuration', 0))/60:.1f} min
• Taxa de Rejeição: {float(metrics_data.get('bounceRate', 0)):.1f}%

Relatório gerado automaticamente pelo Dashboard GA4"""
    
    def test_connection(self):
        """Testa a conexão com Slack"""
        try:
            if not self.enabled:
                print("📵 Slack desabilitado")
                return False
            
            if not (self.use_webhook or self.use_bot_token):
                print("❌ Slack não configurado")
                return False
            
            # Enviar mensagem de teste
            test_message = f"🧪 Teste de conexão - {datetime.now().strftime('%d/%m/%Y %H:%M')}"
            success = self.send_message(test_message)
            
            if success:
                print("✅ Conexão com Slack estabelecida com sucesso!")
                return True
            else:
                print("❌ Falha na conexão com Slack")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao testar conexão Slack: {e}")
            return False
    
    def send_daily_report(self, metrics_data, daily_data=None, top_pages=None, insights=None):
        """Envia relatório diário"""
        return self.send_metrics_report(metrics_data, daily_data, top_pages, insights)
    
    def send_weekly_report(self, metrics_data, daily_data=None, top_pages=None, insights=None):
        """Envia relatório semanal"""
        return self.send_metrics_report(metrics_data, daily_data, top_pages, insights)
    
    def send_monthly_report(self, metrics_data, daily_data=None, top_pages=None, insights=None):
        """Envia relatório mensal"""
        return self.send_metrics_report(metrics_data, daily_data, top_pages, insights)
