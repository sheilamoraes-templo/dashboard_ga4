import requests
import json
import google.generativeai as genai
from datetime import datetime
from config.settings import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, GEMINI_API_KEY

class AIAnalyzer:
    def __init__(self):
        """Inicializa o analisador de IA"""
        self.openrouter_api_key = OPENROUTER_API_KEY
        self.openrouter_base_url = OPENROUTER_BASE_URL
        self.gemini_api_key = GEMINI_API_KEY
        
        # Configurar Gemini se a chave estiver disponível
        if self.gemini_api_key and self.gemini_api_key != "sua_chave_gemini_aqui":
            try:
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.use_gemini = True
            except Exception as e:
                print(f"Erro ao configurar Gemini: {e}")
                self.use_gemini = False
        else:
            self.use_gemini = False
        
    def analyze_metrics(self, metrics_data):
        """Analisa métricas usando IA e gera insights"""
        try:
            prompt = self._create_analysis_prompt(metrics_data)
            
            # Tentar Gemini primeiro
            if self.use_gemini:
                try:
                    response = self.gemini_model.generate_content(prompt)
                    if response.text:
                        return response.text
                except Exception as e:
                    print(f"Erro no Gemini: {e}")
            
            # Fallback para OpenRouter
            if self.openrouter_api_key and self.openrouter_api_key != "sua_chave_openrouter_aqui":
                try:
                    headers = {
                        "Authorization": f"Bearer {self.openrouter_api_key}",
                        "Content-Type": "application/json"
                    }
                    
                    data = {
                        "model": "openai/gpt-3.5-turbo",
                        "messages": [
                            {
                                "role": "system",
                                "content": "Você é um analista de dados especializado em Google Analytics 4. Analise os dados fornecidos e forneça insights úteis em português brasileiro."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "max_tokens": 500
                    }
                    
                    response = requests.post(
                        f"{self.openrouter_base_url}/chat/completions",
                        headers=headers,
                        json=data
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        print(f"Erro na API OpenRouter: {response.status_code}")
                except Exception as e:
                    print(f"Erro ao usar OpenRouter: {e}")
            
            # Fallback para insights básicos
            return self._generate_fallback_insights(metrics_data)
                
        except Exception as e:
            print(f"Erro ao analisar com IA: {e}")
            return self._generate_fallback_insights(metrics_data)
    
    def _create_analysis_prompt(self, metrics_data):
        """Cria prompt para análise de IA"""
        prompt = f"""
        Analise os seguintes dados do Google Analytics 4 e forneça insights úteis:

        Dados dos últimos 30 dias:
        - Usuários totais: {metrics_data.get('totalUsers', 'N/A')}
        - Sessões: {metrics_data.get('sessions', 'N/A')}
        - Visualizações de página: {metrics_data.get('screenPageViews', 'N/A')}
        - Duração média da sessão: {metrics_data.get('averageSessionDuration', 'N/A')} segundos
        - Taxa de rejeição: {metrics_data.get('bounceRate', 'N/A')}%

        Por favor, forneça:
        1. Análise geral do desempenho
        2. Principais pontos positivos
        3. Áreas de melhoria
        4. Recomendações práticas
        5. Tendências observadas

        Responda em português brasileiro de forma clara e objetiva.
        """
        return prompt
    
    def _generate_fallback_insights(self, metrics_data):
        """Gera insights básicos quando IA não está disponível"""
        users = int(metrics_data.get('totalUsers', 0))
        sessions = int(metrics_data.get('sessions', 0))
        pageviews = int(metrics_data.get('screenPageViews', 0))
        avg_duration = float(metrics_data.get('averageSessionDuration', 0))
        bounce_rate = float(metrics_data.get('bounceRate', 0))
        
        insights = f"""
        📊 **Análise Automática dos Dados GA4**
        
        **Métricas Principais (últimos 30 dias):**
        • Usuários únicos: {users:,}
        • Sessões: {sessions:,}
        • Visualizações de página: {pageviews:,}
        • Duração média da sessão: {avg_duration:.1f} segundos
        • Taxa de rejeição: {bounce_rate:.1f}%
        
        **Análise Rápida:**
        • Páginas por sessão: {pageviews/sessions:.1f} (meta: >2.0)
        • Duração por sessão: {avg_duration/60:.1f} minutos
        
        **Recomendações Básicas:**
        • {'✅ Boa taxa de rejeição' if bounce_rate < 50 else '⚠️ Taxa de rejeição alta - revise conteúdo'}
        • {'✅ Boa duração de sessão' if avg_duration > 120 else '⚠️ Sessões muito curtas - melhore engajamento'}
        • {'✅ Bom volume de usuários' if users > 100 else '⚠️ Baixo tráfego - considere marketing'}
        
        *Para análises mais detalhadas, configure sua chave da OpenRouter.*
        """
        
        return insights
    
    def generate_email_content(self, metrics_data, daily_data=None, top_pages=None):
        """Gera conteúdo para email com análise de IA"""
        try:
            # Análise principal
            main_analysis = self.analyze_metrics(metrics_data)
            
            # Preparar dados para email
            email_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .header {{ background-color: #4285f4; color: white; padding: 20px; text-align: center; }}
                    .metric {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .insight {{ background-color: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                    .footer {{ background-color: #f1f3f4; padding: 10px; text-align: center; font-size: 12px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>📊 Relatório GA4 - {datetime.now().strftime('%d/%m/%Y')}</h1>
                </div>
                
                <div class="metric">
                    <h2>📈 Métricas Principais (Últimos 30 dias)</h2>
                    <p><strong>Usuários:</strong> {metrics_data.get('totalUsers', 'N/A'):,}</p>
                    <p><strong>Sessões:</strong> {metrics_data.get('sessions', 'N/A'):,}</p>
                    <p><strong>Visualizações:</strong> {metrics_data.get('screenPageViews', 'N/A'):,}</p>
                    <p><strong>Duração Média:</strong> {float(metrics_data.get('averageSessionDuration', 0))/60:.1f} min</p>
                    <p><strong>Taxa de Rejeição:</strong> {float(metrics_data.get('bounceRate', 0)):.1f}%</p>
                </div>
                
                <div class="insight">
                    <h2>🤖 Análise de IA</h2>
                    {main_analysis.replace(chr(10), '<br>')}
                </div>
            """
            
            # Adicionar top páginas se disponível
            if top_pages is not None and not top_pages.empty:
                email_content += """
                <div class="metric">
                    <h2>🔥 Páginas Mais Visitadas</h2>
                    <ul>
                """
                for _, row in top_pages.head(5).iterrows():
                    email_content += f"<li><strong>{row['page_title']}</strong> - {row['pageviews']:,} visualizações</li>"
                email_content += "</ul></div>"
            
            email_content += """
                <div class="footer">
                    <p>Relatório gerado automaticamente pelo Dashboard GA4</p>
                    <p>Data: """ + datetime.now().strftime('%d/%m/%Y %H:%M') + """</p>
                </div>
            </body>
            </html>
            """
            
            return email_content
            
        except Exception as e:
            print(f"Erro ao gerar conteúdo do email: {e}")
            return "Erro ao gerar relatório"
