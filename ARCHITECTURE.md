# 🏗️ Arquitetura do Projeto Dashboard GA4

## 📋 **Visão Geral da Arquitetura**

O projeto evoluiu de uma arquitetura Flask complexa para uma **arquitetura Streamlit simplificada** que funciona de forma mais eficiente e confiável.

## 🎯 **Estratégia Atual: Streamlit-First**

### **Arquitetura Principal:**
```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT DASHBOARD                      │
│                     (streamlit_dashboard.py)               │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   Sidebar   │  │   Metrics   │  │   Charts    │         │
│  │  (Data      │  │   Display   │  │  (Plotly    │         │
│  │  Selection) │  │   (KPIs)    │  │  Interactive)│         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│                    DATA LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    CSVs     │  │   GA4 API   │  │   Fake      │         │
│  │  (Real      │  │  (Optional) │  │   Data      │         │
│  │   Data)     │  │             │  │  (Demo)     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 📁 **Estrutura Detalhada dos Arquivos**

### **🎯 ARQUIVOS PRINCIPAIS (ATIVOS)**

#### **Dashboard Streamlit**
- **`streamlit_dashboard.py`** - Dashboard principal funcional
  - Interface Streamlit com sidebar e métricas
  - Carregamento automático de CSVs
  - Gráficos interativos com Plotly
  - Cache inteligente (5 minutos)
  - Fallback para dados simulados

#### **Scripts de Execução**
- **`run_dashboard.py`** - Script de inicialização automática
  - Verificação de dependências
  - Criação automática da pasta `data/`
  - Execução do Streamlit
  - Interface amigável

#### **Documentação**
- **`README.md`** - Documentação principal atualizada
- **`README_STREAMLIT.md`** - Documentação detalhada do Streamlit

### **📊 DADOS E CACHE**

#### **Pasta `data/`**
```
data/
├── kpis_daily.csv          # ✅ Dados temporais principais
├── pages_top.csv           # ✅ Top páginas por pageviews  
├── devices.csv             # ✅ Breakdown por dispositivo
├── device_breakdown.csv    # ✅ Dados de dispositivos
├── first_user_acquisition.csv # ✅ Dados de aquisição
├── video_events.csv        # ✅ Eventos de vídeo
├── fake_ga4_data.csv       # ✅ Dados simulados para demo
├── cache/                  # 📦 Cache do sistema
└── *.parquet              # 📦 Versões otimizadas dos CSVs
```

### **🔧 CÓDIGO FONTE (REFERÊNCIA)**

#### **Pasta `src/` (Mantida para referência)**
```
src/
├── ga4_client.py           # 🔌 Cliente GA4 API (funcional)
├── cache_manager.py        # 📦 Gerenciador de cache
├── report_catalog.py       # 📋 Catálogo de relatórios
├── agent_llm.py           # 🤖 Agent com LLM
├── ai_analyzer.py         # 🧠 Análise com IA
├── automation.py          # ⚙️ Automação de relatórios
├── email_sender.py        # 📧 Envio de emails
├── slack_client.py        # 💬 Integração Slack
├── fake_data_client.py    # 🎭 Cliente de dados simulados
└── superstore_data_client.py # 📊 Cliente de dados de exemplo
```

### **🎨 INTERFACE FLASK (LEGACY)**

#### **Pasta `templates/` (Mantida para referência)**
```
templates/
├── dashboard_analytics.html # 🎨 Dashboard Flask principal
├── status_system.html      # 📊 Sistema de status
├── dashboard.html          # 🎨 Dashboard básico
├── dashboard_debug.html    # 🐛 Dashboard de debug
├── debug_dashboard.html    # 🐛 Debug avançado
├── test_csv.html          # 🧪 Teste de CSVs
└── test_simple.html       # 🧪 Teste simples
```

#### **Pasta `static/` (Mantida para referência)**
```
static/
└── js/
    └── status_system.js   # ⚡ Sistema de status JavaScript
