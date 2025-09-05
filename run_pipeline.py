#!/usr/bin/env python3
"""
Script de Execução do Pipeline GA4
Interface simples para baixar dados do GA4
"""

import os
import sys
import subprocess
from datetime import datetime

def print_banner():
    """Exibe banner do pipeline"""
    print("=" * 60)
    print("🚀 PIPELINE GA4 - DOWNLOAD DE DADOS")
    print("=" * 60)
    print("📊 Métricas Principais, Top Páginas, Dispositivos, Vídeos")
    print("🎯 Primeiros Acessos, Comparações Semanais")
    print("=" * 60)

def check_credentials():
    """Verifica se as credenciais GA4 estão configuradas"""
    cred_file = "credenciais_google_ga4.json"
    if os.path.exists(cred_file):
        print(f"✅ Credenciais encontradas: {cred_file}")
        return True
    else:
        print(f"❌ Credenciais não encontradas: {cred_file}")
        print("📝 Configure as credenciais do Google Cloud Console")
        return False

def run_pipeline(days=30, mode="standard"):
    """Executa o pipeline GA4"""
    print(f"\n🚀 Executando pipeline GA4...")
    print(f"📅 Período: {days} dias")
    print(f"⚙️ Modo: {mode}")
    print("-" * 40)
    
    try:
        if mode == "quick":
            cmd = [sys.executable, "ga4_pipeline.py", "--quick"]
        elif mode == "full":
            cmd = [sys.executable, "ga4_pipeline.py", "--full", "--days", str(days)]
        else:
            cmd = [sys.executable, "ga4_pipeline.py", "--days", str(days)]
        
        # Executar pipeline
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Exibir resultado
        if result.stdout:
            print("📊 SAÍDA DO PIPELINE:")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ AVISOS/ERROS:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("\n✅ Pipeline executado com sucesso!")
            return True
        else:
            print(f"\n❌ Pipeline falhou (código: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao executar pipeline: {e}")
        return False

def show_menu():
    """Exibe menu de opções"""
    print("\n📋 OPÇÕES DO PIPELINE:")
    print("1. Pipeline Padrão (30 dias) - Métricas + Top Páginas + Dispositivos")
    print("2. Pipeline Rápido (7 dias) - Dados essenciais")
    print("3. Pipeline Completo (30 dias) - Todos os dados")
    print("4. Pipeline Customizado - Escolher período")
    print("5. Executar Dashboard")
    print("6. Sair")
    print("-" * 40)

def main():
    """Função principal"""
    print_banner()
    
    # Verificar credenciais
    if not check_credentials():
        print("\n❌ Configure as credenciais antes de continuar")
        return
    
    while True:
        show_menu()
        
        try:
            choice = input("🎯 Escolha uma opção (1-6): ").strip()
            
            if choice == "1":
                # Pipeline padrão
                success = run_pipeline(days=30, mode="standard")
                if success:
                    print("\n🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
                
            elif choice == "2":
                # Pipeline rápido
                success = run_pipeline(days=7, mode="quick")
                if success:
                    print("\n🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
                
            elif choice == "3":
                # Pipeline completo
                success = run_pipeline(days=30, mode="full")
                if success:
                    print("\n🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
                
            elif choice == "4":
                # Pipeline customizado
                try:
                    days = int(input("📅 Quantos dias? (1-90): "))
                    if 1 <= days <= 90:
                        success = run_pipeline(days=days, mode="standard")
                        if success:
                            print("\n🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
                    else:
                        print("❌ Período deve estar entre 1 e 90 dias")
                except ValueError:
                    print("❌ Digite um número válido")
                
            elif choice == "5":
                # Executar dashboard
                print("\n🌐 Iniciando dashboard Streamlit...")
                try:
                    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_dashboard.py"])
                except KeyboardInterrupt:
                    print("\n👋 Dashboard encerrado")
                except Exception as e:
                    print(f"❌ Erro ao executar dashboard: {e}")
                
            elif choice == "6":
                # Sair
                print("\n👋 Encerrando pipeline GA4...")
                break
                
            else:
                print("❌ Opção inválida. Escolha entre 1-6.")
            
            if choice in ["1", "2", "3", "4"]:
                input("\n⏸️ Pressione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Encerrando pipeline GA4...")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()
