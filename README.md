# 📊 Dashboard GA4 Analytics

Dashboard profissional para análise de dados do Google Analytics 4.

## 🎯 **Estratégia Atual: Streamlit (RECOMENDADO)**

**✅ FUNCIONANDO:** Dashboard Streamlit com dados reais dos CSVs

### **Executar Dashboard:**
```bash
# Opção 1: Script automático
python run_dashboard.py

# Opção 2: Comando direto
streamlit run streamlit_dashboard.py
```

**Acesse:** http://localhost:8501

### **Funcionalidades:**
- 📊 Métricas principais (usuários, sessões, pageviews)
- 📈 Gráficos interativos com Plotly
- 📁 Carregamento automático de CSVs
- 🔄 Cache inteligente (5 minutos)
- 📱 Interface responsiva

---

## 📋 **Estratégias Testadas**

### **✅ Estratégia 2: Streamlit (ATUAL)**
- **Status:** ✅ Funcionando
- **Vantagens:** Interface intuitiva, carregamento automático, gráficos nativos
- **Arquivo:** `streamlit_dashboard.py`

### **❌ Estratégia 1: Flask (PROBLEMAS)**
- **Status:** ❌ Problemas de inicialização
- **Problemas:** APIs não respondiam, complexidade desnecessária
- **Arquivos:** `app.py`, `templates/`, `static/` (mantidos para referência)

---

## 🚀 **Início Rápido**

1. **Instalar dependências:**
   ```bash
   pip install streamlit pandas plotly
   ```

2. **Executar dashboard:**
   ```bash
   python run_dashboard.py
   ```

3. **Acessar:** http://localhost:8501

4. **Selecionar dados:** Menu lateral → Escolher CSV ou dados simulados

---

## 📁 **Estrutura do Projeto**

```
dashboard_ga4/
├── streamlit_dashboard.py    # 🎯 Dashboard principal
├── run_dashboard.py          # 🚀 Script de inicialização
├── data/                     # 📊 CSVs com dados do GA4
│   ├── kpis_daily.csv
│   ├── pages_top.csv
│   ├── devices.csv
│   └── ...
├── src/                      # 🔧 Código Flask (referência)
├── templates/                # 🎨 Templates HTML (referência)
├── static/                   # 📱 Assets estáticos (referência)
├── requirements.txt          # 📦 Dependências
└── README_STREAMLIT.md       # 📖 Documentação detalhada
```

---

## 📊 **Dados Suportados**

O dashboard detecta automaticamente a estrutura dos CSVs:

- **kpis_daily.csv** - Dados temporais (usuários, sessões, pageviews)
- **pages_top.csv** - Top páginas por pageviews
- **devices.csv** - Breakdown por dispositivo
- **Dados simulados** - Para demonstração

---

## 🔧 **Desenvolvimento**

### **Próximos Passos:**
1. Melhorar formatação dos dados
2. Adicionar filtros por período
3. Integrar GA4 API para atualização automática
4. Exportar relatórios (PDF, Excel)
5. Dashboard mobile-friendly

### **Contribuir:**
- Edite `streamlit_dashboard.py` para funcionalidades
- Adicione CSVs na pasta `data/`
- Use Plotly para gráficos customizados

---

## 📈 **Resultado**

✅ **Dashboard funcionando** com dados reais
✅ **Interface intuitiva** e responsiva
✅ **Gráficos interativos** com Plotly
✅ **Estratégia bem-sucedida** - Streamlit é a solução!

**Desenvolvido com ❤️ usando Streamlit + Plotly + Pandas**