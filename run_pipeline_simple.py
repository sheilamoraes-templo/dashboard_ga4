#!/usr/bin/env python3
"""
Comando de Execução - Pipeline GA4
Interface simples para executar o pipeline
"""

import os
import sys
import subprocess

def print_banner():
    """Exibe banner"""
    print("🚀 PIPELINE GA4 - COMANDO DE EXECUÇÃO")
    print("=" * 50)
    print("📊 Dados: Métricas, Páginas, Dispositivos, Vídeos")
    print("🎯 Primeiros Acessos, Comparações, Análise Temporal")
    print("=" * 50)

def run_simple_pipeline():
    """Executa pipeline simplificado"""
    print("\n📊 Executando pipeline simplificado...")
    try:
        result = subprocess.run([sys.executable, "simple_pipeline.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Pipeline executado com sucesso!")
            print("\n📁 Dados criados:")
            print("   - kpis_daily.csv (métricas principais)")
            print("   - pages_top.csv (top páginas)")
            print("   - devices.csv (breakdown por dispositivo)")
            print("   - first_user_acquisition.csv (primeiros acessos)")
            print("   - video_events.csv (eventos de vídeo)")
            print("   - weekly_comparison.csv (comparação semanal)")
            print("   - days_with_most_users.csv (dias com mais usuários)")
            
            print("\n🌐 Execute o dashboard:")
            print("   streamlit run streamlit_dashboard.py")
            print("   Acesse: http://localhost:8501")
            
            return True
        else:
            print(f"❌ Erro no pipeline: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar pipeline: {e}")
        return False

def run_dashboard():
    """Executa dashboard"""
    print("\n🌐 Iniciando dashboard Streamlit...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard encerrado")
    except Exception as e:
        print(f"❌ Erro ao executar dashboard: {e}")

def main():
    """Função principal"""
    print_banner()
    
    print("\n📋 OPÇÕES:")
    print("1. Executar Pipeline (criar dados)")
    print("2. Executar Dashboard")
    print("3. Pipeline + Dashboard")
    print("4. Sair")
    
    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-4): ").strip()
            
            if choice == "1":
                run_simple_pipeline()
                
            elif choice == "2":
                run_dashboard()
                
            elif choice == "3":
                if run_simple_pipeline():
                    input("\n⏸️ Pressione Enter para iniciar o dashboard...")
                    run_dashboard()
                
            elif choice == "4":
                print("\n👋 Encerrando...")
                break
                
            else:
                print("❌ Opção inválida. Escolha entre 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
