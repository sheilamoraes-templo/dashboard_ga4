# src/cache_manager.py
import os
import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

class CacheManager:
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self.ensure_cache_dir()
    
    def ensure_cache_dir(self):
        """Cria o diretório de cache se não existir"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def get_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Gera chave única para o cache baseada no endpoint e parâmetros"""
        key_data = {
            "endpoint": endpoint,
            "params": sorted(params.items())
        }
        return f"{endpoint}_{hash(json.dumps(key_data, sort_keys=True))}"
    
    def is_cache_valid(self, cache_key: str, max_age_minutes: int = 30) -> bool:
        """Verifica se o cache ainda é válido"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if not os.path.exists(cache_file):
            return False
        
        # Verificar idade do arquivo
        file_time = os.path.getmtime(cache_file)
        age_minutes = (time.time() - file_time) / 60
        
        return age_minutes <= max_age_minutes
    
    def get_cached_data(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """Recupera dados do cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        if not os.path.exists(cache_file):
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📦 Cache hit: {cache_key}")
                return data
        except Exception as e:
            print(f"❌ Erro ao ler cache {cache_key}: {e}")
            return None
    
    def set_cached_data(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Armazena dados no cache"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        
        try:
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "data": data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 Cache saved: {cache_key}")
        except Exception as e:
            print(f"❌ Erro ao salvar cache {cache_key}: {e}")
    
    def clear_cache(self, pattern: str = "*") -> None:
        """Limpa cache baseado em padrão"""
        import glob
        
        cache_files = glob.glob(os.path.join(self.cache_dir, f"{pattern}.json"))
        for cache_file in cache_files:
            try:
                os.remove(cache_file)
                print(f"🗑️ Cache removido: {os.path.basename(cache_file)}")
            except Exception as e:
                print(f"❌ Erro ao remover cache {cache_file}: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache"""
        cache_files = [f for f in os.listdir(self.cache_dir) if f.endswith('.json')]
        
        total_size = 0
        oldest_file = None
        newest_file = None
        
        for cache_file in cache_files:
            file_path = os.path.join(self.cache_dir, cache_file)
            file_size = os.path.getsize(file_path)
            file_time = os.path.getmtime(file_path)
            
            total_size += file_size
            
            if oldest_file is None or file_time < oldest_file[1]:
                oldest_file = (cache_file, file_time)
            
            if newest_file is None or file_time > newest_file[1]:
                newest_file = (cache_file, file_time)
        
        return {
            "total_files": len(cache_files),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "oldest_file": oldest_file[0] if oldest_file else None,
            "newest_file": newest_file[0] if newest_file else None
        }

# Instância global do cache
cache_manager = CacheManager()
