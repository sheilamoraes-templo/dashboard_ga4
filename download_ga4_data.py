#!/usr/bin/env python3
"""
Comando Direto - Pipeline GA4
Execução rápida do pipeline sem menu interativo
"""

import sys
import os

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Execução direta do pipeline"""
    print("🚀 PIPELINE GA4 - EXECUÇÃO DIRETA")
    print("=" * 40)
    
    # Importar pipeline
    try:
        import ga4_pipeline
        pipeline = ga4_pipeline.GA4Pipeline()
        print("✅ Pipeline importado com sucesso")
    except ImportError as e:
        print(f"❌ Erro ao importar pipeline: {e}")
        return
    
    # Criar pipeline
    pipeline = ga4_pipeline.GA4Pipeline()
    
    # Executar pipeline padrão (30 dias)
    print("📊 Executando pipeline padrão (30 dias)...")
    success = pipeline.run_full_pipeline(days=30)
    
    if success:
        print("\n🎉 Pipeline executado com sucesso!")
        print("📁 Dados salvos na pasta 'data/'")
        print("🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
    else:
        print("\n❌ Pipeline falhou")
        print("🔧 Verifique as credenciais GA4 em 'credenciais_google_ga4.json'")

if __name__ == "__main__":
    main()