```

### **⚙️ CONFIGURAÇÃO**

#### **Pasta `config/`**
```
config/
└── settings.py            # ⚙️ Configurações centralizadas
```

#### **Arquivos de Configuração**
- **`requirements.txt`** - Dependências Python atualizadas
- **`credenciais_google_ga4.json`** - Credenciais GA4 (não versionado)
- **`SLACK_SETUP.md`** - Documentação do Slack

### **🧪 TESTES E DEBUG**

#### **Arquivos de Teste**
```
├── test_analytics_dashboard.py  # 🧪 Teste do dashboard
├── test_app_simple.py           # 🧪 Teste da app simples
├── test_connection.py           # 🧪 Teste de conexão
├── test_ga4_connection.py      # 🧪 Teste GA4
├── test_system.py              # 🧪 Teste do sistema
├── test_frontend_debug.html     # 🐛 Debug frontend
└── test.csv                    # 📊 Dados de teste
```

## 🔄 **Fluxo de Dados**

### **1. Inicialização**
```
run_dashboard.py → streamlit_dashboard.py → Interface Streamlit
```

### **2. Carregamento de Dados**
```
Usuário seleciona fonte → Streamlit carrega → Pandas processa → Plotly visualiza
```

### **3. Fontes de Dados (em ordem de prioridade)**
1. **CSVs reais** (`data/*.csv`) - Dados do GA4
2. **GA4 API** (opcional) - Dados em tempo real
3. **Dados simulados** - Para demonstração

## 🎨 **Padrões de Design**

### **Streamlit Dashboard**
- **Sidebar**: Seleção de dados e configurações
- **Main Area**: Métricas principais e gráficos
- **Cache**: Sistema de cache inteligente
- **Responsive**: Interface adaptável

### **Tratamento de Dados**
- **Detecção automática** de colunas nos CSVs
- **Fallback robusto** para diferentes estruturas
- **Validação de dados** antes da visualização
- **Formatação inteligente** de métricas

## 🔧 **Dependências por Categoria**

### **Core (Essenciais)**
```python
streamlit==1.28.1      # Dashboard principal
pandas==2.1.3          # Manipulação de dados
plotly==5.17.0         # Gráficos interativos
```

### **GA4 Integration (Opcional)**
```python
google-analytics-data==0.18.0  # API GA4
google-auth==2.23.4            # Autenticação
```

### **Legacy Flask (Referência)**
```python
Flask==2.3.3           # Framework web
Flask-CORS==4.0.0      # CORS para APIs
```

### **Utilitários**
```python
python-dotenv==1.0.0   # Variáveis de ambiente
requests>=2.32.3       # Requisições HTTP
openpyxl==3.1.2        # Suporte Excel
```

## 🚀 **Estratégias de Execução**

### **Estratégia 1: Script Automático (RECOMENDADO)**
```bash
python run_dashboard.py
```
- ✅ Verificação automática de dependências
- ✅ Criação de pastas necessárias
- ✅ Interface amigável
- ✅ Tratamento de erros

### **Estratégia 2: Comando Direto**
```bash
streamlit run streamlit_dashboard.py
```
- ✅ Execução direta
- ✅ Controle total do Streamlit
- ⚠️ Requer verificação manual

## 📈 **Métricas de Sucesso**

### **✅ Funcionalidades Implementadas**
- Dashboard Streamlit funcional
- Carregamento automático de CSVs
- Gráficos interativos com Plotly
- Sistema de cache inteligente
- Interface responsiva
- Fallback para dados simulados

### **🔄 Próximos Passos**
1. Melhorar formatação dos dados
2. Adicionar filtros por período
3. Integrar GA4 API para atualização automática
4. Exportar relatórios (PDF, Excel)
5. Dashboard mobile-friendly

## 🎯 **Conclusão da Arquitetura**

A arquitetura atual é **simples, eficiente e funcional**:

- **Streamlit** como frontend principal
- **Pandas** para manipulação de dados
- **Plotly** para visualizações
- **CSVs** como fonte principal de dados
- **Cache** para performance
- **Fallback** para robustez

Esta arquitetura resolve os problemas da versão Flask e oferece uma base sólida para futuras expansões.
