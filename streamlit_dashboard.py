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

# Função para carregar dados dos CSVs
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_csv_data(filename):
    """Carrega dados de um arquivo CSV"""
    try:
        file_path = os.path.join("data", filename)
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            st.success(f"✅ Dados carregados: {filename}")
            return df
        else:
            st.warning(f"⚠️ Arquivo não encontrado: {filename}")
            return None
    except Exception as e:
        st.error(f"❌ Erro ao carregar {filename}: {e}")
        return None

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

# Função para obter métricas básicas
def get_basic_metrics(df):
    """Calcula métricas básicas do DataFrame"""
    if df is None or df.empty:
        return None
    
    metrics = {}
    
    # Verificar quais colunas existem e calcular métricas correspondentes
    if 'users' in df.columns:
        metrics['total_users'] = df['users'].sum()
    elif 'user' in df.columns:
        metrics['total_users'] = df['user'].sum()
    else:
        metrics['total_users'] = 0
    
    if 'sessions' in df.columns:
        metrics['total_sessions'] = df['sessions'].sum()
    else:
        metrics['total_sessions'] = 0
    
    if 'pageviews' in df.columns:
        metrics['total_pageviews'] = df['pageviews'].sum()
    else:
        metrics['total_pageviews'] = 0
    
    if 'avg_session_duration' in df.columns:
        metrics['avg_session_duration'] = df['avg_session_duration'].mean()
    else:
        metrics['avg_session_duration'] = 0
    
    if 'bounce_rate' in df.columns:
        metrics['avg_bounce_rate'] = df['bounce_rate'].mean()
    else:
        metrics['avg_bounce_rate'] = 0
    
    return metrics

# Carregar dados
st.sidebar.subheader("📁 Carregar Dados")

# Opção de dados
data_source = st.sidebar.selectbox(
    "Fonte de dados:",
    ["CSV (kpis_daily)", "Dados Simulados", "CSV (pages_top)", "CSV (devices)"]
)

# Carregar dados baseado na seleção
if data_source == "CSV (kpis_daily)":
    df = load_csv_data("kpis_daily.csv")
elif data_source == "CSV (pages_top)":
    df = load_csv_data("pages_top.csv")
elif data_source == "CSV (devices)":
    df = load_csv_data("devices.csv")
else:
    days = st.sidebar.slider("Número de dias:", 7, 90, 30)
    df = generate_fake_data(days)
    st.info(f"📊 Usando dados simulados para {days} dias")

# Verificar se temos dados
if df is not None and not df.empty:
    st.success(f"✅ Dados carregados: {len(df)} registros")
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    
    metrics = get_basic_metrics(df)
    if metrics:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="👥 Total Usuários",
                value=f"{metrics['total_users']:,}",
                delta=None
            )
        
        with col2:
            st.metric(
                label="🔄 Total Sessões",
                value=f"{metrics['total_sessions']:,}",
                delta=None
            )
        
        with col3:
            st.metric(
                label="📄 Total Pageviews",
                value=f"{metrics['total_pageviews']:,}",
                delta=None
            )
        
        with col4:
            st.metric(
                label="⏱️ Duração Média",
                value=f"{metrics['avg_session_duration']:.1f}s",
                delta=None
            )
        
        with col5:
            st.metric(
                label="📉 Taxa de Rejeição",
                value=f"{metrics['avg_bounce_rate']:.1%}",
                delta=None
            )
    
    # Gráficos
    st.subheader("📊 Visualizações")
    
    # Mostrar informações sobre os dados
    st.info(f"📋 **Estrutura dos dados:** {list(df.columns)}")
    
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
        
        # Top 10 páginas
        top_pages = df.nlargest(10, 'pageviews')
        
        fig = px.bar(
            top_pages,
            x='pageviews',
            y='page',
            orientation='h',
            title="Top 10 Páginas por Pageviews",
            color='pageviews',
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
