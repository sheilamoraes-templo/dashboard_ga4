#!/usr/bin/env python3
"""
Verificador de CSVs Manuais no Dashboard
Script para verificar se os CSVs manuais estão sendo detectados pelo dashboard
"""

import os
import pandas as pd

def check_manual_csvs():
    """Verifica se os CSVs manuais estão disponíveis"""
    print("🔍 VERIFICADOR DE CSVs MANUAIS")
    print("=" * 50)
    
    manual_dir = "data/manual"
    
    if not os.path.exists(manual_dir):
        print(f"❌ Pasta {manual_dir} não existe")
        return False
    
    # Listar arquivos CSV manuais
    files = [f for f in os.listdir(manual_dir) if f.endswith('_manual.csv')]
    
    if not files:
        print(f"❌ Nenhum CSV manual encontrado em {manual_dir}")
        return False
    
    print(f"📁 CSVs manuais encontrados: {len(files)}")
    
    # Verificar cada arquivo
    available_csvs = []
    
    for file in files:
        filepath = os.path.join(manual_dir, file)
        try:
            df = pd.read_csv(filepath)
            print(f"✅ {file}: {len(df)} linhas, {len(df.columns)} colunas")
            available_csvs.append(file)
        except Exception as e:
            print(f"❌ {file}: Erro - {e}")
    
    print(f"\n📊 CSVs manuais disponíveis: {len(available_csvs)}")
    
    # Mapear para opções do dashboard
    dashboard_options = {
        'kpis_daily_manual.csv': 'CSV Manual (kpis_daily)',
        'pages_top_manual.csv': 'CSV Manual (pages_top)',
        'devices_manual.csv': 'CSV Manual (devices)',
        'first_user_acquisition_manual.csv': 'CSV Manual (first_user_acquisition)',
        'video_events_manual.csv': 'CSV Manual (video_events)',
        'days_with_most_users_manual.csv': 'CSV Manual (days_with_most_users)'
    }
    
    print(f"\n🎯 Opções disponíveis no dashboard:")
    for csv_file in available_csvs:
        if csv_file in dashboard_options:
            print(f"   ✅ {dashboard_options[csv_file]}")
        else:
            print(f"   ⚠️ {csv_file} (não mapeado)")
    
    return len(available_csvs) > 0

def main():
    """Função principal"""
    success = check_manual_csvs()
    
    if success:
        print(f"\n✅ CSVs manuais estão disponíveis!")
        print(f"🌐 Execute o dashboard: streamlit run streamlit_dashboard.py")
        print(f"📋 No menu lateral, selecione as opções 'CSV Manual'")
        print(f"💡 Você verá dados reais do GA4 convertidos para o formato padrão")
    else:
        print(f"\n❌ Nenhum CSV manual disponível")
        print(f"💡 Execute: python convert_ga4_csvs_robust.py")

if __name__ == "__main__":
    main()
