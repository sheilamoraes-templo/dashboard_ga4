import json
import pandas as pd
from datetime import datetime, timedelta, date
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension,
    Filter,
    FilterExpression,
    FilterExpressionList,
    OrderBy
)
from config.settings import GA4_PROPERTY_ID, GA4_CREDENTIALS_PATH
from src.cache_manager import cache_manager
from .fake_data_client import FakeDataClient
from .superstore_data_client import SuperstoreDataClient

class GA4Client:
    def __init__(self):
        """Inicializa o cliente GA4"""
        self.property_id = GA4_PROPERTY_ID
        self.fake_client = None  # Carregar apenas quando necessário
        self.superstore_client = None  # Carregar apenas quando necessário
        
        # Tentar inicializar cliente GA4 real
        try:
            self.client = BetaAnalyticsDataClient.from_service_account_json(GA4_CREDENTIALS_PATH)
            self.use_fake_data = False
            print("✅ Cliente GA4 real inicializado")
        except Exception as e:
            print(f"⚠️ Erro ao inicializar GA4 real: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            self.client = None
            self.use_fake_data = True
            self.superstore_client = SuperstoreDataClient()
        
    def get_basic_metrics(self, days=30):
        """Obtém métricas básicas dos últimos N dias"""
        # Se estiver usando dados fake ou se a conexão GA4 falhar
        if self.use_fake_data or self.client is None:
            if self.superstore_client is None:
                self.superstore_client = SuperstoreDataClient()
            print("🔄 Usando dataset Superstore para métricas básicas")
            return self.superstore_client.get_basic_metrics(days)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="bounceRate")
                ]
            )
            
            response = self.client.run_report(request)
            
            # Processar resposta
            data = {}
            for row in response.rows:
                for i, metric in enumerate(row.metric_values):
                    metric_name = request.metrics[i].name
                    data[metric_name] = metric.value
                    
            return data
            
        except Exception as e:
            print(f"Erro ao obter métricas básicas do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            if self.superstore_client is None:
                self.superstore_client = SuperstoreDataClient()
            return self.superstore_client.get_basic_metrics(days)
    
    def get_daily_metrics(self, days=30):
        """Obtém métricas diárias dos últimos N dias"""
        # Se estiver usando dados fake ou se a conexão GA4 falhar
        if self.use_fake_data or self.client is None:
            print("🔄 Usando dataset Superstore para métricas diárias")
            return self.superstore_client.get_daily_metrics(days)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews")
                ],
                dimensions=[Dimension(name="date")]
            )
            
            response = self.client.run_report(request)
            
            # Converter para DataFrame
            data = []
            for row in response.rows:
                data.append({
                    'date': row.dimension_values[0].value,
                    'users': int(row.metric_values[0].value),
                    'sessions': int(row.metric_values[1].value),
                    'pageviews': int(row.metric_values[2].value)
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter métricas diárias do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            return self.superstore_client.get_daily_metrics(days)
    
    def get_top_pages(self, days=30, limit=10):
        """Obtém páginas mais visitadas"""
        # Se estiver usando dados fake ou se a conexão GA4 falhar
        if self.use_fake_data or self.client is None:
            print("🔄 Usando dataset Superstore para páginas mais visitadas")
            return self.superstore_client.get_top_pages(days, limit)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="screenPageViews"),
                    Metric(name="totalUsers"),
                    Metric(name="averageSessionDuration")
                ],
                dimensions=[
                    Dimension(name="pageTitle"),
                    Dimension(name="pagePath")
                ],
                limit=limit
            )
            
            response = self.client.run_report(request)
            
            # Converter para DataFrame
            data = []
            for row in response.rows:
                data.append({
                    'page_title': row.dimension_values[0].value,
                    'page_path': row.dimension_values[1].value,
                    'pageviews': int(row.metric_values[0].value),
                    'users': int(row.metric_values[1].value),
                    'avg_duration': float(row.metric_values[2].value)
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter páginas mais visitadas do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            return self.superstore_client.get_top_pages(days, limit)
    
    def get_device_breakdown(self, days=30):
        """Obtém breakdown por dispositivo"""
        # Se estiver usando dados fake ou se a conexão GA4 falhar
        if self.use_fake_data or self.client is None:
            print("🔄 Usando dataset Superstore para breakdown por dispositivo")
            return self.superstore_client.get_device_breakdown(days)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions"),
                    Metric(name="screenPageViews")
                ],
                dimensions=[Dimension(name="deviceCategory")]
            )
            
            response = self.client.run_report(request)
            
            # Converter para DataFrame
            data = []
            for row in response.rows:
                data.append({
                    'device': row.dimension_values[0].value,
                    'users': int(row.metric_values[0].value),
                    'sessions': int(row.metric_values[1].value),
                    'pageviews': int(row.metric_values[2].value)
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter breakdown por dispositivo do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            return self.superstore_client.get_device_breakdown(days)
    
    def first_user_acquisition(self, days=30):
        """Obtém dados de aquisição de primeiro acesso"""
        if self.use_fake_data or self.client is None:
            print("🔄 Usando dataset Superstore para aquisição de primeiro acesso")
            return self.superstore_client.first_user_acquisition(days)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="totalUsers"),
                    Metric(name="sessions")
                ],
                dimensions=[
                    Dimension(name="firstUserSource"),
                    Dimension(name="firstUserMedium"),
                    Dimension(name="firstUserCampaignName")
                ],
                limit=1000
            )
            
            response = self.client.run_report(request)
            
            # Converter para DataFrame
            data = []
            for row in response.rows:
                data.append({
                    'source': row.dimension_values[0].value,
                    'medium': row.dimension_values[1].value,
                    'campaign': row.dimension_values[2].value,
                    'users': int(row.metric_values[0].value),
                    'sessions': int(row.metric_values[1].value)
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter dados de aquisição do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            return self.superstore_client.first_user_acquisition(days)
    
    def video_events(self, days=30):
        """Obtém eventos de vídeo"""
        if self.use_fake_data or self.client is None:
            print("🔄 Usando dataset Superstore para eventos de vídeo")
            if self.superstore_client is None:
                self.superstore_client = SuperstoreDataClient()
            return self.superstore_client.video_events(days)
        
        try:
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="eventCount")
                ],
                dimensions=[
                    Dimension(name="date"),
                    Dimension(name="eventName"),
                    Dimension(name="customEvent:video_title"),
                    Dimension(name="customEvent:video_percent")
                ],
                dimension_filter=FilterExpression(
                    filter=Filter(
                        field_name="eventName",
                        string_filter=Filter.StringFilter(
                            match_type=Filter.StringFilter.MatchType.CONTAINS,
                            value="video_"
                        )
                    )
                ),
                limit=10000
            )
            
            response = self.client.run_report(request)
            
            # Converter para DataFrame
            data = []
            for row in response.rows:
                data.append({
                    'date': row.dimension_values[0].value,
                    'event_name': row.dimension_values[1].value,
                    'video_title': row.dimension_values[2].value,
                    'video_percent': row.dimension_values[3].value,
                    'event_count': int(row.metric_values[0].value)
                })
            
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao obter eventos de vídeo do GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            if self.superstore_client is None:
                self.superstore_client = SuperstoreDataClient()
            return self.superstore_client.video_events(days)

    def test_connection(self):
        """Testa a conexão com GA4"""
        try:
            if self.use_fake_data or self.client is None:
                print("🔄 Testando dataset Superstore...")
                return self.superstore_client.test_connection()
            
            # Tenta obter dados básicos dos últimos 7 dias
            data = self.get_basic_metrics(days=7)
            if data:
                print("✅ Conexão com GA4 estabelecida com sucesso!")
                print(f"Dados dos últimos 7 dias: {data}")
                return True
            else:
                print("❌ Falha na conexão com GA4")
                print("🔄 Usando dataset Superstore como fallback")
                return self.superstore_client.test_connection()
        except Exception as e:
            print(f"❌ Erro ao testar conexão GA4: {e}")
            print("🔄 Usando dataset Superstore como fallback")
            return self.superstore_client.test_connection()

    # ---------- Novos métodos para catálogo de relatórios ----------
    
    def _build_filter_in(self, spec):
        """Constrói filtro IN para dimensões"""
        if not spec: 
            return None
        return FilterExpression(
            filter=Filter(
                field_name=spec["dimension"],
                in_list_filter=Filter.InListFilter(values=list(spec.get("values", [])))
            )
        )

    def _build_filter_contains(self, spec):
        """Constrói filtro CONTAINS para dimensões"""
        if not spec:
            return None
        return FilterExpression(
            filter=Filter(
                field_name=spec["dimension"],
                string_filter=Filter.StringFilter(
                    value=spec["contains"], 
                    match_type=Filter.StringFilter.MatchType.CONTAINS, 
                    case_sensitive=False
                )
            )
        )

    def _window(self, days: int):
        """Retorna tupla (start_date, end_date) para o período especificado"""
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        return start_date, end_date

    def _as_date(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Converte coluna para datetime se necessário"""
        if column in df.columns and df[column].dtype == 'object':
            try:
                df[column] = pd.to_datetime(df[column], errors='coerce')
            except Exception:
                pass
        return df

    def _run_with_cache(self, method_name: str, days: int, **kwargs) -> pd.DataFrame:
        """Executa método com cache para reduzir chamadas à API"""
        # Gerar chave de cache
        cache_params = {"days": days, **kwargs}
        cache_key = cache_manager.get_cache_key(method_name, cache_params)
        
        # Verificar se há cache válido (30 minutos)
        if cache_manager.is_cache_valid(cache_key, max_age_minutes=30):
            cached_data = cache_manager.get_cached_data(cache_key)
            if cached_data and "data" in cached_data:
                print(f"📦 Usando cache para {method_name}")
                return pd.DataFrame(cached_data["data"])
        
        # Executar método original
        print(f"🔄 Executando {method_name} via API...")
        method = getattr(self, method_name)
        result = method(days, **kwargs)
        
        # Salvar no cache
        if not result.empty:
            cache_manager.set_cached_data(cache_key, result.to_dict(orient="records"))
        
        return result

    def run_generic(self, days: int, dimensions: list, metrics: list,
                    filter_in: dict = None, filter_contains: dict = None,
                    order_by_metric: str = None, limit: int = 100000) -> pd.DataFrame:
        """Runner genérico com filtros e ordenação"""
        start, end = self._window(days)
        where = None
        
        # Combina filtros (AND) se ambos existirem
        f_in = self._build_filter_in(filter_in)
        f_ct = self._build_filter_contains(filter_contains)
        
        if f_in and f_ct:
            where = FilterExpression(
                and_group=FilterExpressionList(expressions=[f_in, f_ct])
            )
        else:
            where = f_in or f_ct

        rows, page_size, offset = [], min(limit, 100000), 0
        order_bys = []
        
        if order_by_metric:
            order_bys = [OrderBy(
                metric=OrderBy.MetricOrderBy(metric_name=order_by_metric), 
                desc=True
            )]

        while True:
            req = RunReportRequest(
                property=f"properties/{self.property_id}",
                dimensions=[Dimension(name=d) for d in dimensions],
                metrics=[Metric(name=m) for m in metrics],
                date_ranges=[DateRange(start_date=start, end_date=end)],
                limit=page_size, 
                offset=offset,
                dimension_filter=where, 
                order_bys=order_bys
            )
            
            resp = self.client.run_report(req)
            if not resp.rows: 
                break
                
            for r in resp.rows:
                row = {}
                for i, d in enumerate(dimensions):
                    row[d] = r.dimension_values[i].value
                for j, m in enumerate(metrics):
                    row[m] = r.metric_values[j].value
                rows.append(row)
                
            if len(resp.rows) < page_size or len(rows) >= limit: 
                break
            offset += page_size
            
        return pd.DataFrame(rows)

    def run_compare_periods(self, days: int, **kwargs):
        """Executa consulta comparando período atual vs anterior"""
        # Período atual: [today-days+1, today]
        # Período anterior: imediatamente anterior, mesmo tamanho
        cur = self.run_generic(days=days, **kwargs)
        
        # Desloca a janela para trás
        start_prev = (date.today() - timedelta(days=days*2)).isoformat()
        end_prev = (date.today() - timedelta(days=days)).isoformat()
        
        # Reusa o runner com datas específicas
        prev = self._run(start_prev, end_prev, kwargs["dimensions"], kwargs["metrics"], 
                        limit=kwargs.get("limit", 100000))
        return cur, prev

    def postprocess(self, key: str, df: pd.DataFrame) -> pd.DataFrame:
        """Pós-processamento de dados baseado na chave"""
        if df is None or df.empty:
            return df

        # NUMÉRICOS padronizados
        for c in df.columns:
            if c in ["totalUsers", "sessions", "screenPageViews", "eventCount", "averageSessionDuration"]:
                df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

        if key == "daily":
            df = self._as_date(df, "date")
            out = pd.DataFrame({
                "date": df["date"],
                "users": df["totalUsers"] if "totalUsers" in df else 0,
                "sessions": df["sessions"] if "sessions" in df else 0,
                "pageviews": df["screenPageViews"] if "screenPageViews" in df else 0,
            })
            return out.sort_values("date")

        if key == "pages":
            out = (df.groupby("pagePath", as_index=False)["screenPageViews"].sum()
                     .rename(columns={"pagePath": "page", "screenPageViews": "pageviews"})
                     .sort_values("pageviews", ascending=False))
            return out

        if key == "pages_compare":
            # Espera dois períodos já combinados fora (veremos na rota); aqui só garantimos nomes
            return df  # deixamos a rota/refresh compor o comparativo

        if key == "devices":
            out = df.rename(columns={"deviceCategory": "device", "totalUsers": "users"})
            out["users"] = pd.to_numeric(out["users"], errors="coerce").fillna(0)
            return out.groupby("device", as_index=False)["users"].sum()

        if key == "first_user":
            out = df.rename(columns={
                "firstUserSource": "source",
                "firstUserMedium": "medium",
                "firstUserCampaignName": "campaign",
                "totalUsers": "users"
            })
            out["users"] = pd.to_numeric(out["users"], errors="coerce").fillna(0)
            return out.sort_values("users", ascending=False)

        if key == "days_top":
            df = self._as_date(df, "date")
            out = df.rename(columns={"totalUsers": "users"})[["date", "users"]]
            return out.sort_values("users", ascending=False).head(30)

        if key == "weekday_heatmap":
            df = self._as_date(df, "date")
            if "totalUsers" in df:
                df = df.rename(columns={"totalUsers": "users"})
            df["dow"] = df["date"].dt.dayofweek  # 0=Seg ... 6=Dom
            df["week"] = df["date"].dt.isocalendar().week
            out = df.groupby(["week", "dow"], as_index=False)["users"].sum()
            # Também devolve versão "legível"
            out["day_name"] = out["dow"].map({0: "Seg", 1: "Ter", 2: "Qua", 3: "Qui", 4: "Sex", 5: "Sáb", 6: "Dom"})
            return out.sort_values(["week", "dow"])

        if key == "compare_sum":
            # Será montado fora (somatório cur vs prev); aqui só dizemos que é comparativo
            return df

        if key == "compare_avg_duration":
            return df

        return df

    def video_events_specific(self, days: int, event_names: list) -> pd.DataFrame:
        """Eventos de vídeo específicos por tipo"""
        start, end = self._window(days)
        ev_filter = FilterExpression(
            filter=Filter(
                field_name="eventName",
                in_list_filter=Filter.InListFilter(values=event_names)
            )
        )
        
        dims_base = ["date", "eventName"]
        mets = ["eventCount"]
        title_candidates = ["videoTitle", "customEvent:video_title", "customEvent:title"]
        percent_candidates = ["percent", "videoPercent", "customEvent:percent", "customEvent:video_percent"]

        for title_dim in title_candidates:
            for perc_dim in percent_candidates:
                try:
                    df = self._run(start, end, dims_base + [title_dim, perc_dim], mets, 
                                 limit=1_000_000, where=ev_filter)
                    if not df.empty:
                        df = self._as_date(df, "date")
                        df["event_count"] = pd.to_numeric(df["eventCount"], errors="coerce").fillna(0)
                        return df.rename(columns={
                            title_dim: "video_title",
                            perc_dim: "video_percent",
                            "eventName": "event_name"
                        })[["date", "event_name", "video_title", "video_percent", "event_count"]]
                except Exception:
                    continue
                    
        # Fallback sem título/percent
        df = self._run(start, end, ["date", "eventName"], mets, limit=1_000_000, where=ev_filter)
        if df.empty: 
            return pd.DataFrame(columns=["date", "event_name", "video_title", "video_percent", "event_count"])
            
        df = self._as_date(df, "date")
        df["event_count"] = pd.to_numeric(df["eventCount"], errors="coerce").fillna(0)
        df = df.rename(columns={"eventName": "event_name"})
        df["video_title"] = None
        df["video_percent"] = None
        return df[["date", "event_name", "video_title", "video_percent", "event_count"]]
