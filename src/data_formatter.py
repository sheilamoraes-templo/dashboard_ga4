"""
Utilitários de Formatação para Dashboard GA4
Funções para formatação consistente de dados e métricas
"""

import pandas as pd
import numpy as np
from typing import Any, Dict, List, Optional, Union
import re

class DataFormatter:
    """Classe para formatação consistente de dados"""
    
    @staticmethod
    def format_number(value: Union[int, float, str], decimals: int = 0) -> str:
        """Formata números com separadores de milhares"""
        try:
            if pd.isna(value) or value == '':
                return "0"
            
            num = float(value)
            if decimals == 0:
                return f"{int(num):,}"
            else:
                return f"{num:,.{decimals}f}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def format_percentage(value: Union[int, float, str], decimals: int = 1) -> str:
        """Formata percentuais"""
        try:
            if pd.isna(value) or value == '':
                return "0%"
            
            num = float(value)
            # Se o valor está entre 0 e 1, converter para percentual
            if 0 <= num <= 1:
                return f"{num:.{decimals}%}"
            # Se o valor está entre 0 e 100, tratar como percentual
            elif 0 <= num <= 100:
                return f"{num:.{decimals}f}%"
            else:
                return f"{num:.{decimals}f}%"
        except (ValueError, TypeError):
            return "0%"
    
    @staticmethod
    def format_duration(seconds: Union[int, float, str]) -> str:
        """Formata duração em segundos para formato legível"""
        try:
            if pd.isna(seconds) or seconds == '':
                return "0s"
            
            sec = float(seconds)
            
            if sec < 60:
                return f"{sec:.1f}s"
            elif sec < 3600:
                minutes = sec / 60
                return f"{minutes:.1f}min"
            else:
                hours = sec / 3600
                return f"{hours:.1f}h"
        except (ValueError, TypeError):
            return "0s"
    
    @staticmethod
    def format_currency(value: Union[int, float, str], currency: str = "R$") -> str:
        """Formata valores monetários"""
        try:
            if pd.isna(value) or value == '':
                return f"{currency} 0,00"
            
            num = float(value)
            return f"{currency} {num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except (ValueError, TypeError):
            return f"{currency} 0,00"
    
    @staticmethod
    def format_date(date_value: Union[str, pd.Timestamp], format_type: str = "display") -> str:
        """Formata datas"""
        try:
            if pd.isna(date_value) or date_value == '':
                return "N/A"
            
            if isinstance(date_value, str):
                date_obj = pd.to_datetime(date_value)
            else:
                date_obj = date_value
            
            if format_type == "display":
                return date_obj.strftime("%d/%m/%Y")
            elif format_type == "short":
                return date_obj.strftime("%d/%m")
            elif format_type == "long":
                return date_obj.strftime("%d de %B de %Y")
            else:
                return date_obj.strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return "N/A"
    
    @staticmethod
    def format_large_number(value: Union[int, float, str]) -> str:
        """Formata números grandes com sufixos (K, M, B)"""
        try:
            if pd.isna(value) or value == '':
                return "0"
            
            num = float(value)
            
            if num >= 1_000_000_000:
                return f"{num/1_000_000_000:.1f}B"
            elif num >= 1_000_000:
                return f"{num/1_000_000:.1f}M"
            elif num >= 1_000:
                return f"{num/1_000:.1f}K"
            else:
                return f"{num:.0f}"
        except (ValueError, TypeError):
            return "0"
    
    @staticmethod
    def format_url(url: str, max_length: int = 50) -> str:
        """Formata URLs para exibição"""
        if not url or pd.isna(url):
            return "N/A"
        
        url_str = str(url)
        if len(url_str) <= max_length:
            return url_str
        
        return url_str[:max_length-3] + "..."
    
    @staticmethod
    def format_device_name(device: str) -> str:
        """Formata nomes de dispositivos"""
        if not device or pd.isna(device):
            return "N/A"
        
        device_map = {
            'desktop': '🖥️ Desktop',
            'mobile': '📱 Mobile',
            'tablet': '📱 Tablet',
            'smartphone': '📱 Smartphone',
            'unknown': '❓ Desconhecido'
        }
        
        device_lower = str(device).lower()
        return device_map.get(device_lower, f"📱 {device.title()}")
    
    @staticmethod
    def format_source_medium(source: str, medium: str) -> str:
        """Formata combinação source/medium"""
        if not source or pd.isna(source):
            source = "N/A"
        if not medium or pd.isna(medium):
            medium = "N/A"
        
        return f"{source} / {medium}"
    
    @staticmethod
    def format_page_title(page: str, max_length: int = 40) -> str:
        """Formata títulos de páginas"""
        if not page or pd.isna(page):
            return "N/A"
        
        page_str = str(page)
        
        # Remover protocolo se presente
        page_str = re.sub(r'^https?://', '', page_str)
        
        # Truncar se muito longo
        if len(page_str) > max_length:
            page_str = page_str[:max_length-3] + "..."
        
        return page_str

