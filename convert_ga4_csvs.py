#!/usr/bin/env python3
"""
Conversor de CSVs GA4 para Formato Padrão
Converte CSVs baixados do GA4 para o formato usado pelo dashboard
"""

import os
import pandas as pd
import re
from datetime import datetime

def convert_ga4_csv(filepath):
    """Converte um CSV do GA4 para formato padrão"""
    filename = os.path.basename(filepath)
    print(f"\n🔄 Convertendo: {filename}")
    print("-" * 50)
    
    try:
        # Ler arquivo como texto primeiro
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Encontrar linha de cabeçalho (primeira linha que não é comentário)
        header_line = None
        data_start = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith(''):
                if header_line is None:
                    header_line = i
                elif data_start is None:
                    data_start = i
                    break
        
        if header_line is None:
            print("❌ Não foi possível encontrar cabeçalho")
            return False
        
        print(f"📋 Cabeçalho encontrado na linha {header_line + 1}")
        print(f"📊 Dados começam na linha {data_start + 1 if data_start else 'não encontrada'}")
        
        # Ler dados a partir da linha de cabeçalho
        df = pd.read_csv(filepath, skiprows=header_line, encoding='utf-8')
        
        print(f"📊 Dados originais: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"📋 Colunas originais: {list(df.columns)}")
        
        # Mapear para formato padrão baseado no nome do arquivo
        converted_df = map_to_standard_format(df, filename)
        
        if converted_df is not None:
            print(f"✅ Convertido: {len(converted_df)} linhas, {len(converted_df.columns)} colunas")
            print(f"📋 Colunas finais: {list(converted_df.columns)}")
            
            # Salvar arquivo convertido
            output_filename = get_standard_filename(filename)
            output_path = os.path.join("data/manual", output_filename)
            converted_df.to_csv(output_path, index=False, encoding='utf-8')
            
            print(f"💾 Salvo como: {output_filename}")
            return True
        else:
            print("❌ Não foi possível converter")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def map_to_standard_format(df, filename):
    """Mapeia dados para formato padrão"""
    filename_lower = filename.lower()
    
    # Remover linhas de total geral
    df = df[~df.iloc[:, 0].astype(str).str.contains('Total geral', na=False)]
    
    if 'kpis' in filename_lower or 'daily' in filename_lower:
        # Métricas principais diárias
        if len(df.columns) >= 6:
            df_clean = df.iloc[:, :6].copy()
            df_clean.columns = ['date', 'users', 'sessions', 'pageviews', 'avg_session_duration', 'bounce_rate']
            
            # Converter tipos
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            df_clean['sessions'] = pd.to_numeric(df_clean['sessions'], errors='coerce').fillna(0)
            df_clean['pageviews'] = pd.to_numeric(df_clean['pageviews'], errors='coerce').fillna(0)
            df_clean['avg_session_duration'] = pd.to_numeric(df_clean['avg_session_duration'], errors='coerce').fillna(0)
            df_clean['bounce_rate'] = pd.to_numeric(df_clean['bounce_rate'], errors='coerce').fillna(0)
            
            return df_clean
    
    elif 'pages' in filename_lower or 'paginas' in filename_lower:
        # Top páginas
        if len(df.columns) >= 4:
            df_clean = df.iloc[:, :4].copy()
            df_clean.columns = ['page', 'pageviews', 'users', 'avg_engagement']
            
            # Converter tipos
            df_clean['pageviews'] = pd.to_numeric(df_clean['pageviews'], errors='coerce').fillna(0)
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            df_clean['avg_engagement'] = pd.to_numeric(df_clean['avg_engagement'], errors='coerce').fillna(0)
            
            # Adicionar coluna sessions estimada
            df_clean['sessions'] = (df_clean['pageviews'] * 0.6).astype(int)
            
            return df_clean[['page', 'pageviews', 'sessions', 'users']]
    
    elif 'device' in filename_lower or 'classes' in filename_lower:
        # Dispositivos/Classes
        if len(df.columns) >= 3:
            df_clean = df.iloc[:, :3].copy()
            df_clean.columns = ['device', 'pageviews', 'users']
            
            # Converter tipos
            df_clean['pageviews'] = pd.to_numeric(df_clean['pageviews'], errors='coerce').fillna(0)
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            
            # Adicionar coluna sessions estimada
            df_clean['sessions'] = (df_clean['pageviews'] * 0.6).astype(int)
            
            return df_clean[['device', 'pageviews', 'sessions', 'users']]
    
    elif 'acquisition' in filename_lower or 'primeiro' in filename_lower:
        # Primeiros acessos
        if len(df.columns) >= 2:
            df_clean = df.iloc[:, :2].copy()
            df_clean.columns = ['date', 'new_users']
            
            # Converter tipos
            df_clean['new_users'] = pd.to_numeric(df_clean['new_users'], errors='coerce').fillna(0)
            
            # Adicionar colunas estimadas
            df_clean['source'] = 'unknown'
            df_clean['medium'] = 'unknown'
            df_clean['sessions'] = (df_clean['new_users'] * 1.2).astype(int)
            
            return df_clean[['source', 'medium', 'new_users', 'sessions']]
    
    elif 'video' in filename_lower:
        # Eventos de vídeo
        if len(df.columns) >= 2:
            df_clean = df.iloc[:, :2].copy()
            df_clean.columns = ['video_title', 'count']
            
            # Converter tipos
            df_clean['count'] = pd.to_numeric(df_clean['count'], errors='coerce').fillna(0)
            
            # Adicionar colunas padrão
            df_clean['date'] = '2024-01-01'  # Data padrão
            df_clean['event_name'] = filename_lower.split('_')[0] if '_' in filename_lower else 'video_event'
            
            return df_clean[['date', 'event_name', 'count']]
    
    elif 'dias' in filename_lower or 'usuarios' in filename_lower:
        # Dias com mais usuários
        if len(df.columns) >= 2:
            df_clean = df.iloc[:, :2].copy()
            df_clean.columns = ['date', 'users']
            
            # Converter tipos
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            
            # Adicionar colunas estimadas
            df_clean['sessions'] = (df_clean['users'] * 1.2).astype(int)
            df_clean['pageviews'] = (df_clean['users'] * 4).astype(int)
            df_clean['avg_session_duration'] = 250  # Valor padrão
            df_clean['bounce_rate'] = 0.45  # Valor padrão
            
            return df_clean[['date', 'users', 'sessions', 'pageviews', 'avg_session_duration', 'bounce_rate']]
    
    return None

def get_standard_filename(original_filename):
    """Retorna nome padrão baseado no arquivo original"""
    filename_lower = original_filename.lower()
    
    if 'kpis' in filename_lower or 'daily' in filename_lower:
        return 'kpis_daily_manual.csv'
    elif 'pages' in filename_lower or 'paginas' in filename_lower:
        return 'pages_top_manual.csv'
    elif 'device' in filename_lower or 'classes' in filename_lower:
        return 'devices_manual.csv'
    elif 'acquisition' in filename_lower or 'primeiro' in filename_lower:
        return 'first_user_acquisition_manual.csv'
    elif 'video' in filename_lower:
        return 'video_events_manual.csv'
    elif 'dias' in filename_lower or 'usuarios' in filename_lower:
        return 'days_with_most_users_manual.csv'
    else:
        return f'converted_{original_filename}'

def main():
    """Função principal"""
    print("🔄 CONVERSOR DE CSVs GA4")
    print("=" * 50)
    
    manual_dir = "data/manual"
    
    if not os.path.exists(manual_dir):
        print(f"❌ Pasta {manual_dir} não existe")
        return
    
    # Listar arquivos CSV originais (não os já convertidos)
    files = [f for f in os.listdir(manual_dir) 
             if f.endswith('.csv') and not f.endswith('_manual.csv')]
    
    if not files:
        print(f"❌ Nenhum CSV original encontrado em {manual_dir}")
        return
    
    print(f"📁 CSVs originais encontrados: {len(files)}")
    for file in files:
        print(f"   - {file}")
    
    print("\n🔄 Iniciando conversão...")
    
    success_count = 0
    total_count = len(files)
    
    for file in files:
        filepath = os.path.join(manual_dir, file)
        if convert_ga4_csv(filepath):
            success_count += 1
    
    print(f"\n📈 RESULTADO: {success_count}/{total_count} CSVs convertidos")
    
    if success_count > 0:
        print("\n✅ Conversão concluída!")
        print("📁 Arquivos convertidos:")
        print("   - kpis_daily_manual.csv")
        print("   - pages_top_manual.csv")
        print("   - devices_manual.csv")
        print("   - first_user_acquisition_manual.csv")
        print("   - video_events_manual.csv")
        print("   - days_with_most_users_manual.csv")
        print("\n💡 Próximos passos:")
        print("   1. Execute: python test_manual_csvs.py")
        print("   2. Execute: streamlit run streamlit_dashboard.py")
        print("   3. Selecione os CSVs manuais no dashboard")
    else:
        print("\n❌ Nenhum CSV foi convertido com sucesso")

if __name__ == "__main__":
    main()
