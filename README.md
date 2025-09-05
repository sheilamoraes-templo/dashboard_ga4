# 📊 Dashboard GA4 com Automação de Relatórios

Um dashboard completo para visualização de dados do Google Analytics 4 com automação de relatórios por email e análise de IA.

## 🚀 Funcionalidades

### ✅ Dashboard Web
- **Métricas em tempo real** do GA4
- **Gráficos interativos** com Plotly
- **Análise de dispositivos** (desktop, mobile, tablet)
- **Páginas mais visitadas**
- **Insights automáticos** com IA

### ✅ Automação de Relatórios
- **Relatórios diários, semanais e mensais**
- **Envio automático por email**
- **Análise de IA integrada**
- **Agendamento flexível**

### ✅ Integração com IA
- **Análise automática** de tendências
- **Insights personalizados**
- **Recomendações práticas**
- **Suporte à OpenRouter**

## 📋 Pré-requisitos

- Python 3.8+
- Conta Google Analytics 4
- Service Account do Google Cloud
- Email para envio de relatórios (opcional)
- Chave OpenRouter para IA avançada (opcional)

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd dashboard_ga4
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais

#### Google Analytics 4
1. Crie um projeto no [Google Cloud Console](https://console.cloud.google.com/)
2. Ative a **Google Analytics Data API v1**
3. Crie um **Service Account** e baixe o arquivo JSON
4. Adicione o email do Service Account como usuário no seu GA4
5. Coloque o arquivo JSON na raiz do projeto como `credenciais_google_ga4.json`

#### Configurações do Projeto
Edite `config/settings.py`:

```python
# Configurações do GA4
GA4_PROPERTY_ID = "SEU_ID_DA_PROPRIEDADE"

# Configurações de Email (opcional)
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_app"

# Configurações de IA (opcional)
OPENROUTER_API_KEY = "sua_chave_openrouter"
```

## 🚀 Como Usar

### 1. Teste a Instalação
```bash
python test_connection.py
```

### 2. Inicie o Dashboard
```bash
python app.py
```

### 3. Acesse o Dashboard
Abra seu navegador e acesse: `http://localhost:5000`

## 📊 Funcionalidades do Dashboard

### Métricas Principais
- **Usuários únicos**
- **Sessões**
- **Visualizações de página**
- **Duração média da sessão**
- **Taxa de rejeição**
- **Páginas por sessão**

### Gráficos Interativos
- **Atividade diária** (usuários, sessões, visualizações)
- **Distribuição por dispositivo** (gráfico de pizza)
- **Tendências temporais**

### Análise de IA
- **Insights automáticos** sobre performance
- **Recomendações** de melhoria
- **Análise de tendências**

### Automação
- **Iniciar/parar** automação
- **Enviar relatórios** manuais
- **Configurar frequência** (diário/semanal/mensal)

## 📧 Configuração de Email

### Gmail
1. Ative a **verificação em duas etapas**
2. Gere uma **senha de app**
3. Configure em `config/settings.py`:

```python
EMAIL_SENDER = "seu_email@gmail.com"
EMAIL_PASSWORD = "sua_senha_de_app"
```

### Outros Provedores
Ajuste as configurações SMTP em `config/settings.py`:

```python
EMAIL_SMTP_SERVER = "smtp.seu_provedor.com"
EMAIL_SMTP_PORT = 587  # ou 465 para SSL
```

## 🤖 Configuração da IA

### OpenRouter (Recomendado)
1. Crie uma conta em [OpenRouter](https://openrouter.ai/)
2. Obtenha sua chave API
3. Configure em `config/settings.py`:

```python
OPENROUTER_API_KEY = "sua_chave_aqui"
```

### Sem IA
O sistema funciona sem IA, gerando insights básicos automaticamente.

## 📁 Estrutura do Projeto

```
dashboard_ga4/
├── 📁 config/
│   └── 📄 settings.py          # Configurações
├── 📁 src/
│   ├── 📄 ga4_client.py        # Cliente GA4
│   ├── 📄 ai_analyzer.py       # Análise de IA
│   ├── 📄 email_sender.py      # Envio de emails
│   └── 📄 automation.py        # Automação
├── 📁 templates/
│   └── 📄 dashboard.html       # Interface web
├── 📄 app.py                   # Aplicação Flask
├── 📄 test_connection.py       # Script de teste
├── 📄 requirements.txt         # Dependências
└── 📄 README.md               # Documentação
```

## 🔧 Configurações Avançadas

### Frequência de Relatórios
Edite `config/settings.py`:

```python
REPORT_FREQUENCY = "daily"  # daily, weekly, monthly
```

### Destinatários
```python
REPORT_RECIPIENTS = ["email1@exemplo.com", "email2@exemplo.com"]
```

### Cache de Dados
```python
CACHE_DURATION = 3600  # 1 hora em segundos
```

## 🚨 Solução de Problemas

### Erro de Conexão GA4
1. Verifique se o arquivo `credenciais_google_ga4.json` está correto
2. Confirme se o Service Account tem permissões no GA4
3. Verifique se a API está ativada no Google Cloud

### Erro de Email
1. Verifique as configurações SMTP
2. Confirme se a senha de app está correta
3. Teste com `python test_connection.py`

### Erro de IA
1. Verifique se a chave OpenRouter está correta
2. O sistema funciona sem IA (insights básicos)

## 📈 Métricas Disponíveis

### Métricas Básicas
- `totalUsers` - Usuários únicos
- `sessions` - Sessões
- `screenPageViews` - Visualizações de página
- `averageSessionDuration` - Duração média da sessão
- `bounceRate` - Taxa de rejeição

### Dimensões
- `date` - Data
- `pageTitle` - Título da página
- `pagePath` - Caminho da página
- `deviceCategory` - Categoria do dispositivo
- `country` - País

## 🔄 Automação

### Relatórios Diários
- **Horário**: 8h da manhã
- **Dados**: Último dia
- **Conteúdo**: Métricas + análise de IA

### Relatórios Semanais
- **Horário**: Segunda-feira às 9h
- **Dados**: Última semana
- **Conteúdo**: Métricas + tendências + top páginas

### Relatórios Mensais
- **Horário**: Primeiro dia do mês às 10h
- **Dados**: Último mês
- **Conteúdo**: Análise completa + insights

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se você encontrar problemas:

1. Execute `python test_connection.py` para diagnosticar
2. Verifique as configurações em `config/settings.py`
3. Consulte a documentação do Google Analytics 4
4. Abra uma issue no repositório

## 🎯 Roadmap

- [ ] Suporte a múltiplas propriedades GA4
- [ ] Relatórios em PDF
- [ ] Integração com Slack/Discord
- [ ] Dashboard mobile responsivo
- [ ] Análise de conversões
- [ ] Alertas automáticos

---

**Desenvolvido com ❤️ para facilitar a análise de dados do GA4**
