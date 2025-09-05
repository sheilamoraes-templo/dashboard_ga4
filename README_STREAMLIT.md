# 📊 Dashboard GA4 Analytics - Streamlit Edition

Dashboard profissional para análise de dados do Google Analytics 4, desenvolvido com **Streamlit** para máxima simplicidade e eficiência.

## 🚀 **Nova Estratégia: Streamlit**

Após testes extensivos com Flask, migramos para **Streamlit** que oferece:
- ✅ **Funcionamento imediato** - Sem problemas de inicialização
- ✅ **Interface intuitiva** - Widgets nativos e responsivos
- ✅ **Carregamento automático de CSVs** - Dados reais do GA4
- ✅ **Gráficos interativos** - Plotly integrado
- ✅ **Cache inteligente** - Performance otimizada

## 📋 **Funcionalidades**

### **📊 Métricas Principais**
- Total de Usuários
- Total de Sessões  
- Total de Pageviews
- Duração Média de Sessão
- Taxa de Rejeição

### **📈 Visualizações**
- **Gráfico Temporal** - Tendências ao longo do tempo
- **Top Páginas** - Páginas mais acessadas
- **Breakdown por Dispositivo** - Desktop, Mobile, Tablet
- **Tabela de Dados** - Visualização completa
- **Estatísticas** - Resumo estatístico automático

### **📁 Fontes de Dados**
- **CSV (kpis_daily)** - Dados temporais do GA4
- **CSV (pages_top)** - Top páginas por pageviews
- **CSV (devices)** - Breakdown por dispositivo
- **Dados Simulados** - Para demonstração

## 🛠️ **Instalação e Uso**

### **Pré-requisitos**
```bash
pip install streamlit pandas plotly
```

### **Executar o Dashboard**
```bash
streamlit run streamlit_dashboard.py
```

**Acesse:** http://localhost:8501

## 📁 **Estrutura do Projeto**

```
dashboard_ga4/
├── streamlit_dashboard.py    # 🎯 Dashboard principal (Streamlit)
├── data/                    # 📊 CSVs com dados do GA4
│   ├── kpis_daily.csv
│   ├── pages_top.csv
│   ├── devices.csv
│   └── ...
├── src/                     # 🔧 Código fonte (Flask - mantido para referência)
├── templates/               # 🎨 Templates HTML (Flask - mantido para referência)
├── static/                  # 📱 Assets estáticos (Flask - mantido para referência)
└── requirements.txt         # 📦 Dependências
```

## 🔄 **Migração de Estratégias**

### **Estratégia 1: Flask (❌ Problemas)**
- Problemas de inicialização automática
- APIs não respondiam corretamente
- Complexidade desnecessária para o objetivo

### **Estratégia 2: Streamlit (✅ Sucesso)**
- Funcionamento imediato
- Interface intuitiva
- Carregamento automático de dados
- Gráficos interativos nativos

## 📊 **Dados Suportados**

O dashboard detecta automaticamente a estrutura dos CSVs e adapta as visualizações:

### **kpis_daily.csv**
```
date,users,sessions,pageviews
2025-08-06,31,65,635
2025-08-07,28,49,360
```

### **pages_top.csv**
```
page,pageviews
/,2870
/course/view.php,2255
```

### **devices.csv**
```
device,users
desktop,266
mobile,53
```

## 🎨 **Personalização**

### **Adicionar Novos CSVs**
1. Coloque o arquivo na pasta `data/`
2. Adicione a opção no menu lateral
3. O dashboard detectará automaticamente as colunas

### **Modificar Gráficos**
- Edite `streamlit_dashboard.py`
- Use Plotly para gráficos customizados
- Streamlit oferece widgets nativos

## 🔧 **Desenvolvimento**

### **Cache**
- Dados são cacheados por 5 minutos
- Use `st.cache_data.clear()` para limpar

### **Performance**
- Streamlit otimiza automaticamente
- Plotly oferece gráficos interativos
- Pandas para manipulação eficiente

## 📈 **Próximos Passos**

1. **Melhorar apresentação** - Formatação de dados
2. **Adicionar filtros** - Por período, dispositivo, etc.
3. **Integrar GA4 API** - Atualização automática
4. **Exportar relatórios** - PDF, Excel, etc.
5. **Dashboard responsivo** - Mobile-friendly

## 🎯 **Resultado**

✅ **Dashboard funcionando** com dados reais dos CSVs
✅ **Interface intuitiva** e responsiva  
✅ **Gráficos interativos** com Plotly
✅ **Carregamento automático** de dados
✅ **Estratégia bem-sucedida** - Streamlit é a solução!

---

**Desenvolvido com ❤️ usando Streamlit + Plotly + Pandas**
