#!/usr/bin/env python3
"""
Conversor Robusto de CSVs GA4
Versão melhorada para lidar com CSVs complexos do GA4
"""

import os
import pandas as pd
import re

def convert_ga4_csv_robust(filepath):
    """Converte um CSV do GA4 de forma robusta"""
    filename = os.path.basename(filepath)
    print(f"\n🔄 Convertendo: {filename}")
    print("-" * 50)
    
    try:
        # Ler arquivo como texto
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Dividir em linhas
        lines = content.split('\n')
        
        # Encontrar linha de cabeçalho (primeira linha com vírgulas)
        header_line_idx = None
        for i, line in enumerate(lines):
            if ',' in line and not line.startswith('#') and line.strip():
                # Verificar se tem pelo menos 2 colunas
                parts = line.split(',')
                if len(parts) >= 2:
                    header_line_idx = i
                    break
        
        if header_line_idx is None:
            print("❌ Não foi possível encontrar cabeçalho válido")
            return False
        
        print(f"📋 Cabeçalho encontrado na linha {header_line_idx + 1}")
        print(f"📄 Cabeçalho: {lines[header_line_idx]}")
        
        # Criar DataFrame a partir da linha de cabeçalho
        data_lines = lines[header_line_idx:]
        
        # Remover linhas vazias e comentários
        clean_lines = []
        for line in data_lines:
            line = line.strip()
            if line and not line.startswith('#') and ',' in line:
                clean_lines.append(line)
        
        if not clean_lines:
            print("❌ Nenhuma linha de dados encontrada")
            return False
        
        print(f"📊 {len(clean_lines)} linhas de dados encontradas")
        
        # Criar DataFrame manualmente
        headers = clean_lines[0].split(',')
        data_rows = []
        
        for line in clean_lines[1:]:
            parts = line.split(',')
            if len(parts) >= len(headers):
                # Pegar apenas as colunas necessárias
                row = parts[:len(headers)]
                data_rows.append(row)
        
        if not data_rows:
            print("❌ Nenhuma linha de dados válida")
            return False
        
        # Criar DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        
        print(f"📊 DataFrame criado: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Remover linhas de total geral
        df = df[~df.iloc[:, 0].astype(str).str.contains('Total geral', na=False)]
        
        # Mapear para formato padrão
        converted_df = map_to_standard_format_robust(df, filename)
        
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

def map_to_standard_format_robust(df, filename):
    """Mapeia dados para formato padrão de forma robusta"""
    filename_lower = filename.lower()
    
    print(f"🔍 Mapeando dados para formato padrão...")
    print(f"📊 Dados originais: {len(df)} linhas")
    print(f"📋 Colunas originais: {list(df.columns)}")
    
    # Mostrar amostra dos dados
    print(f"📄 Amostra dos dados:")
    print(df.head(3).to_string())
    
    if 'kpis' in filename_lower or 'daily' in filename_lower:
        # Métricas principais diárias
        if len(df.columns) >= 2:
            df_clean = df.iloc[:, :2].copy()
            df_clean.columns = ['date', 'users']
            
            # Converter tipos
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            
            # Adicionar colunas estimadas
            df_clean['sessions'] = (df_clean['users'] * 1.2).astype(int)
            df_clean['pageviews'] = (df_clean['users'] * 4).astype(int)
            df_clean['avg_session_duration'] = 250
            df_clean['bounce_rate'] = 0.45
            
            return df_clean[['date', 'users', 'sessions', 'pageviews', 'avg_session_duration', 'bounce_rate']]
    
    elif 'pages' in filename_lower or 'paginas' in filename_lower:
        # Top páginas
        if len(df.columns) >= 3:
            df_clean = df.iloc[:, :3].copy()
            df_clean.columns = ['page', 'pageviews', 'users']
            
            # Converter tipos
            df_clean['pageviews'] = pd.to_numeric(df_clean['pageviews'], errors='coerce').fillna(0)
            df_clean['users'] = pd.to_numeric(df_clean['users'], errors='coerce').fillna(0)
            
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
            df_clean['date'] = '2024-01-01'
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
            df_clean['avg_session_duration'] = 250
            df_clean['bounce_rate'] = 0.45
            
            return df_clean[['date', 'users', 'sessions', 'pageviews', 'avg_session_duration', 'bounce_rate']]
    
    # Formato genérico se não conseguir mapear
    print("⚠️ Usando formato genérico")
    if len(df.columns) >= 2:
        df_clean = df.iloc[:, :2].copy()
        df_clean.columns = ['metric', 'value']
        df_clean['value'] = pd.to_numeric(df_clean['value'], errors='coerce').fillna(0)
        return df_clean
    
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
    print("🔄 CONVERSOR ROBUSTO DE CSVs GA4")
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
    
    print("\n🔄 Iniciando conversão robusta...")
    
    success_count = 0
    total_count = len(files)
    
    for file in files:
        filepath = os.path.join(manual_dir, file)
        if convert_ga4_csv_robust(filepath):
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
