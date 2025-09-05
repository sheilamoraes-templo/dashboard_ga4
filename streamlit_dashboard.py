"""
Dashboard GA4 com Streamlit
Versão simplificada e funcional
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
import json
import sys

# Adicionar src ao path para importar módulos
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from data_processor import data_processor
    from data_formatter import data_formatter, metric_calculator
except ImportError as e:
    st.error(f"Erro ao importar módulos de processamento: {e}")
    st.stop()

# Configuração da página
st.set_page_config(
    page_title="Dashboard GA4",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.title("📊 Dashboard GA4 Analytics")
st.markdown("---")

# Sidebar para configurações
st.sidebar.title("⚙️ Configurações")

# Função para carregar dados dos CSVs com processamento
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_csv_data(filename, data_type=None):
    """Carrega e processa dados de um arquivo CSV"""
    try:
        # Verificar se é um arquivo manual primeiro
        manual_path = os.path.join("data", "manual", filename)
        if os.path.exists(manual_path):
            file_path = manual_path
            st.info(f"📁 Carregando CSV manual: {filename}")
        else:
            file_path = os.path.join("data", filename)
        
        if os.path.exists(file_path):
            # Carregar dados brutos
            df_raw = pd.read_csv(file_path)
            
            # Determinar tipo de dados se não especificado
            if data_type is None:
                data_type = _infer_data_type(filename)
            
            # Processar dados com a camada de tratamento
            df_processed = data_processor.process_dataframe(df_raw, data_type)
            
            st.success(f"✅ Dados carregados e processados: {filename}")
            return df_processed
        else:
            st.warning(f"⚠️ Arquivo não encontrado: {filename}")
            st.info(f"💡 Dica: Para CSVs manuais, salve em 'data/manual/' com o nome: {filename}")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar {filename}: {e}")
        return None

def _infer_data_type(filename):
    """Infere o tipo de dados baseado no nome do arquivo"""
    filename_lower = filename.lower()
    
    # Remover sufixo _manual se presente
    if '_manual' in filename_lower:
        filename_lower = filename_lower.replace('_manual', '')
    
    if 'kpis' in filename_lower or 'daily' in filename_lower:
        return 'kpis_daily'
    elif 'pages' in filename_lower or 'top' in filename_lower:
        return 'pages_top'
    elif 'device' in filename_lower:
        return 'devices'
    elif 'acquisition' in filename_lower or 'first' in filename_lower:
        return 'acquisition'
    elif 'video' in filename_lower:
        return 'video_events'
    else:
        return 'generic'

# Função para gerar dados simulados
def generate_fake_data(days=30):
    """Gera dados simulados para demonstração"""
    import random
    
    # Gerar datas
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Gerar dados realistas
    data = []
    for date in dates:
        users = random.randint(15, 45)
        sessions = random.randint(25, 65)
        pageviews = random.randint(100, 300)
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'users': users,
            'sessions': sessions,
            'pageviews': pageviews,
            'avg_session_duration': round(random.uniform(200, 800), 2),
            'bounce_rate': round(random.uniform(0.2, 0.6), 4)
        })
    
    return pd.DataFrame(data)

# Função para obter métricas básicas com formatação
def get_basic_metrics(df):
    """Calcula métricas básicas do DataFrame com formatação"""
    if df is None or df.empty:
        return None
    
    metrics = {}
    
    # Verificar quais colunas existem e calcular métricas correspondentes
    if 'users' in df.columns:
        # Garantir que é numérico
        users_data = pd.to_numeric(df['users'], errors='coerce').fillna(0)
        total_users = users_data.sum()
        metrics['total_users'] = {
            'value': total_users,
            'formatted': data_formatter.format_number(total_users),
            'label': 'Total de Usuários'
        }
    elif 'user' in df.columns:
        users_data = pd.to_numeric(df['user'], errors='coerce').fillna(0)
        total_users = users_data.sum()
        metrics['total_users'] = {
            'value': total_users,
            'formatted': data_formatter.format_number(total_users),
            'label': 'Total de Usuários'
        }
    else:
        metrics['total_users'] = {
            'value': 0,
            'formatted': '0',
            'label': 'Total de Usuários'
        }
    
    if 'sessions' in df.columns:
        sessions_data = pd.to_numeric(df['sessions'], errors='coerce').fillna(0)
        total_sessions = sessions_data.sum()
        metrics['total_sessions'] = {
            'value': total_sessions,
            'formatted': data_formatter.format_number(total_sessions),
            'label': 'Total de Sessões'
        }
    else:
        metrics['total_sessions'] = {
            'value': 0,
            'formatted': '0',
            'label': 'Total de Sessões'
        }
    
    if 'pageviews' in df.columns:
        pageviews_data = pd.to_numeric(df['pageviews'], errors='coerce').fillna(0)
        total_pageviews = pageviews_data.sum()
        metrics['total_pageviews'] = {
            'value': total_pageviews,
            'formatted': data_formatter.format_number(total_pageviews),
            'label': 'Total de Pageviews'
        }
    else:
        metrics['total_pageviews'] = {
            'value': 0,
            'formatted': '0',
            'label': 'Total de Pageviews'
        }
    
    if 'avg_session_duration' in df.columns:
        # Tentar converter para numérico, removendo sufixos como 's'
        duration_data = df['avg_session_duration'].astype(str).str.replace('s', '').str.replace('%', '')
        duration_data = pd.to_numeric(duration_data, errors='coerce').fillna(0)
        avg_duration = duration_data.mean()
        metrics['avg_session_duration'] = {
            'value': avg_duration,
            'formatted': data_formatter.format_duration(avg_duration),
            'label': 'Duração Média de Sessão'
        }
    else:
        metrics['avg_session_duration'] = {
            'value': 0,
            'formatted': '0s',
            'label': 'Duração Média de Sessão'
        }
    
    if 'bounce_rate' in df.columns:
        # Tentar converter para numérico, removendo sufixos como '%'
        bounce_data = df['bounce_rate'].astype(str).str.replace('%', '')
        bounce_data = pd.to_numeric(bounce_data, errors='coerce').fillna(0)
        # Se os valores estão entre 0-100, converter para 0-1
        if bounce_data.max() > 1:
            bounce_data = bounce_data / 100
        bounce_rate = bounce_data.mean()
        metrics['bounce_rate'] = {
            'value': bounce_rate,
            'formatted': data_formatter.format_percentage(bounce_rate),
            'label': 'Taxa de Rejeição'
        }
    else:
        metrics['bounce_rate'] = {
            'value': 0,
            'formatted': '0%',
            'label': 'Taxa de Rejeição'
        }
    
    return metrics

# Carregar dados
st.sidebar.subheader("📁 Carregar Dados")

# Opção de dados
data_source = st.sidebar.selectbox(
    "Fonte de dados:",
    [
        "Dados Simulados",
        "CSV (kpis_daily)", 
        "CSV (pages_top)", 
        "CSV (devices)",
        "CSV Manual (kpis_daily)",
        "CSV Manual (pages_top)",
        "CSV Manual (devices)",
        "CSV Manual (first_user_acquisition)",
        "CSV Manual (video_events)",
        "CSV Manual (days_with_most_users)"
    ]
)

# Carregar dados baseado na seleção
if data_source == "CSV (kpis_daily)":
    df = load_csv_data("kpis_daily.csv")
elif data_source == "CSV (pages_top)":
    df = load_csv_data("pages_top.csv")
elif data_source == "CSV (devices)":
    df = load_csv_data("devices.csv")
elif data_source == "CSV Manual (kpis_daily)":
    df = load_csv_data("kpis_daily_manual.csv")
elif data_source == "CSV Manual (pages_top)":
    df = load_csv_data("pages_top_manual.csv")
elif data_source == "CSV Manual (devices)":
    df = load_csv_data("devices_manual.csv")
elif data_source == "CSV Manual (first_user_acquisition)":
    df = load_csv_data("first_user_acquisition_manual.csv")
elif data_source == "CSV Manual (video_events)":
    df = load_csv_data("video_events_manual.csv")
elif data_source == "CSV Manual (days_with_most_users)":
    df = load_csv_data("days_with_most_users_manual.csv")
else:
    days = st.sidebar.slider("Número de dias:", 7, 90, 30)
    df_raw = generate_fake_data(days)
    # Processar dados simulados também
    df = data_processor.process_dataframe(df_raw, "kpis_daily")
    st.info(f"📊 Usando dados simulados para {days} dias")

# Verificar se temos dados
if df is not None and not df.empty:
    st.success(f"✅ Dados carregados: {len(df)} registros")
    
    # Mostrar informações sobre CSVs manuais
    if "Manual" in data_source:
        st.info(f"📁 Carregando CSV manual: {data_source}")
        st.info("💡 Estes são dados reais do GA4 convertidos para o formato padrão")
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    
    metrics = get_basic_metrics(df)
    if metrics:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label=metrics['total_users']['label'],
                value=metrics['total_users']['formatted'],
                delta=None
            )
        
        with col2:
            st.metric(
                label=metrics['total_sessions']['label'],
                value=metrics['total_sessions']['formatted'],
                delta=None
            )
        
        with col3:
            st.metric(
                label=metrics['total_pageviews']['label'],
                value=metrics['total_pageviews']['formatted'],
                delta=None
            )
        
        with col4:
            st.metric(
                label=metrics['avg_session_duration']['label'],
                value=metrics['avg_session_duration']['formatted'],
                delta=None
            )
        
        with col5:
            st.metric(
                label=metrics['bounce_rate']['label'],
                value=metrics['bounce_rate']['formatted'],
                delta=None
            )
    
    # Resumo dos dados processados
    st.subheader("📋 Resumo dos Dados")
    
    # Determinar tipo de dados baseado na fonte selecionada
    if data_source == "Dados Simulados":
        data_type = "kpis_daily"
    else:
        data_type = _infer_data_type(data_source)
    
    # Obter resumo usando o processador
    data_summary = data_processor.get_data_summary(df, data_type)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"📊 **Total de Registros:** {data_summary['total_rows']:,}")
    
    with col2:
        st.info(f"📋 **Total de Colunas:** {data_summary['total_columns']}")
    
    with col3:
        st.info(f"🏷️ **Tipo de Dados:** {data_summary['data_type']}")
    
    # Mostrar range de datas se disponível
    if data_summary.get('date_range'):
        st.info(f"📅 **Período:** {data_summary['date_range']['start']} a {data_summary['date_range']['end']} ({data_summary['date_range']['days']} dias)")
    
    # Mostrar colunas disponíveis
    st.write("**Colunas disponíveis:**", ", ".join(data_summary['columns']))
    
    # Mostrar resumo numérico
    if data_summary.get('numeric_summary'):
        st.write("**Resumo numérico:**")
        for col, stats in data_summary['numeric_summary'].items():
            st.write(f"- **{col}:** Soma: {stats['sum']:,}, Média: {stats['mean']:.1f}, Min: {stats['min']:,}, Max: {stats['max']:,}")
    
    st.markdown("---")
    
    # Gráficos
    st.subheader("📊 Visualizações")
    
    # Gráfico de linha temporal
    if 'date' in df.columns:
        st.subheader("📈 Tendência Temporal")
        
        # Preparar dados para o gráfico
        df_chart = df.copy()
        df_chart['date'] = pd.to_datetime(df_chart['date'])
        
        # Criar gráfico de linha
        fig = go.Figure()
        
        if 'users' in df_chart.columns:
            fig.add_trace(go.Scatter(
                x=df_chart['date'],
                y=df_chart['users'],
                mode='lines+markers',
                name='Usuários',
                line=dict(color='#1f77b4')
            ))
        
        if 'sessions' in df_chart.columns:
            fig.add_trace(go.Scatter(
                x=df_chart['date'],
                y=df_chart['sessions'],
                mode='lines+markers',
                name='Sessões',
                line=dict(color='#ff7f0e')
            ))
        
        if 'pageviews' in df_chart.columns:
            fig.add_trace(go.Scatter(
                x=df_chart['date'],
                y=df_chart['pageviews'],
                mode='lines+markers',
                name='Pageviews',
                line=dict(color='#2ca02c')
            ))
        
        fig.update_layout(
            title="Métricas ao Longo do Tempo",
            xaxis_title="Data",
            yaxis_title="Valor",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("ℹ️ Dados não contêm coluna 'date' - gráfico temporal não disponível")
    
    # Gráfico de barras para páginas (se disponível)
    if 'page' in df.columns and 'pageviews' in df.columns:
        st.subheader("📄 Top Páginas")
        
        # Garantir que pageviews é numérico para ordenação
        df_pages = df.copy()
        df_pages['pageviews_numeric'] = pd.to_numeric(df_pages['pageviews'], errors='coerce').fillna(0)
        
        # Top 10 páginas
        top_pages = df_pages.nlargest(10, 'pageviews_numeric')
        
        fig = px.bar(
            top_pages,
            x='pageviews_numeric',
            y='page',
            orientation='h',
            title="Top 10 Páginas por Pageviews",
            color='pageviews_numeric',
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico de dispositivos (se disponível)
    if 'device' in df.columns and 'users' in df.columns:
        st.subheader("📱 Breakdown por Dispositivo")
        
        device_data = df.groupby('device')['users'].sum().reset_index()
        
        fig = px.pie(
            device_data,
            values='users',
            names='device',
            title="Distribuição de Usuários por Dispositivo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    elif 'device_category' in df.columns and 'users' in df.columns:
        st.subheader("📱 Breakdown por Dispositivo")
        
        device_data = df.groupby('device_category')['users'].sum().reset_index()
        
        fig = px.pie(
            device_data,
            values='users',
            names='device_category',
            title="Distribuição de Usuários por Dispositivo"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de dados
    st.subheader("📋 Dados Detalhados")
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        show_rows = st.selectbox("Mostrar linhas:", [10, 25, 50, 100, "Todas"])
    
    with col2:
        if st.button("🔄 Atualizar Dados"):
            st.cache_data.clear()
            st.rerun()
    
    # Mostrar tabela
    if show_rows == "Todas":
        st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df.head(show_rows), use_container_width=True)
    
    # Estatísticas
    st.subheader("📊 Estatísticas")
    st.write(df.describe())

else:
    st.error("❌ Nenhum dado disponível. Verifique os arquivos CSV na pasta 'data/' ou use dados simulados.")
    
    # Botão para gerar dados simulados
    if st.button("🎲 Gerar Dados Simulados"):
        df = generate_fake_data(30)
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>📊 Dashboard GA4 Analytics | Desenvolvido com Streamlit</p>
    <p>🔄 Dados atualizados automaticamente a cada 5 minutos</p>
</div>
""", unsafe_allow_html=True)
