"""
Camada de Tratamento e Padronização de Dados
Sistema robusto para processar CSVs do GA4 antes da visualização
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import re
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Processador principal de dados do GA4"""
    
    def __init__(self):
        self.column_mappings = self._get_column_mappings()
        self.data_validators = self._get_data_validators()
        self.formatters = self._get_formatters()
    
    def _get_column_mappings(self) -> Dict[str, Dict[str, str]]:
        """Mapeamentos de colunas para padronização"""
        return {
            'kpis_daily': {
                # Mapeamentos para dados temporais
                'date': ['date', 'data', 'dia', 'timestamp', 'created_at'],
                'users': ['users', 'user', 'usuarios', 'unique_users', 'total_users'],
                'sessions': ['sessions', 'sessao', 'sessoes', 'total_sessions'],
                'pageviews': ['pageviews', 'page_views', 'visualizacoes', 'total_pageviews'],
                'avg_session_duration': ['avg_session_duration', 'duracao_media', 'tempo_medio', 'session_duration'],
                'bounce_rate': ['bounce_rate', 'taxa_rejeicao', 'taxa_saida', 'exit_rate']
            },
            'pages_top': {
                'page': ['page', 'pagina', 'url', 'path', 'page_path'],
                'pageviews': ['pageviews', 'page_views', 'visualizacoes', 'views', 'hits']
            },
            'devices': {
                'device': ['device', 'dispositivo', 'device_category', 'device_type'],
                'users': ['users', 'user', 'usuarios', 'unique_users', 'total_users']
            },
            'acquisition': {
                'source': ['source', 'fonte', 'traffic_source'],
                'medium': ['medium', 'meio', 'traffic_medium'],
                'users': ['users', 'user', 'usuarios', 'unique_users']
            },
            'video_events': {
                'event_name': ['event_name', 'evento', 'event_type', 'action'],
                'count': ['count', 'total', 'quantidade', 'events', 'event_count']
            }
        }
    
    def _get_data_validators(self) -> Dict[str, Dict[str, Any]]:
        """Validadores de dados por tipo"""
        return {
            'date': {
                'type': 'datetime',
                'required': True,
                'format': ['%Y-%m-%d', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
            },
            'users': {
                'type': 'numeric',
                'min': 0,
                'max': 1000000,
                'required': True
            },
            'sessions': {
                'type': 'numeric',
                'min': 0,
                'max': 1000000,
                'required': True
            },
            'pageviews': {
                'type': 'numeric',
                'min': 0,
                'max': 10000000,
                'required': True
            },
            'avg_session_duration': {
                'type': 'numeric',
                'min': 0,
                'max': 3600,  # 1 hora máximo
                'required': False
            },
            'bounce_rate': {
                'type': 'numeric',
                'min': 0,
                'max': 1,  # 0-100% ou 0-1
                'required': False
            }
        }
    
    def _get_formatters(self) -> Dict[str, Dict[str, Any]]:
        """Formatadores de dados"""
        return {
            'date': {
                'format': '%Y-%m-%d',
                'display_format': '%d/%m/%Y'
            },
            'users': {
                'format': '{:,}',
                'suffix': ' usuários'
            },
            'sessions': {
                'format': '{:,}',
                'suffix': ' sessões'
            },
            'pageviews': {
                'format': '{:,}',
                'suffix': ' pageviews'
            },
            'avg_session_duration': {
                'format': '{:.1f}',
                'suffix': ' segundos'
            },
            'bounce_rate': {
                'format': '{:.1%}',
                'suffix': ''
            }
        }
    
    def process_dataframe(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """
        Processa um DataFrame aplicando padronização, validação e limpeza
        
        Args:
            df: DataFrame original
            data_type: Tipo de dados ('kpis_daily', 'pages_top', 'devices', etc.)
        
        Returns:
            DataFrame processado e padronizado (dados numéricos mantidos para cálculos)
        """
        if df is None or df.empty:
            logger.warning(f"DataFrame vazio para tipo {data_type}")
            return df
        
        logger.info(f"Processando DataFrame {data_type} com {len(df)} linhas")
        
        # 1. Padronizar colunas
        df_standardized = self._standardize_columns(df, data_type)
        
        # 2. Validar dados
        df_validated = self._validate_data(df_standardized, data_type)
        
        # 3. Limpar dados
        df_cleaned = self._clean_data(df_validated, data_type)
        
        # NOTA: Não formatamos os dados aqui para manter tipos numéricos para cálculos
        # A formatação será feita apenas na exibição
        
        logger.info(f"DataFrame processado: {len(df_cleaned)} linhas, {len(df_cleaned.columns)} colunas")
        return df_cleaned
    
    def _standardize_columns(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Padroniza nomes de colunas"""
        df_std = df.copy()
        
        if data_type not in self.column_mappings:
            logger.warning(f"Tipo de dados {data_type} não encontrado nos mapeamentos")
            return df_std
        
        mappings = self.column_mappings[data_type]
        
        # Mapear colunas existentes para nomes padronizados
        column_renames = {}
        for standard_name, possible_names in mappings.items():
            for possible_name in possible_names:
                if possible_name in df_std.columns:
                    column_renames[possible_name] = standard_name
                    break
        
        if column_renames:
            df_std = df_std.rename(columns=column_renames)
            logger.info(f"Colunas renomeadas: {column_renames}")
        
        return df_std
    
    def _validate_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Valida dados do DataFrame"""
        df_val = df.copy()
        
        if data_type not in self.column_mappings:
            return df_val
        
        mappings = self.column_mappings[data_type]
        
        for standard_name in mappings.keys():
            if standard_name in df_val.columns:
                validator = self.data_validators.get(standard_name, {})
                df_val = self._apply_validation(df_val, standard_name, validator)
        
        return df_val
    
    def _apply_validation(self, df: pd.DataFrame, column: str, validator: Dict[str, Any]) -> pd.DataFrame:
        """Aplica validação específica a uma coluna"""
        if column not in df.columns:
            return df
        
        # Validar tipo de dados
        if validator.get('type') == 'datetime':
            df[column] = pd.to_datetime(df[column], errors='coerce')
        elif validator.get('type') == 'numeric':
            df[column] = pd.to_numeric(df[column], errors='coerce')
        
        # Validar ranges
        if 'min' in validator:
            df[column] = df[column].clip(lower=validator['min'])
        if 'max' in validator:
            df[column] = df[column].clip(upper=validator['max'])
        
        # Verificar valores nulos em colunas obrigatórias
        if validator.get('required', False):
            null_count = df[column].isnull().sum()
            if null_count > 0:
                logger.warning(f"Coluna {column}: {null_count} valores nulos encontrados")
        
        return df
    
    def _clean_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Limpa dados do DataFrame"""
        df_clean = df.copy()
        
        # Remover linhas completamente vazias
        df_clean = df_clean.dropna(how='all')
        
        # Tratar valores nulos específicos por tipo
        if data_type == 'kpis_daily':
            # Para dados temporais, interpolar valores nulos
            numeric_cols = ['users', 'sessions', 'pageviews']
            for col in numeric_cols:
                if col in df_clean.columns:
                    df_clean[col] = df_clean[col].fillna(0)
            
            # Para métricas calculadas, usar média
            calc_cols = ['avg_session_duration', 'bounce_rate']
            for col in calc_cols:
                if col in df_clean.columns:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
        
        # Remover outliers extremos (valores > 3 desvios padrão)
        numeric_columns = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if col in df_clean.columns:
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                if std > 0:
                    df_clean = df_clean[abs(df_clean[col] - mean) <= 3 * std]
        
        return df_clean
    
    def _format_data(self, df: pd.DataFrame, data_type: str) -> pd.DataFrame:
        """Formata dados para exibição (DEPRECATED - não usar mais)"""
        # Esta função foi desabilitada para manter dados numéricos para cálculos
        # A formatação agora é feita apenas na exibição
        return df
    
    def get_data_summary(self, df: pd.DataFrame, data_type: str) -> Dict[str, Any]:
        """Retorna resumo dos dados processados"""
        if df is None or df.empty:
            return {"error": "DataFrame vazio"}
        
        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "data_type": data_type,
            "columns": list(df.columns),
            "date_range": None,
            "numeric_summary": {}
        }
        
        # Resumo de datas
        if 'date' in df.columns:
            try:
                dates = pd.to_datetime(df['date'])
                summary["date_range"] = {
                    "start": dates.min().strftime('%d/%m/%Y'),
                    "end": dates.max().strftime('%d/%m/%Y'),
                    "days": (dates.max() - dates.min()).days + 1
                }
            except:
                pass
        
        # Resumo numérico
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col in df.columns:
                summary["numeric_summary"][col] = {
                    "sum": df[col].sum(),
                    "mean": df[col].mean(),
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "null_count": df[col].isnull().sum()
                }
        
        return summary
    
    def create_sample_data(self, data_type: str, rows: int = 30) -> pd.DataFrame:
        """Cria dados de exemplo para demonstração"""
        if data_type == 'kpis_daily':
            dates = pd.date_range(start='2024-01-01', periods=rows, freq='D')
            return pd.DataFrame({
                'date': dates,
                'users': np.random.randint(20, 100, rows),
                'sessions': np.random.randint(30, 150, rows),
                'pageviews': np.random.randint(100, 500, rows),
                'avg_session_duration': np.random.uniform(200, 600, rows),
                'bounce_rate': np.random.uniform(0.3, 0.7, rows)
            })
        
        elif data_type == 'pages_top':
            pages = ['/', '/sobre', '/contato', '/produtos', '/blog']
            return pd.DataFrame({
                'page': np.random.choice(pages, rows),
                'pageviews': np.random.randint(10, 1000, rows)
            })
        
        elif data_type == 'devices':
            devices = ['desktop', 'mobile', 'tablet']
            return pd.DataFrame({
                'device': np.random.choice(devices, rows),
                'users': np.random.randint(10, 200, rows)
            })
        
        else:
            return pd.DataFrame()

# Instância global do processador
data_processor = DataProcessor()
