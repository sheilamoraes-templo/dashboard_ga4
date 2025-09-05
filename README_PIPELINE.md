# 🚀 Pipeline GA4 - Download de Dados

Sistema completo para baixar dados específicos do Google Analytics 4 e disponibilizar no dashboard Streamlit.

## 📊 **Dados Baixados**

### **Métricas Principais**
- ✅ **Usuários** - Total de usuários únicos
- ✅ **Sessões** - Total de sessões
- ✅ **Pageviews** - Total de visualizações de página
- ✅ **Duração Média** - Tempo médio de sessão
- ✅ **Taxa de Rejeição** - Percentual de rejeição

### **Top Páginas e Links**
- ✅ **Páginas Mais Acessadas** - Top 50 páginas por pageviews
- ✅ **Links Mais Clicados** - Análise de tráfego por página
- ✅ **Análise de Conteúdo** - Performance por seção

### **Breakdown por Dispositivo**
- ✅ **Desktop** - Usuários desktop
- ✅ **Mobile** - Usuários mobile
- ✅ **Tablet** - Usuários tablet
- ✅ **Distribuição** - Percentual por dispositivo

### **Primeiros Acessos**
- ✅ **Source/Medium** - Fonte de aquisição
- ✅ **Novos Usuários** - Usuários por fonte
- ✅ **Canais** - Análise de canais de aquisição

### **Eventos de Vídeo**
- ✅ **video_start** - Início de reprodução
- ✅ **video_progress** - Progresso da reprodução
- ✅ **video_complete** - Conclusão da reprodução

### **Análise Temporal**
- ✅ **Dias com Mais Usuários** - Ranking diário
- ✅ **Comparação Semanal** - Tendências semanais
- ✅ **Análise de Padrões** - Comportamento temporal

## 🚀 **Como Executar**

### **1. Pipeline Padrão (30 dias)**
```bash
python ga4_pipeline.py --days 30
```
**Baixa:** Métricas principais + Top páginas + Dispositivos

### **2. Pipeline Rápido (7 dias)**
```bash
python ga4_pipeline.py --quick
```
**Baixa:** Dados essenciais para teste rápido

### **3. Pipeline Completo (30 dias)**
```bash
python ga4_pipeline.py --full --days 30
```
**Baixa:** Todos os dados disponíveis

### **4. Download Direto**
```bash
python download_ga4_data.py
```
**Execução:** Pipeline completo sem parâmetros

### **5. Menu Interativo**
```bash
python run_pipeline.py
```
**Interface:** Menu com opções interativas

## 📁 **Arquivos Gerados**

Após a execução, os seguintes arquivos serão criados na pasta `data/`:

```
data/
├── kpis_daily.csv                    # Métricas principais
├── pages_top.csv                     # Top páginas
├── devices.csv                       # Breakdown por dispositivo
├── first_user_acquisition.csv       # Primeiros acessos
├── video_events.csv                  # Eventos de vídeo
├── weekly_comparison.csv            # Comparação semanal
└── days_with_most_users.csv        # Dias com mais usuários
```

## 🔧 **Pré-requisitos**

### **1. Credenciais GA4**
- Arquivo `credenciais_google_ga4.json` na raiz do projeto
- Service Account do Google Cloud Console
- Permissões de leitura na propriedade GA4

### **2. Configuração**
- Propriedade GA4 configurada em `config/settings.py`
- Python 3.8+ com dependências instaladas

### **3. Dependências**
```bash
pip install -r requirements.txt
```

## 🌐 **Após o Download**

### **Executar Dashboard**
```bash
streamlit run streamlit_dashboard.py
```

### **Acessar Dashboard**
- **Local:** http://localhost:8501
- **Rede:** http://192.168.1.9:8501

## 📊 **Exemplo de Uso Completo**

```bash
# 1. Baixar dados (30 dias)
python ga4_pipeline.py --full --days 30

# 2. Executar dashboard
streamlit run streamlit_dashboard.py

# 3. Acessar no navegador
# http://localhost:8501
```

## 🔄 **Fluxo de Dados**

```
GA4 API → Pipeline → Processamento → CSVs → Dashboard Streamlit
```

1. **GA4 API** - Baixa dados do Google Analytics
2. **Pipeline** - Processa e organiza os dados
3. **Processamento** - Padroniza e valida dados
4. **CSVs** - Salva dados processados
5. **Dashboard** - Visualiza dados no Streamlit

## ⚙️ **Configurações Avançadas**

### **Período Personalizado**
```bash
python ga4_pipeline.py --days 60
```

### **Limite de Páginas**
Editar `pipeline_config.py`:
```python
"top_pages_limit": 100  # Aumentar para 100 páginas
```

### **Cache Personalizado**
Editar `pipeline_config.py`:
```python
"cache_ttl_minutes": 60  # Cache por 1 hora
```

## 🐛 **Troubleshooting**

### **Erro de Credenciais**
```
❌ Credenciais não encontradas: credenciais_google_ga4.json
```
**Solução:** Configure as credenciais do Google Cloud Console

### **Erro de Propriedade GA4**
```
❌ Propriedade GA4 não configurada
```
**Solução:** Configure `GA4_PROPERTY_ID` em `config/settings.py`

### **Erro de Permissões**
```
❌ Acesso negado à propriedade GA4
```
**Solução:** Verifique permissões do Service Account

## 📈 **Monitoramento**

### **Logs do Pipeline**
O pipeline exibe logs detalhados:
```
INFO:data_processor:Processando DataFrame kpis_daily com 31 linhas
✅ Métricas principais salvas: kpis_daily.csv (31 registros)
🎉 Pipeline concluído: 7/7 downloads bem-sucedidos
```

### **Status dos Downloads**
- ✅ **Sucesso** - Dados baixados e processados
- ⚠️ **Aviso** - Dados parciais ou limitados
- ❌ **Erro** - Falha no download

## 🎯 **Resultado Final**

Após executar o pipeline, você terá:

- ✅ **Dados atualizados** do GA4
- ✅ **CSVs processados** e padronizados
- ✅ **Dashboard funcional** com dados reais
- ✅ **Análises específicas** que você solicitou

**Desenvolvido com ❤️ para análise completa de dados GA4**