class MetricCalculator:
    """Classe para cálculos de métricas"""
    
    @staticmethod
    def calculate_growth_rate(current: float, previous: float) -> Dict[str, Any]:
        """Calcula taxa de crescimento"""
        if previous == 0:
            return {
                "rate": 0,
                "percentage": "0%",
                "trend": "neutral",
                "formatted": "0%"
            }
        
        rate = (current - previous) / previous
        percentage = rate * 100
        
        if rate > 0.05:  # > 5%
            trend = "up"
        elif rate < -0.05:  # < -5%
            trend = "down"
        else:
            trend = "neutral"
        
        return {
            "rate": rate,
            "percentage": f"{percentage:+.1f}%",
            "trend": trend,
            "formatted": f"{percentage:+.1f}%"
        }
    
    @staticmethod
    def calculate_conversion_rate(conversions: float, sessions: float) -> Dict[str, Any]:
        """Calcula taxa de conversão"""
        if sessions == 0:
            return {
                "rate": 0,
                "percentage": "0%",
                "formatted": "0%"
            }
        
        rate = conversions / sessions
        
        return {
            "rate": rate,
            "percentage": f"{rate:.2%}",
            "formatted": f"{rate:.2%}"
        }
    
    @staticmethod
    def calculate_engagement_score(pageviews: float, sessions: float, users: float) -> Dict[str, Any]:
        """Calcula score de engajamento"""
        if users == 0:
            return {
                "score": 0,
                "level": "Baixo",
                "formatted": "0.0"
            }
        
        # Fórmula simples de engajamento
        score = (pageviews / sessions) * (sessions / users)
        
        if score >= 3:
            level = "Alto"
        elif score >= 2:
            level = "Médio"
        else:
            level = "Baixo"
        
        return {
            "score": score,
            "level": level,
            "formatted": f"{score:.1f}"
        }

class DataValidator:
    """Classe para validação de dados"""
    
    @staticmethod
    def validate_date_range(start_date: str, end_date: str) -> Dict[str, Any]:
        """Valida range de datas"""
        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            if start > end:
                return {
                    "valid": False,
                    "error": "Data inicial maior que data final"
                }
            
            days_diff = (end - start).days
            if days_diff > 365:
                return {
                    "valid": False,
                    "error": "Range de datas muito grande (máximo 365 dias)"
                }
            
            return {
                "valid": True,
                "days": days_diff + 1
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Erro ao validar datas: {str(e)}"
            }
    
    @staticmethod
    def validate_numeric_range(value: float, min_val: float, max_val: float) -> bool:
        """Valida se valor está dentro do range"""
        return min_val <= value <= max_val
    
    @staticmethod
    def validate_percentage(value: float) -> bool:
        """Valida se valor é um percentual válido"""
        return 0 <= value <= 1 or 0 <= value <= 100

# Instâncias globais
data_formatter = DataFormatter()
metric_calculator = MetricCalculator()
data_validator = DataValidator()
