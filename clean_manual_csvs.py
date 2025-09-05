#!/usr/bin/env python3
"""
Limpeza e Padronização de CSVs Manuais
Script para corrigir problemas de formatação nos CSVs
"""

import os
import pandas as pd
import sys

def clean_csv_file(filepath):
    """Limpa e padroniza um arquivo CSV"""
    try:
        print(f"🧹 Limpando: {os.path.basename(filepath)}")
        
        # Tentar diferentes encodings
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv(filepath, encoding=encoding)
                print(f"   ✅ Encoding: {encoding}")
                break
            except:
                continue
        
        if df is None:
            print(f"   ❌ Não foi possível ler o arquivo")
            return False
        
        # Limpar dados
        print(f"   📊 Dados originais: {len(df)} linhas, {len(df.columns)} colunas")
        
        # Remover linhas completamente vazias
        df = df.dropna(how='all')
        
        # Remover colunas completamente vazias
        df = df.dropna(axis=1, how='all')
        
        # Limpar espaços em branco nas colunas de texto
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        # Remover linhas com valores vazios ou 'nan'
        df = df[df.astype(str).ne('nan').all(axis=1)]
        
        print(f"   📊 Dados limpos: {len(df)} linhas, {len(df.columns)} colunas")
        print(f"   📋 Colunas: {list(df.columns)}")
        
        # Salvar arquivo limpo
        backup_path = filepath + '.backup'
        clean_path = filepath + '.clean'
        
        # Fazer backup do original
        try:
            df_original = pd.read_csv(filepath, encoding='utf-8')
        except:
            df_original = pd.read_csv(filepath, encoding='latin-1')
        df_original.to_csv(backup_path, index=False, encoding='utf-8')
        
        # Salvar versão limpa
        df.to_csv(clean_path, index=False, encoding='utf-8')
        
        print(f"   💾 Backup salvo: {os.path.basename(backup_path)}")
        print(f"   💾 Limpo salvo: {os.path.basename(clean_path)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🧹 LIMPEZA DE CSVs MANUAIS")
    print("=" * 40)
    
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
    for file in files:
        print(f"   - {file}")
    
    print("\n🧹 Iniciando limpeza...")
    
    success_count = 0
    total_count = len(files)
    
    for file in files:
        filepath = os.path.join(manual_dir, file)
        if clean_csv_file(filepath):
            success_count += 1
        print()
    
    print(f"📈 RESULTADO: {success_count}/{total_count} CSVs limpos")
    
    if success_count > 0:
        print("\n✅ Limpeza concluída!")
        print("📁 Arquivos criados:")
        print("   - *.backup (backup do original)")
        print("   - *.clean (versão limpa)")
        print("\n💡 Próximos passos:")
        print("   1. Revise os arquivos *.clean")
        print("   2. Renomeie para os nomes padrão se necessário")
        print("   3. Execute: python test_manual_csvs.py")
        print("   4. Execute: streamlit run streamlit_dashboard.py")
    else:
        print("\n❌ Nenhum CSV foi limpo com sucesso")

if __name__ == "__main__":
    main()
