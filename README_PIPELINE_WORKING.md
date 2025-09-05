# 🚀 Pipeline GA4 - Versão Funcional

Sistema completo para criar dados específicos do GA4 e disponibilizar no dashboard Streamlit.

## ✅ **FUNCIONANDO AGORA!**

### **Comando Simples:**
```bash
python simple_pipeline.py
```

### **Interface Interativa:**
```bash
python run_pipeline_simple.py
```

## 📊 **Dados Criados**

### **✅ Métricas Principais**
- **kpis_daily.csv** - 31 dias de dados
- Usuários, Sessões, Pageviews
- Duração média de sessão
- Taxa de rejeição

### **✅ Top Páginas e Links**
- **pages_top.csv** - 20 páginas mais acessadas
- Pageviews, Sessões, Usuários por página
- Análise de conteúdo

### **✅ Breakdown por Dispositivo**
- **devices.csv** - Desktop, Mobile, Tablet
- Distribuição de usuários por dispositivo
- Métricas por categoria

### **✅ Primeiros Acessos**
- **first_user_acquisition.csv** - 7 fontes
- Google, Facebook, Instagram, LinkedIn
- Email, Direct, YouTube
- Novos usuários por fonte

### **✅ Eventos de Vídeo**
- **video_events.csv** - 9 eventos
- video_start, video_progress, video_complete
- Contagem por data

### **✅ Comparação Semanal**
- **weekly_comparison.csv** - 4 semanas
- Tendências semanais
- Comparação de performance

### **✅ Dias com Mais Usuários**
- **days_with_most_users.csv** - Top 10 dias
- Ranking diário
- Análise de picos

## 🚀 **Como Usar**

### **1. Execução Direta**
```bash
python simple_pipeline.py
```

### **2. Interface Interativa**
```bash
python run_pipeline_simple.py
```

### **3. Dashboard**
```bash
streamlit run streamlit_dashboard.py
```

## 📁 **Estrutura dos Dados**

```
data/
├── kpis_daily.csv                    # ✅ Métricas principais
├── pages_top.csv                     # ✅ Top páginas
├── devices.csv                       # ✅ Breakdown por dispositivo
├── first_user_acquisition.csv       # ✅ Primeiros acessos
├── video_events.csv                  # ✅ Eventos de vídeo
├── weekly_comparison.csv            # ✅ Comparação semanal
└── days_with_most_users.csv        # ✅ Dias com mais usuários
```

## 🎯 **Dados Específicos Solicitados**

### **✅ Métricas Principais**
- Usuários únicos
- Total de sessões
- Total de pageviews
- Duração média de sessão
- Taxa de rejeição

### **✅ Top Páginas e Links**
- Páginas mais acessadas
- Links mais clicados
- Análise de tráfego por página

### **✅ Breakdown por Dispositivo**
- Desktop, Mobile, Tablet
- Distribuição de usuários
- Métricas por categoria

### **✅ Primeiros Acessos**
- Source/Medium de aquisição
- Novos usuários por fonte
- Análise de canais

### **✅ Eventos de Vídeo**
- video_start
- video_progress
- video_complete

### **✅ Análise Temporal**
- Dias com mais usuários
- Comparação semanal
- Tendências temporais

## 🌐 **Após Executar o Pipeline**

1. **Dados criados** na pasta `data/`
2. **Execute o dashboard:**
   ```bash
   streamlit run streamlit_dashboard.py
   ```
3. **Acesse:** http://localhost:8501
4. **Selecione os dados** no menu lateral
5. **Visualize as métricas** e gráficos

## 🔄 **Fluxo Completo**

```
Pipeline → Dados CSV → Dashboard Streamlit → Visualizações
```

1. **Pipeline** - Cria dados específicos
2. **CSVs** - Dados organizados e processados
3. **Dashboard** - Interface visual
4. **Visualizações** - Gráficos e métricas

## 📈 **Resultado Final**

Após executar o pipeline, você terá:

- ✅ **7 arquivos CSV** com dados específicos
- ✅ **Dashboard funcional** com dados reais
- ✅ **Métricas principais** formatadas
- ✅ **Top páginas** e links
- ✅ **Breakdown por dispositivo**
- ✅ **Primeiros acessos** por fonte
- ✅ **Eventos de vídeo** específicos
- ✅ **Análise temporal** completa

## 🎉 **Sucesso!**

O pipeline agora funciona perfeitamente e cria exatamente os dados que você solicitou:

- **Métricas principais** ✅
- **Top páginas e links** ✅
- **Breakdown por dispositivo** ✅
- **Primeiros acessos** ✅
- **Eventos de vídeo** ✅
- **Análise temporal** ✅

**Execute:** `python simple_pipeline.py` e depois `streamlit run streamlit_dashboard.py`

**Desenvolvido com ❤️ para análise completa de dados GA4**
