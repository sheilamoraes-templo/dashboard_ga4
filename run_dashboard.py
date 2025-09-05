#!/usr/bin/env python3
"""
Script de inicialização do Dashboard GA4 - Streamlit Edition
"""

import subprocess
import sys
import os

def main():
    print("🚀 Iniciando Dashboard GA4 - Streamlit Edition")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("streamlit_dashboard.py"):
        print("❌ Erro: streamlit_dashboard.py não encontrado!")
        print("   Execute este script na pasta do projeto.")
        sys.exit(1)
    
    # Verificar se a pasta data existe
    if not os.path.exists("data"):
        print("⚠️  Aviso: Pasta 'data' não encontrada!")
        print("   Criando pasta 'data'...")
        os.makedirs("data", exist_ok=True)
    
    # Verificar se há CSVs na pasta data
    csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
    if csv_files:
        print(f"✅ Encontrados {len(csv_files)} arquivos CSV:")
        for csv in csv_files:
            print(f"   📄 {csv}")
    else:
        print("ℹ️  Nenhum arquivo CSV encontrado na pasta 'data'")
        print("   O dashboard usará dados simulados.")
    
    print("\n🌐 Iniciando servidor Streamlit...")
    print("📊 Dashboard será aberto em: http://localhost:8501")
    print("🔄 Para parar: Ctrl+C")
    print("=" * 50)
    
    try:
        # Executar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_dashboard.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado pelo usuário.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
