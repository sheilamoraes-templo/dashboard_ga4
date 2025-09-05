#!/usr/bin/env python3
"""
Pipeline GA4 Simplificado - Versão que Funciona
Usa os dados existentes e melhora gradualmente
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleGA4Pipeline:
    """Pipeline simplificado que funciona com dados existentes"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        """Garante que a pasta data existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"📁 Pasta {self.data_dir} criada")
    
    def create_sample_data(self):
        """Cria dados de exemplo baseados no que você precisa"""
        logger.info("📊 Criando dados de exemplo...")
        
        # 1. Métricas principais (30 dias)
        self.create_kpis_daily()
        
        # 2. Top páginas
        self.create_pages_top()
        
        # 3. Breakdown por dispositivo
        self.create_devices()
        
        # 4. Primeiros acessos
        self.create_first_user_acquisition()
        
        # 5. Eventos de vídeo
        self.create_video_events()
        
        # 6. Comparação semanal
        self.create_weekly_comparison()
        
        # 7. Dias com mais usuários
        self.create_days_with_most_users()
        
        logger.info("✅ Dados de exemplo criados com sucesso!")
    
    def create_kpis_daily(self):
        """Cria métricas principais diárias"""
        logger.info("📈 Criando métricas principais...")
        
        # Gerar 30 dias de dados
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = []
        for i, date in enumerate(dates):
            # Dados realistas com variação
            base_users = 50 + (i % 7) * 10  # Variação semanal
            users = max(20, base_users + (i % 3) * 5)
            sessions = int(users * (1.5 + (i % 5) * 0.2))
            pageviews = int(sessions * (3 + (i % 4) * 0.5))
            duration = 200 + (i % 6) * 50  # 200-500 segundos
            bounce_rate = 0.3 + (i % 4) * 0.1  # 30-70%
            
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'users': users,
                'sessions': sessions,
                'pageviews': pageviews,
                'avg_session_duration': duration,
                'bounce_rate': bounce_rate
            })
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.data_dir, "kpis_daily.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ kpis_daily.csv criado: {len(df)} registros")
    
    def create_pages_top(self):
        """Cria top páginas"""
        logger.info("📄 Criando top páginas...")
        
        pages = [
            '/', '/sobre', '/contato', '/produtos', '/blog',
            '/servicos', '/portfolio', '/depoimentos', '/faq', '/contato',
            '/curso/view.php', '/login', '/cadastro', '/dashboard', '/perfil',
            '/configuracoes', '/ajuda', '/suporte', '/termos', '/privacidade'
        ]
        
        data = []
        for i, page in enumerate(pages):
            # Pageviews decrescentes
            pageviews = max(100, 2000 - i * 80)
            sessions = int(pageviews * 0.6)
            users = int(sessions * 0.8)
            
            data.append({
                'page': page,
                'pageviews': pageviews,
                'sessions': sessions,
                'users': users
            })
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.data_dir, "pages_top.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ pages_top.csv criado: {len(df)} registros")
    
    def create_devices(self):
        """Cria breakdown por dispositivo"""
        logger.info("📱 Criando breakdown por dispositivo...")
        
        data = [
            {'device': 'desktop', 'users': 180, 'sessions': 220, 'pageviews': 850},
            {'device': 'mobile', 'users': 120, 'sessions': 150, 'pageviews': 600},
            {'device': 'tablet', 'users': 45, 'sessions': 55, 'pageviews': 200}
        ]
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.data_dir, "devices.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ devices.csv criado: {len(df)} registros")
    
    def create_first_user_acquisition(self):
        """Cria dados de primeiros acessos"""
        logger.info("🎯 Criando primeiros acessos...")
        
        sources = [
            {'source': 'google', 'medium': 'organic', 'users': 85, 'sessions': 100},
            {'source': 'facebook', 'medium': 'social', 'users': 45, 'sessions': 60},
            {'source': 'instagram', 'medium': 'social', 'users': 35, 'sessions': 45},
            {'source': 'linkedin', 'medium': 'social', 'users': 25, 'sessions': 30},
            {'source': 'email', 'medium': 'email', 'users': 40, 'sessions': 50},
            {'source': 'direct', 'medium': '(none)', 'users': 30, 'sessions': 35},
            {'source': 'youtube', 'medium': 'social', 'users': 20, 'sessions': 25}
        ]
        
        df = pd.DataFrame(sources)
        filepath = os.path.join(self.data_dir, "first_user_acquisition.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ first_user_acquisition.csv criado: {len(df)} registros")
    
    def create_video_events(self):
        """Cria eventos de vídeo"""
        logger.info("🎬 Criando eventos de vídeo...")
        
        events = [
            {'date': '2024-01-01', 'event_name': 'video_start', 'count': 150},
            {'date': '2024-01-01', 'event_name': 'video_progress', 'count': 120},
            {'date': '2024-01-01', 'event_name': 'video_complete', 'count': 85},
            {'date': '2024-01-02', 'event_name': 'video_start', 'count': 180},
            {'date': '2024-01-02', 'event_name': 'video_progress', 'count': 140},
            {'date': '2024-01-02', 'event_name': 'video_complete', 'count': 95},
            {'date': '2024-01-03', 'event_name': 'video_start', 'count': 200},
            {'date': '2024-01-03', 'event_name': 'video_progress', 'count': 160},
            {'date': '2024-01-03', 'event_name': 'video_complete', 'count': 110}
        ]
        
        df = pd.DataFrame(events)
        filepath = os.path.join(self.data_dir, "video_events.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ video_events.csv criado: {len(df)} registros")
    
    def create_weekly_comparison(self):
        """Cria comparação semanal"""
        logger.info("📅 Criando comparação semanal...")
        
        weeks = [
            {'week': '2024-W01', 'users': 1200, 'sessions': 1500, 'pageviews': 4500, 'avg_session_duration': 280, 'bounce_rate': 0.45},
            {'week': '2024-W02', 'users': 1350, 'sessions': 1700, 'pageviews': 5200, 'avg_session_duration': 295, 'bounce_rate': 0.42},
            {'week': '2024-W03', 'users': 1100, 'sessions': 1400, 'pageviews': 4200, 'avg_session_duration': 275, 'bounce_rate': 0.48},
            {'week': '2024-W04', 'users': 1450, 'sessions': 1800, 'pageviews': 5500, 'avg_session_duration': 310, 'bounce_rate': 0.38}
        ]
        
        df = pd.DataFrame(weeks)
        filepath = os.path.join(self.data_dir, "weekly_comparison.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ weekly_comparison.csv criado: {len(df)} registros")
    
    def create_days_with_most_users(self):
        """Cria dias com mais usuários"""
        logger.info("📈 Criando dias com mais usuários...")
        
        # Top 10 dias dos últimos 30 dias
        data = []
        for i in range(10):
            users = 200 - i * 15  # Decrescente
            sessions = int(users * 1.3)
            pageviews = int(sessions * 3.2)
            duration = 250 + i * 20
            bounce_rate = 0.35 + i * 0.03
            
            data.append({
                'date': f'2024-01-{(i+1):02d}',
                'users': users,
                'sessions': sessions,
                'pageviews': pageviews,
                'avg_session_duration': duration,
                'bounce_rate': bounce_rate
            })
        
        df = pd.DataFrame(data)
        filepath = os.path.join(self.data_dir, "days_with_most_users.csv")
        df.to_csv(filepath, index=False)
        logger.info(f"✅ days_with_most_users.csv criado: {len(df)} registros")
    
    def run_pipeline(self):
        """Executa o pipeline completo"""
        logger.info("🚀 Iniciando pipeline simplificado...")
        
        try:
            self.create_sample_data()
            
            logger.info("🎉 Pipeline executado com sucesso!")
            logger.info("📁 Dados criados na pasta 'data/'")
            logger.info("🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no pipeline: {e}")
            return False

def main():
    """Função principal"""
    print("🚀 PIPELINE GA4 SIMPLIFICADO")
    print("=" * 40)
    print("📊 Criando dados de exemplo para o dashboard")
    print("=" * 40)
    
    pipeline = SimpleGA4Pipeline()
    success = pipeline.run_pipeline()
    
    if success:
        print("\n✅ Pipeline executado com sucesso!")
        print("📁 Dados disponíveis na pasta 'data/'")
        print("🌐 Execute: streamlit run streamlit_dashboard.py")
    else:
        print("\n❌ Pipeline falhou")

if __name__ == "__main__":
    main()
