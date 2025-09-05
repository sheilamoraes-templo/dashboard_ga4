#!/usr/bin/env python3
"""
Analisador de CSVs Manuais
Script para analisar problemas nos CSVs e sugerir correções
"""

import os
import pandas as pd

def analyze_csv_file(filepath):
    """Analisa um arquivo CSV e identifica problemas"""
    filename = os.path.basename(filepath)
    print(f"\n📊 Analisando: {filename}")
    print("-" * 50)
    
    try:
        # Tentar ler o arquivo
        df = pd.read_csv(filepath)
        print(f"✅ Arquivo lido com sucesso")
        print(f"📊 Dimensões: {len(df)} linhas x {len(df.columns)} colunas")
        print(f"📋 Colunas: {list(df.columns)}")
        
        # Mostrar primeiras linhas
        print(f"\n📄 Primeiras 3 linhas:")
        print(df.head(3).to_string())
        
        # Verificar valores nulos
        nulls = df.isnull().sum()
        if nulls.sum() > 0:
            print(f"\n⚠️ Valores nulos encontrados:")
            print(nulls[nulls > 0])
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        
        # Tentar ler como texto para ver o conteúdo
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:10]  # Primeiras 10 linhas
                print(f"\n📄 Conteúdo do arquivo (primeiras 10 linhas):")
                for i, line in enumerate(lines):
                    print(f"   {i+1}: {repr(line.strip())}")
        except:
            print("❌ Não foi possível ler o arquivo como texto")
        
        return False

def suggest_standard_format(filename):
    """Sugere formato padrão baseado no nome do arquivo"""
    filename_lower = filename.lower()
    
    suggestions = {
        'kpis': {
            'columns': ['date', 'users', 'sessions', 'pageviews', 'avg_session_duration', 'bounce_rate'],
            'example': '2024-01-01,150,200,800,250,0.45'
        },
        'pages': {
            'columns': ['page', 'pageviews', 'sessions', 'users'],
            'example': '/,1500,800,600'
        },
        'device': {
            'columns': ['device', 'users', 'sessions', 'pageviews'],
            'example': 'desktop,200,250,1200'
        },
        'acquisition': {
            'columns': ['source', 'medium', 'users', 'sessions'],
            'example': 'google,organic,100,120'
        },
        'video': {
            'columns': ['date', 'event_name', 'count'],
            'example': '2024-01-01,video_start,150'
        }
    }
    
    for key, suggestion in suggestions.items():
        if key in filename_lower:
            print(f"\n💡 Sugestão de formato para {filename}:")
            print(f"   Colunas: {suggestion['columns']}")
            print(f"   Exemplo: {suggestion['example']}")
            return suggestion
    
    print(f"\n💡 Formato genérico para {filename}:")
    print(f"   Use colunas descritivas e valores numéricos separados por vírgula")
    return None

def main():
    """Função principal"""
    print("🔍 ANALISADOR DE CSVs MANUAIS")
    print("=" * 50)
    
    manual_dir = "data/manual"
    
    if not os.path.exists(manual_dir):
        print(f"❌ Pasta {manual_dir} não existe")
        return
    
    # Listar arquivos CSV
    files = [f for f in os.listdir(manual_dir) if f.endswith('.csv')]
    
    if not files:
        print(f"❌ Nenhum CSV encontrado em {manual_dir}")
        return
    
    print(f"📁 CSVs encontrados: {len(files)}")
    
    success_count = 0
    total_count = len(files)
    
    for file in files:
        filepath = os.path.join(manual_dir, file)
        if analyze_csv_file(filepath):
            success_count += 1
        suggest_standard_format(file)
    
    print(f"\n📈 RESULTADO: {success_count}/{total_count} CSVs analisados com sucesso")
    
    if success_count < total_count:
        print("\n💡 CSVs que precisam de correção:")
        print("   1. Verifique se estão no formato CSV correto")
        print("   2. Use vírgulas como separadores")
        print("   3. Evite caracteres especiais nos nomes das colunas")
        print("   4. Use encoding UTF-8")
        print("\n🔧 Para corrigir:")
        print("   1. Abra os CSVs no Excel ou LibreOffice")
        print("   2. Salve como CSV (UTF-8)")
        print("   3. Ou use o script clean_manual_csvs.py")

if __name__ == "__main__":
    main()
