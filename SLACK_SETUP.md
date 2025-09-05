# 📱 Configuração do Slack para Dashboard GA4

## 🎯 Objetivo
Este documento explica como configurar a integração com Slack para receber relatórios automáticos de GA4.

## 🔧 Métodos de Configuração

### Método 1: Webhook (Recomendado - Mais Simples)

1. **Criar Webhook no Slack:**
   - Acesse: https://api.slack.com/messaging/webhooks
   - Clique em "Create your Slack app"
   - Escolha "From scratch"
   - Nome: "Dashboard GA4"
   - Workspace: Seu workspace

2. **Configurar Webhook:**
   - Vá em "Incoming Webhooks"
   - Ative "Activate Incoming Webhooks"
   - Clique "Add New Webhook to Workspace"
   - Escolha o canal (ex: #analytics)
   - Copie a URL do webhook

3. **Configurar no projeto:**
   ```python
   # Em config/settings.py
   SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
   SLACK_CHANNEL = "#analytics"
   ```

### Método 2: Bot Token (Mais Avançado)

1. **Criar App no Slack:**
   - Acesse: https://api.slack.com/apps
   - Clique "Create New App" > "From scratch"
   - Nome: "Dashboard GA4 Bot"
   - Workspace: Seu workspace

2. **Configurar Permissões:**
   - Vá em "OAuth & Permissions"
   - Scopes necessários:
     - `chat:write` - Enviar mensagens
     - `channels:read` - Ler canais
   - Clique "Install to Workspace"
   - Copie o "Bot User OAuth Token"

3. **Configurar no projeto:**
   ```python
   # Em config/settings.py
   SLACK_BOT_TOKEN = "SEU_BOT_TOKEN_AQUI"  # Substitua pelo seu token real
   SLACK_CHANNEL = "#analytics"
   ```

## ⚙️ Configuração no Projeto

### 1. Editar config/settings.py:
```python
# Configurações do Slack
SLACK_BOT_TOKEN = "SEU_BOT_TOKEN_AQUI"  # OU deixe vazio se usar webhook
SLACK_CHANNEL = "#analytics"  # Canal onde enviar as atualizações
SLACK_WEBHOOK_URL = "SEU_WEBHOOK_URL_AQUI"  # OU deixe vazio se usar bot token
SLACK_REPORTS_ENABLED = True  # Habilitar relatórios no Slack
```

### 2. Escolher um método:
- **Webhook**: Configure apenas `SLACK_WEBHOOK_URL`
- **Bot Token**: Configure apenas `SLACK_BOT_TOKEN`
- **Ambos**: O sistema tentará webhook primeiro, depois bot token

## 🧪 Testando a Configuração

### Via Dashboard Web:
1. Acesse o dashboard
2. Clique em "Testar Slack" na barra superior
3. Verifique se aparece mensagem de sucesso

### Via API:
```bash
curl -X GET "http://localhost:5000/api/test-slack"
```

### Via Python:
```python
from src.slack_client import SlackClient

slack = SlackClient()
success = slack.test_connection()
print("✅ Slack funcionando!" if success else "❌ Problema no Slack")
```

## 📊 Tipos de Relatórios

### Relatórios Automáticos:
- **Diário**: Enviado às 8h (configurável)
- **Semanal**: Enviado às 9h de segunda-feira
- **Mensal**: Enviado no primeiro dia do mês às 10h

### Relatórios Manuais:
- Via dashboard web
- Via API endpoints
- Via código Python

## 📱 Formato das Mensagens

### Estrutura do Relatório:
```
📊 Relatório GA4 - DD/MM/AAAA

📈 Métricas Principais:
• Usuários: X,XXX
• Sessões: X,XXX
• Visualizações: X,XXX
• Duração Média: X.X min
• Taxa de Rejeição: XX.X%

🤖 Análise de IA:
[Insights gerados pela IA]

🔥 Páginas Mais Visitadas:
1. Página X - X,XXX visualizações
2. Página Y - X,XXX visualizações
3. Página Z - X,XXX visualizações
```

## 🔧 Solução de Problemas

### Erro: "Slack não configurado"
- Verifique se `SLACK_BOT_TOKEN` ou `SLACK_WEBHOOK_URL` estão configurados
- Certifique-se que não são os valores padrão ("sua_chave_slack_aqui")

### Erro: "Falha na conexão Slack"
- Verifique se o token/webhook está correto
- Teste a conexão manualmente
- Verifique se o bot tem permissões no canal

### Erro: "Canal não encontrado"
- Verifique se o canal existe
- Certifique-se que o bot tem acesso ao canal
- Use formato correto: "#canal" ou "@usuario"

### Mensagens não aparecem:
- Verifique se `SLACK_REPORTS_ENABLED = True`
- Confirme que a automação está rodando
- Verifique os logs do sistema

## 🚀 Próximos Passos

1. **Configure o Slack** usando um dos métodos acima
2. **Teste a conexão** via dashboard
3. **Inicie a automação** para relatórios automáticos
4. **Personalize os horários** se necessário
5. **Monitore os logs** para garantir funcionamento

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do sistema
2. Teste a configuração manualmente
3. Consulte a documentação oficial do Slack
4. Verifique se todas as dependências estão instaladas
