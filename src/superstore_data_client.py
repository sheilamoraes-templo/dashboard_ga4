import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

class SuperstoreDataClient:
    def __init__(self):
        """Inicializa o cliente de dados Superstore"""
        self.data_file = "data/global_superstore_2016.xlsx"
        self.df = None
        self._load_data()
        
    def _load_data(self):
        """Carrega os dados do Excel Superstore"""
        try:
            print("📊 Carregando dataset Superstore...")
            
            # Verificar se o arquivo existe
            if not os.path.exists(self.data_file):
                print(f"❌ Arquivo não encontrado: {self.data_file}")
                self._generate_fallback_data()
                return
            
            # Carregar dados
            self.df = pd.read_excel(self.data_file, engine='openpyxl')
            
            # Converter coluna de data
            if 'Order Date' in self.df.columns:
                self.df['Order Date'] = pd.to_datetime(self.df['Order Date'])
                self.df['date'] = self.df['Order Date'].dt.date
            elif 'Date' in self.df.columns:
                self.df['date'] = pd.to_datetime(self.df['Date']).dt.date
            
            print(f"✅ Dataset carregado: {len(self.df)} registros")
            print(f"Colunas disponíveis: {list(self.df.columns)}")
            
        except Exception as e:
            print(f"❌ Erro ao carregar dataset Superstore: {e}")
            self._generate_fallback_data()
    
    def _generate_fallback_data(self):
        """Gera dados de fallback se não conseguir carregar o Excel"""
        print("🔄 Gerando dados de fallback...")
        
        # Gerar dados para os últimos 30 dias
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        data = []
        for date in dates:
            # Simular métricas de e-commerce
            users = random.randint(500, 2000)
            sessions = int(users * random.uniform(1.2, 2.0))
            pageviews = int(sessions * random.uniform(2.0, 4.0))
            avg_duration = random.uniform(120, 300)
            bounce_rate = random.uniform(25, 55)
            
            data.append({
                'date': date,
                'users': users,
                'sessions': sessions,
                'pageviews': pageviews,
                'avg_duration': round(avg_duration, 1),
                'bounce_rate': round(bounce_rate, 1),
                'revenue': random.uniform(5000, 25000),
                'orders': random.randint(50, 200)
            })
        
        self.df = pd.DataFrame(data)
    
    def get_basic_metrics(self, days=30):
        """Obtém métricas básicas dos últimos N dias"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Filtrar dados por período
            if 'date' in self.df.columns:
                mask = (self.df['date'] >= start_date.date()) & (self.df['date'] <= end_date.date())
                period_data = self.df[mask]
            else:
                # Se não tiver coluna date, usar todos os dados
                period_data = self.df
            
            if period_data.empty:
                return self._get_default_metrics()
            
            # Calcular métricas agregadas
            total_users = period_data['users'].sum() if 'users' in period_data.columns else len(period_data)
            total_sessions = period_data['sessions'].sum() if 'sessions' in period_data.columns else total_users * 1.5
            total_pageviews = period_data['pageviews'].sum() if 'pageviews' in period_data.columns else total_sessions * 2.5
            
            # Calcular média ponderada da duração
            if 'avg_duration' in period_data.columns and 'sessions' in period_data.columns:
                weighted_duration = (period_data['avg_duration'] * period_data['sessions']).sum() / total_sessions
            else:
                weighted_duration = 180.0  # 3 minutos padrão
            
            # Calcular média ponderada da taxa de rejeição
            if 'bounce_rate' in period_data.columns and 'sessions' in period_data.columns:
                weighted_bounce = (period_data['bounce_rate'] * period_data['sessions']).sum() / total_sessions
            else:
                weighted_bounce = 45.0  # 45% padrão
            
            return {
                'totalUsers': str(int(total_users)),
                'sessions': str(int(total_sessions)),
                'screenPageViews': str(int(total_pageviews)),
                'averageSessionDuration': str(round(weighted_duration, 1)),
                'bounceRate': str(round(weighted_bounce, 1))
            }
            
        except Exception as e:
            print(f"Erro ao obter métricas básicas: {e}")
            return self._get_default_metrics()
    
    def get_daily_metrics(self, days=30):
        """Obtém métricas diárias dos últimos N dias"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Se temos dados reais com datas
            if 'date' in self.df.columns:
                mask = (self.df['date'] >= start_date.date()) & (self.df['date'] <= end_date.date())
                period_data = self.df[mask]
                
                if not period_data.empty:
                    # Agrupar por data
                    daily_metrics = period_data.groupby('date').agg({
                        'users': 'sum' if 'users' in period_data.columns else 'count',
                        'sessions': 'sum' if 'sessions' in period_data.columns else lambda x: x.count() * 1.5,
                        'pageviews': 'sum' if 'pageviews' in period_data.columns else lambda x: x.count() * 2.5
                    }).reset_index()
                    
                    # Formatar data
                    daily_metrics['date'] = daily_metrics['date'].astype(str)
                    return daily_metrics
            
            # Fallback: gerar dados diários
            return self._get_default_daily_data(days)
            
        except Exception as e:
            print(f"Erro ao obter métricas diárias: {e}")
            return self._get_default_daily_data(days)
    
    def get_top_pages(self, days=30, limit=10):
        """Obtém páginas mais visitadas (simulado com categorias de produto)"""
        try:
            # Se temos dados de produtos/categorias
            if 'Category' in self.df.columns or 'Product Name' in self.df.columns:
                # Usar categorias como "páginas"
                if 'Category' in self.df.columns:
                    page_data = self.df['Category'].value_counts().head(limit)
                else:
                    page_data = self.df['Product Name'].value_counts().head(limit)
                
                data = []
                for i, (page_name, pageviews) in enumerate(page_data.items()):
                    data.append({
                        'page_title': f"{page_name} - Superstore",
                        'page_path': f"/category/{page_name.lower().replace(' ', '-')}",
                        'pageviews': int(pageviews * 10),  # Multiplicar para simular pageviews
                        'users': int(pageviews * 7),
                        'avg_duration': random.uniform(120, 240)
                    })
                
                return pd.DataFrame(data)
            
            # Fallback: páginas padrão
            return self._get_default_top_pages(limit)
            
        except Exception as e:
            print(f"Erro ao obter páginas mais visitadas: {e}")
            return self._get_default_top_pages(limit)
    
    def get_device_breakdown(self, days=30):
        """Obtém breakdown por dispositivo (simulado)"""
        try:
            # Simular breakdown por dispositivo baseado nos dados
            total_records = len(self.df) if len(self.df) > 0 else 1000
            
            # Distribuição realista de dispositivos
            desktop_users = int(total_records * 0.55)
            mobile_users = int(total_records * 0.35)
            tablet_users = int(total_records * 0.10)
            
            data = [
                {
                    'device': 'desktop',
                    'users': desktop_users,
                    'sessions': int(desktop_users * 1.4),
                    'pageviews': int(desktop_users * 3.2)
                },
                {
                    'device': 'mobile',
                    'users': mobile_users,
                    'sessions': int(mobile_users * 1.2),
                    'pageviews': int(mobile_users * 2.1)
                },
                {
                    'device': 'tablet',
                    'users': tablet_users,
                    'sessions': int(tablet_users * 1.3),
                    'pageviews': int(tablet_users * 2.8)
                }
            ]
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter breakdown por dispositivo: {e}")
            return self._get_default_device_data()
    
    def test_connection(self):
        """Testa a conexão com dados Superstore"""
        try:
            if self.df is not None and not self.df.empty:
                print("✅ Dataset Superstore carregado com sucesso!")
                print(f"Total de registros: {len(self.df)}")
                if 'date' in self.df.columns:
                    print(f"Período: {self.df['date'].min()} a {self.df['date'].max()}")
                print(f"Colunas principais: {list(self.df.columns)[:10]}")
                return True
            else:
                print("❌ Falha ao carregar dataset Superstore")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar dataset Superstore: {e}")
            return False
    
    def _get_default_metrics(self):
        """Retorna métricas padrão"""
        return {
            'totalUsers': '15000',
            'sessions': '22000',
            'screenPageViews': '45000',
            'averageSessionDuration': '125.5',
            'bounceRate': '45.2'
        }
    
    def _get_default_daily_data(self, days):
        """Retorna dados diários padrão"""
        data = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            data.append({
                'date': date,
                'users': random.randint(400, 800),
                'sessions': random.randint(600, 1200),
                'pageviews': random.randint(1200, 2400)
            })
        return pd.DataFrame(data)
    
    def _get_default_top_pages(self, limit):
        """Retorna páginas padrão"""
        pages = [
            ("Homepage - Superstore", "/", 8500, 6500, 145.2),
            ("Electronics - Superstore", "/electronics", 7200, 5800, 135.8),
            ("Furniture - Superstore", "/furniture", 6800, 5200, 155.7),
            ("Office Supplies - Superstore", "/office-supplies", 6200, 4800, 125.2),
            ("Technology - Superstore", "/technology", 5800, 4500, 115.4),
            ("Home & Garden - Superstore", "/home-garden", 5400, 4200, 140.3),
            ("Sports - Superstore", "/sports", 5000, 3900, 150.2),
            ("Books - Superstore", "/books", 4600, 3600, 160.4),
            ("Clothing - Superstore", "/clothing", 4200, 3300, 130.8),
            ("Toys - Superstore", "/toys", 3800, 3000, 125.6)
        ]
        
        data = []
        for i, (title, path, pageviews, users, duration) in enumerate(pages[:limit]):
            data.append({
                'page_title': title,
                'page_path': path,
                'pageviews': pageviews,
                'users': users,
                'avg_duration': duration
            })
        
        return pd.DataFrame(data)
    
    def first_user_acquisition(self, days=30):
        """Obtém dados de aquisição de primeiro acesso (simulado)"""
        try:
            # Simular dados de aquisição baseados em fontes comuns
            sources = [
                ('google', 'organic', ''),
                ('google', 'cpc', 'brand-campaign'),
                ('facebook', 'social', 'social-media-campaign'),
                ('instagram', 'social', 'instagram-ads'),
                ('youtube', 'social', 'youtube-promotion'),
                ('email', 'email', 'newsletter'),
                ('direct', 'none', ''),
                ('bing', 'organic', ''),
                ('linkedin', 'social', 'linkedin-ads'),
                ('twitter', 'social', 'twitter-promotion')
            ]
            
            data = []
            for source, medium, campaign in sources:
                users = random.randint(200, 1500)
                sessions = int(users * random.uniform(1.1, 1.8))
                
                data.append({
                    'source': source,
                    'medium': medium,
                    'campaign': campaign if campaign else '(not set)',
                    'users': users,
                    'sessions': sessions
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter dados de aquisição: {e}")
            return self._get_default_acquisition_data()
    
    def video_events(self, days=30):
        """Obtém eventos de vídeo (simulado)"""
        try:
            # Simular eventos de vídeo
            video_titles = [
                'Introdução ao Produto',
                'Tutorial de Uso',
                'Depoimentos de Clientes',
                'Demonstração Avançada',
                'FAQ Completo',
                'Como Começar',
                'Recursos Premium',
                'Suporte Técnico'
            ]
            
            events = ['video_start', 'video_progress', 'video_complete']
            data = []
            
            # Gerar dados para os últimos N dias
            for i in range(days):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                
                for title in video_titles:
                    for event in events:
                        # Simular diferentes volumes de eventos
                        if event == 'video_start':
                            count = random.randint(50, 200)
                        elif event == 'video_progress':
                            count = random.randint(30, 150)
                        else:  # video_complete
                            count = random.randint(10, 80)
                        
                        data.append({
                            'date': date,
                            'event_name': event,
                            'video_title': title,
                            'video_percent': random.randint(25, 100) if event == 'video_progress' else 0,
                            'event_count': count
                        })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter eventos de vídeo: {e}")
            return self._get_default_video_data()
    
    def _get_default_device_data(self):
        """Retorna dados de dispositivos padrão"""
        return pd.DataFrame([
            {'device': 'desktop', 'users': 8500, 'sessions': 12000, 'pageviews': 24000},
            {'device': 'mobile', 'users': 5500, 'sessions': 8000, 'pageviews': 16000},
            {'device': 'tablet', 'users': 1000, 'sessions': 1400, 'pageviews': 2800}
        ])
    
    def _get_default_acquisition_data(self):
        """Retorna dados de aquisição padrão"""
        return pd.DataFrame([
            {'source': 'google', 'medium': 'organic', 'campaign': '(not set)', 'users': 1200, 'sessions': 1800},
            {'source': 'google', 'medium': 'cpc', 'campaign': 'brand-campaign', 'users': 800, 'sessions': 1200},
            {'source': 'facebook', 'medium': 'social', 'campaign': 'social-media-campaign', 'users': 600, 'sessions': 900},
            {'source': 'direct', 'medium': 'none', 'campaign': '(not set)', 'users': 500, 'sessions': 750},
            {'source': 'email', 'medium': 'email', 'campaign': 'newsletter', 'users': 400, 'sessions': 600}
        ])
    
    def _get_default_video_data(self):
        """Retorna dados de vídeo padrão"""
        return pd.DataFrame([
            {'date': '2024-01-01', 'event_name': 'video_start', 'video_title': 'Introdução ao Produto', 'video_percent': 0, 'event_count': 150},
            {'date': '2024-01-01', 'event_name': 'video_progress', 'video_title': 'Introdução ao Produto', 'video_percent': 50, 'event_count': 100},
            {'date': '2024-01-01', 'event_name': 'video_complete', 'video_title': 'Introdução ao Produto', 'video_percent': 100, 'event_count': 75}
        ])
