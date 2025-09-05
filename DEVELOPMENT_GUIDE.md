# 🛠️ Guia de Desenvolvimento - Dashboard GA4

## 🚀 **Início Rápido para Desenvolvedores**

### **1. Configuração do Ambiente**
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd dashboard_ga4

# Instale as dependências
pip install -r requirements.txt

# Execute o dashboard
python run_dashboard.py
```

### **2. Estrutura de Desenvolvimento**
```
dashboard_ga4/
├── streamlit_dashboard.py    # 🎯 ARQUIVO PRINCIPAL
├── run_dashboard.py          # 🚀 Script de execução
├── data/                     # 📊 Dados (CSVs)
├── src/                      # 🔧 Código fonte (referência)
└── requirements.txt          # 📦 Dependências
```

## 🔧 **Desenvolvimento do Dashboard**

### **Arquivo Principal: `streamlit_dashboard.py`**

#### **Estrutura do Código:**
```python
# 1. IMPORTS E CONFIGURAÇÃO
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard GA4",
    page_icon="📊",
    layout="wide"
)

# 3. FUNÇÕES AUXILIARES
def load_data_from_csv(filename):
    # Carregamento de dados
    pass

def get_basic_metrics(df):
    # Cálculo de métricas
    pass

def render_charts(df):
    # Renderização de gráficos
    pass

# 4. INTERFACE PRINCIPAL
def main():
    # Sidebar
    # Métricas principais
    # Gráficos
    # Tabelas
    pass

# 5. EXECUÇÃO
if __name__ == "__main__":
    main()
```

## 📊 **Adicionando Novos Tipos de Dados**

### **1. Adicionar Novo CSV**
```python
# Em streamlit_dashboard.py, adicione na sidebar:
if st.sidebar.selectbox("Fonte de Dados", ["kpis_daily", "pages_top", "novo_tipo"]):
    df = load_data_from_csv("novo_tipo.csv")
```

### **2. Criar Função de Carregamento**
```python
def load_novo_tipo_data():
    """Carrega dados do novo tipo"""
    try:
        df = pd.read_csv("data/novo_tipo.csv")
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return None
```

### **3. Adicionar Visualizações**
```python
def render_novo_tipo_charts(df):
    """Renderiza gráficos específicos para o novo tipo"""
    if 'coluna_x' in df.columns and 'coluna_y' in df.columns:
        fig = px.scatter(df, x='coluna_x', y='coluna_y')
        st.plotly_chart(fig, use_container_width=True)
```

## 🎨 **Personalizando a Interface**

### **1. Modificar Sidebar**
```python
# Em main(), na seção sidebar:
st.sidebar.header("📊 Configurações")
data_source = st.sidebar.selectbox(
    "Fonte de Dados",
    ["CSV Real", "Dados Simulados", "GA4 API"]
)
```

### **2. Adicionar Filtros**
```python
# Filtro por período
if 'date' in df.columns:
    date_range = st.sidebar.date_input(
        "Período",
        value=(df['date'].min(), df['date'].max()),
        min_value=df['date'].min(),
        max_value=df['date'].max()
    )
```

### **3. Personalizar Métricas**
```python
# Métricas customizadas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Usuários Únicos", f"{total_users:,}")
with col2:
    st.metric("Sessões", f"{total_sessions:,}")
```

## 📈 **Criando Novos Gráficos**

### **1. Gráfico de Linha**
```python
def create_line_chart(df, x_col, y_col, title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        name=y_col
    ))
    fig.update_layout(title=title)
    return fig
```

### **2. Gráfico de Barras**
```python
def create_bar_chart(df, x_col, y_col, title):
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    return fig
```

### **3. Gráfico de Pizza**
```python
def create_pie_chart(df, names_col, values_col, title):
    fig = px.pie(df, names=names_col, values=values_col, title=title)
    return fig
```

## 🔄 **Sistema de Cache**

### **Como Funciona:**
```python
@st.cache_data(ttl=300)  # Cache por 5 minutos
def load_data_with_cache(filename):
    return pd.read_csv(f"data/{filename}")
```

### **Limpar Cache:**
```python
# No código ou via interface
st.cache_data.clear()
```

## 🐛 **Debug e Troubleshooting**

### **1. Verificar Dados**
```python
# Adicionar debug info
st.write("Debug Info:")
st.write(f"Shape: {df.shape}")
st.write(f"Columns: {df.columns.tolist()}")
st.write(f"Data types: {df.dtypes}")
```

### **2. Tratar Erros**
```python
try:
    df = pd.read_csv("data/arquivo.csv")
except FileNotFoundError:
    st.error("Arquivo não encontrado!")
    return None
except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
    return None
```

### **3. Validação de Dados**
```python
def validate_dataframe(df):
    """Valida se o DataFrame tem a estrutura esperada"""
    required_columns = ['date', 'users', 'sessions']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.warning(f"Colunas ausentes: {missing_columns}")
        return False
    
    return True
```

## 📦 **Adicionando Dependências**

### **1. Atualizar requirements.txt**
```bash
# Adicionar nova dependência
pip install nova-dependencia
pip freeze >> requirements.txt
```

### **2. Dependências Comuns**
```python
# Para análise de dados
pandas>=2.0.0
numpy>=1.24.0

# Para visualização
plotly>=5.0.0
matplotlib>=3.7.0

# Para web scraping
requests>=2.32.0
beautifulsoup4>=4.12.0

# Para machine learning
scikit-learn>=1.3.0
```

## 🚀 **Deploy e Produção**

### **1. Streamlit Cloud**
```yaml
# requirements.txt deve estar na raiz
# streamlit_dashboard.py deve estar na raiz
# Pasta data/ deve estar incluída
```

### **2. Docker**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "streamlit_dashboard.py"]
```

### **3. Variáveis de Ambiente**
```python
# .env
GA4_PROPERTY_ID=sua_propriedade
GA4_CREDENTIALS_PATH=credenciais_google_ga4.json
```

## 📋 **Checklist de Desenvolvimento**

### **Antes de Commitar:**
- [ ] Código testado localmente
- [ ] Dados de exemplo funcionando
- [ ] Interface responsiva
- [ ] Tratamento de erros implementado
- [ ] Documentação atualizada

### **Antes de Deploy:**
- [ ] requirements.txt atualizado
- [ ] Dados de produção testados
- [ ] Performance otimizada
- [ ] Cache configurado
- [ ] Logs implementados

## 🎯 **Boas Práticas**

### **1. Código Limpo**
```python
# ✅ Bom
def calculate_metrics(df):
    """Calcula métricas básicas do DataFrame"""
    if df is None or df.empty:
        return None
    # ... código

# ❌ Ruim
def calc(df):
    # ... código sem documentação
```

### **2. Tratamento de Erros**
```python
# ✅ Bom
try:
    df = pd.read_csv("data/file.csv")
except FileNotFoundError:
    st.error("Arquivo não encontrado")
    return None

# ❌ Ruim
df = pd.read_csv("data/file.csv")  # Pode quebrar
```

### **3. Performance**
```python
# ✅ Bom
@st.cache_data(ttl=300)
def expensive_operation():
    # ... operação custosa

# ❌ Ruim
def expensive_operation():
    # ... operação custosa executada sempre
```

## 📞 **Suporte e Recursos**

### **Documentação Oficial:**
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Docs](https://pandas.pydata.org/docs/)

### **Comunidade:**
- [Streamlit Community](https://discuss.streamlit.io/)
- [Plotly Community](https://community.plotly.com/)

---

**Desenvolvido com ❤️ para análise de dados GA4**
