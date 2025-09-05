"""
Pipeline GA4 - Download e Processamento de Dados
Sistema completo para baixar dados específicos do GA4 e disponibilizar no dashboard
"""

import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import logging

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ga4_client import GA4Client
    from data_processor import data_processor
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("🔧 Verifique se os arquivos estão na pasta src/")
    sys.exit(1)

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GA4Pipeline:
    """Pipeline completo para download e processamento de dados GA4"""
    
    def __init__(self):
        self.ga4_client = None
        self.data_dir = "data"
        self.ensure_data_dir()
        
    def ensure_data_dir(self):
        """Garante que a pasta data existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"📁 Pasta {self.data_dir} criada")
    
    def initialize_ga4_client(self):
        """Inicializa o cliente GA4"""
        try:
            self.ga4_client = GA4Client()
            logger.info("✅ Cliente GA4 inicializado")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar GA4: {e}")
            return False
    
    def download_main_metrics(self, days=30):
        """Baixa métricas principais (usuários, sessões, pageviews, etc.)"""
        logger.info(f"📊 Baixando métricas principais para {days} dias...")
        
        try:
            # Baixar dados básicos
            metrics_dict = self.ga4_client.get_basic_metrics(days=days)
            
            if metrics_dict and isinstance(metrics_dict, dict):
                # Converter dict para DataFrame
                df = pd.DataFrame([metrics_dict])
                
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "kpis_daily")
                
                # Salvar CSV
                filename = "kpis_daily.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Métricas principais salvas: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de métricas principais encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar métricas principais: {e}")
            return False
    
    def download_top_pages(self, days=30, limit=50):
        """Baixa top páginas e links mais acessados"""
        logger.info(f"📄 Baixando top {limit} páginas para {days} dias...")
        
        try:
            # Baixar dados de páginas
            df = self.ga4_client.get_top_pages(days=days, limit=limit)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "pages_top")
                
                # Salvar CSV
                filename = "pages_top.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Top páginas salvas: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de páginas encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar top páginas: {e}")
            return False
    
    def download_device_breakdown(self, days=30):
        """Baixa breakdown por dispositivo"""
        logger.info(f"📱 Baixando breakdown por dispositivo para {days} dias...")
        
        try:
            # Baixar dados de dispositivos
            df = self.ga4_client.get_device_breakdown(days=days)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "devices")
                
                # Salvar CSV
                filename = "devices.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Breakdown por dispositivo salvo: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de dispositivos encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar breakdown por dispositivo: {e}")
            return False
    
    def download_first_user_acquisition(self, days=30):
        """Baixa dados de primeiros acessos (source/medium)"""
        logger.info(f"🎯 Baixando primeiros acessos para {days} dias...")
        
        try:
            # Baixar dados de aquisição
            df = self.ga4_client.get_first_user_acquisition(days=days)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "acquisition")
                
                # Salvar CSV
                filename = "first_user_acquisition.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Primeiros acessos salvos: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de primeiros acessos encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar primeiros acessos: {e}")
            return False
    
    def download_video_events(self, days=30):
        """Baixa eventos de vídeo (video_start, video_progress, video_complete)"""
        logger.info(f"🎬 Baixando eventos de vídeo para {days} dias...")
        
        try:
            # Baixar dados de eventos de vídeo
            df = self.ga4_client.get_video_events(days=days)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "video_events")
                
                # Salvar CSV
                filename = "video_events.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Eventos de vídeo salvos: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum evento de vídeo encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar eventos de vídeo: {e}")
            return False
    
    def download_weekly_comparison(self, weeks=4):
        """Baixa dados para comparação semanal"""
        logger.info(f"📅 Baixando comparação semanal para {weeks} semanas...")
        
        try:
            # Baixar dados semanais
            df = self.ga4_client.get_weekly_comparison(weeks=weeks)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "weekly_comparison")
                
                # Salvar CSV
                filename = "weekly_comparison.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Comparação semanal salva: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de comparação semanal encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar comparação semanal: {e}")
            return False
    
    def download_days_with_most_users(self, days=30):
        """Baixa dados dos dias com mais usuários"""
        logger.info(f"📈 Baixando dias com mais usuários para {days} dias...")
        
        try:
            # Baixar dados diários detalhados
            df = self.ga4_client.get_days_with_most_users(days=days)
            
            if df is not None and not df.empty:
                # Processar dados
                df_processed = data_processor.process_dataframe(df, "days_with_most_users")
                
                # Salvar CSV
                filename = "days_with_most_users.csv"
                filepath = os.path.join(self.data_dir, filename)
                df_processed.to_csv(filepath, index=False)
                
                logger.info(f"✅ Dias com mais usuários salvos: {filename} ({len(df_processed)} registros)")
                return True
            else:
                logger.warning("⚠️ Nenhum dado de dias com mais usuários encontrado")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao baixar dias com mais usuários: {e}")
            return False
    
    def run_full_pipeline(self, days=30):
        """Executa o pipeline completo"""
        logger.info("🚀 Iniciando pipeline completo de dados GA4...")
        
        # Inicializar cliente GA4
        if not self.initialize_ga4_client():
            logger.error("❌ Falha ao inicializar cliente GA4. Pipeline interrompido.")
            return False
        
        # Lista de downloads
        downloads = [
            ("Métricas Principais", lambda: self.download_main_metrics(days)),
            ("Top Páginas", lambda: self.download_top_pages(days)),
            ("Breakdown por Dispositivo", lambda: self.download_device_breakdown(days)),
            ("Primeiros Acessos", lambda: self.download_first_user_acquisition(days)),
            ("Eventos de Vídeo", lambda: self.download_video_events(days)),
            ("Comparação Semanal", lambda: self.download_weekly_comparison()),
            ("Dias com Mais Usuários", lambda: self.download_days_with_most_users(days))
        ]
        
        # Executar downloads
        success_count = 0
        total_count = len(downloads)
        
        for name, download_func in downloads:
            logger.info(f"📥 Executando: {name}")
            try:
                if download_func():
                    success_count += 1
                    logger.info(f"✅ {name} - Concluído")
                else:
                    logger.warning(f"⚠️ {name} - Falhou")
            except Exception as e:
                logger.error(f"❌ {name} - Erro: {e}")
        
        # Resumo final
        logger.info(f"🎉 Pipeline concluído: {success_count}/{total_count} downloads bem-sucedidos")
        
        if success_count > 0:
            logger.info("📊 Dados disponíveis no dashboard Streamlit!")
            logger.info("🌐 Execute: streamlit run streamlit_dashboard.py")
        
        return success_count > 0
    
    def run_quick_pipeline(self, days=7):
        """Executa pipeline rápido com dados essenciais"""
        logger.info("⚡ Iniciando pipeline rápido...")
        
        if not self.initialize_ga4_client():
            return False
        
        # Downloads essenciais
        essential_downloads = [
            ("Métricas Principais", lambda: self.download_main_metrics(days)),
            ("Top Páginas", lambda: self.download_top_pages(days)),
            ("Breakdown por Dispositivo", lambda: self.download_device_breakdown(days))
        ]
        
        success_count = 0
        for name, download_func in essential_downloads:
            if download_func():
                success_count += 1
        
        logger.info(f"⚡ Pipeline rápido concluído: {success_count}/{len(essential_downloads)} downloads")
        return success_count > 0

def main():
    """Função principal para execução do pipeline"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline GA4 - Download de Dados")
    parser.add_argument("--days", type=int, default=30, help="Número de dias para baixar (padrão: 30)")
    parser.add_argument("--quick", action="store_true", help="Executar pipeline rápido (7 dias)")
    parser.add_argument("--full", action="store_true", help="Executar pipeline completo")
    
    args = parser.parse_args()
    
    # Criar pipeline
    pipeline = GA4Pipeline()
    
    if args.quick:
        # Pipeline rápido
        success = pipeline.run_quick_pipeline(days=7)
    elif args.full:
        # Pipeline completo
        success = pipeline.run_full_pipeline(days=args.days)
    else:
        # Pipeline padrão (métricas principais + top páginas)
        logger.info("📊 Executando pipeline padrão...")
        if pipeline.initialize_ga4_client():
            success = (
                pipeline.download_main_metrics(args.days) and
                pipeline.download_top_pages(args.days) and
                pipeline.download_device_breakdown(args.days)
            )
        else:
            success = False
    
    if success:
        logger.info("🎉 Pipeline executado com sucesso!")
        logger.info("🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
    else:
        logger.error("❌ Pipeline falhou. Verifique as credenciais GA4.")

if __name__ == "__main__":
    main()
