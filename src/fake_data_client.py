import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class FakeDataClient:
    def __init__(self):
        """Inicializa o cliente de dados fake"""
        self.data_file = "data/fake_ga4_data.csv"
        self.df = None
        self._load_data()
        
    def _load_data(self):
        """Carrega os dados fake do CSV"""
        try:
            self.df = pd.read_csv(self.data_file)
            self.df['date'] = pd.to_datetime(self.df['date'])
        except Exception as e:
            print(f"Erro ao carregar dados fake: {e}")
            self._generate_fake_data()
    
    def _generate_fake_data(self):
        """Gera dados fake se o arquivo não existir"""
        print("Gerando dados fake...")
        
        # Gerar dados para os últimos 30 dias
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        pages = [
            ("Homepage - Empresa XYZ", "/"),
            ("Produtos - Empresa XYZ", "/produtos"),
            ("Sobre Nós - Empresa XYZ", "/sobre"),
            ("Contato - Empresa XYZ", "/contato"),
            ("Blog - Empresa XYZ", "/blog"),
            ("Serviços - Empresa XYZ", "/servicos"),
            ("FAQ - Empresa XYZ", "/faq"),
            ("Preços - Empresa XYZ", "/precos"),
            ("Depoimentos - Empresa XYZ", "/depoimentos"),
            ("Portfolio - Empresa XYZ", "/portfolio")
        ]
        
        devices = ["desktop", "mobile", "tablet"]
        countries = ["Brazil", "United States", "Argentina", "Mexico", "Colombia"]
        
        data = []
        
        for date in dates:
            for page_title, page_path in pages:
                for device in devices:
                    for country in countries:
                        # Gerar métricas realistas
                        base_users = random.randint(50, 200)
                        if device == "desktop":
                            users = base_users
                        elif device == "mobile":
                            users = int(base_users * 0.7)
                        else:  # tablet
                            users = int(base_users * 0.2)
                        
                        sessions = int(users * random.uniform(1.2, 1.8))
                        pageviews = int(sessions * random.uniform(1.5, 2.5))
                        avg_duration = random.uniform(60, 180)
                        bounce_rate = random.uniform(20, 70)
                        
                        data.append({
                            'date': date,
                            'page_title': page_title,
                            'page_path': page_path,
                            'device_category': device,
                            'country': country,
                            'users': users,
                            'sessions': sessions,
                            'pageviews': pageviews,
                            'avg_duration': round(avg_duration, 1),
                            'bounce_rate': round(bounce_rate, 1)
                        })
        
        self.df = pd.DataFrame(data)
        
        # Salvar dados gerados
        try:
            self.df.to_csv(self.data_file, index=False)
            print(f"Dados fake salvos em {self.data_file}")
        except Exception as e:
            print(f"Erro ao salvar dados fake: {e}")
    
    def get_basic_metrics(self, days=30):
        """Obtém métricas básicas dos últimos N dias"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Filtrar dados por período
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            period_data = self.df[mask]
            
            if period_data.empty:
                return self._get_default_metrics()
            
            # Calcular métricas agregadas
            total_users = period_data['users'].sum()
            total_sessions = period_data['sessions'].sum()
            total_pageviews = period_data['pageviews'].sum()
            
            # Calcular média ponderada da duração
            weighted_duration = (period_data['avg_duration'] * period_data['sessions']).sum() / total_sessions
            
            # Calcular média ponderada da taxa de rejeição
            weighted_bounce = (period_data['bounce_rate'] * period_data['sessions']).sum() / total_sessions
            
            return {
                'totalUsers': str(total_users),
                'sessions': str(total_sessions),
                'screenPageViews': str(total_pageviews),
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
            
            # Filtrar dados por período
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            period_data = self.df[mask]
            
            if period_data.empty:
                return self._get_default_daily_data(days)
            
            # Agrupar por data
            daily_metrics = period_data.groupby('date').agg({
                'users': 'sum',
                'sessions': 'sum',
                'pageviews': 'sum'
            }).reset_index()
            
            # Formatar data
            daily_metrics['date'] = daily_metrics['date'].dt.strftime('%Y-%m-%d')
            
            return daily_metrics
            
        except Exception as e:
            print(f"Erro ao obter métricas diárias: {e}")
            return self._get_default_daily_data(days)
    
    def get_top_pages(self, days=30, limit=10):
        """Obtém páginas mais visitadas"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Filtrar dados por período
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            period_data = self.df[mask]
            
            if period_data.empty:
                return self._get_default_top_pages(limit)
            
            # Agrupar por página
            page_metrics = period_data.groupby(['page_title', 'page_path']).agg({
                'pageviews': 'sum',
                'users': 'sum',
                'avg_duration': lambda x: (x * period_data.loc[x.index, 'sessions']).sum() / period_data.loc[x.index, 'sessions'].sum()
            }).reset_index()
            
            # Ordenar por visualizações e limitar
            page_metrics = page_metrics.sort_values('pageviews', ascending=False).head(limit)
            
            # Renomear colunas
            page_metrics = page_metrics.rename(columns={
                'page_title': 'page_title',
                'page_path': 'page_path',
                'pageviews': 'pageviews',
                'users': 'users',
                'avg_duration': 'avg_duration'
            })
            
            return page_metrics
            
        except Exception as e:
            print(f"Erro ao obter páginas mais visitadas: {e}")
            return self._get_default_top_pages(limit)
    
    def get_device_breakdown(self, days=30):
        """Obtém breakdown por dispositivo"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Filtrar dados por período
            mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
            period_data = self.df[mask]
            
            if period_data.empty:
                return self._get_default_device_data()
            
            # Agrupar por dispositivo
            device_metrics = period_data.groupby('device_category').agg({
                'users': 'sum',
                'sessions': 'sum',
                'pageviews': 'sum'
            }).reset_index()
            
            # Renomear colunas
            device_metrics = device_metrics.rename(columns={
                'device_category': 'device',
                'users': 'users',
                'sessions': 'sessions',
                'pageviews': 'pageviews'
            })
            
            return device_metrics
            
        except Exception as e:
            print(f"Erro ao obter breakdown por dispositivo: {e}")
            return self._get_default_device_data()
    
    def test_connection(self):
        """Testa a conexão com dados fake"""
        try:
            if self.df is not None and not self.df.empty:
                print("✅ Dados fake carregados com sucesso!")
                print(f"Total de registros: {len(self.df)}")
                print(f"Período: {self.df['date'].min()} a {self.df['date'].max()}")
                return True
            else:
                print("❌ Falha ao carregar dados fake")
                return False
        except Exception as e:
            print(f"❌ Erro ao testar dados fake: {e}")
            return False
    
    def _get_default_metrics(self):
        """Retorna métricas padrão caso não consiga carregar dados"""
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
            ("Homepage - Empresa XYZ", "/", 8500, 6500, 145.2),
            ("Produtos - Empresa XYZ", "/produtos", 7200, 5800, 135.8),
            ("Blog - Empresa XYZ", "/blog", 6800, 5200, 155.7),
            ("Sobre Nós - Empresa XYZ", "/sobre", 6200, 4800, 125.2),
            ("Contato - Empresa XYZ", "/contato", 5800, 4500, 115.4),
            ("Serviços - Empresa XYZ", "/servicos", 5400, 4200, 140.3),
            ("Preços - Empresa XYZ", "/precos", 5000, 3900, 150.2),
            ("Portfolio - Empresa XYZ", "/portfolio", 4600, 3600, 160.4),
            ("FAQ - Empresa XYZ", "/faq", 4200, 3300, 130.8),
            ("Depoimentos - Empresa XYZ", "/depoimentos", 3800, 3000, 125.6)
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
    
    def _get_default_device_data(self):
        """Retorna dados de dispositivos padrão"""
        return pd.DataFrame([
            {'device': 'desktop', 'users': 8500, 'sessions': 12000, 'pageviews': 24000},
            {'device': 'mobile', 'users': 5500, 'sessions': 8000, 'pageviews': 16000},
            {'device': 'tablet', 'users': 1000, 'sessions': 1400, 'pageviews': 2800}
        ])
