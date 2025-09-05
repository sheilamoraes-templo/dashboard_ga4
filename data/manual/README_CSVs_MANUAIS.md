# 📁 INSTRUÇÕES PARA CSVs MANUAIS

## 🎯 **ONDE SALVAR SEUS CSVs MANUAIS**

### **Pasta:**
```
C:\repositorio_dev\dashboard_ga4\data\manual\
```

### **Nomes dos Arquivos:**
```
kpis_daily_manual.csv          # Métricas principais diárias
pages_top_manual.csv           # Top páginas e links
devices_manual.csv             # Breakdown por dispositivo
first_user_acquisition_manual.csv  # Primeiros acessos
video_events_manual.csv        # Eventos de vídeo
weekly_comparison_manual.csv   # Comparação semanal
days_with_most_users_manual.csv # Dias com mais usuários
```

## 📊 **FORMATO DOS CSVs**

### **1. kpis_daily_manual.csv**
```csv
date,users,sessions,pageviews,avg_session_duration,bounce_rate
2024-01-01,150,200,800,250,0.45
2024-01-02,180,220,950,280,0.42
```

### **2. pages_top_manual.csv**
```csv
page,pageviews,sessions,users
/,1500,800,600
/sobre,800,500,400
/contato,600,400,300
```

### **3. devices_manual.csv**
```csv
device,users,sessions,pageviews
desktop,200,250,1200
mobile,150,180,800
tablet,50,70,300
```

### **4. first_user_acquisition_manual.csv**
```csv
source,medium,users,sessions
google,organic,100,120
facebook,social,80,100
instagram,social,60,80
```

### **5. video_events_manual.csv**
```csv
date,event_name,count
2024-01-01,video_start,150
2024-01-01,video_progress,120
2024-01-01,video_complete,85
```

### **6. weekly_comparison_manual.csv**
```csv
week,users,sessions,pageviews,avg_session_duration,bounce_rate
2024-W01,1200,1500,4500,280,0.45
2024-W02,1350,1700,5200,295,0.42
```

### **7. days_with_most_users_manual.csv**
```csv
date,users,sessions,pageviews,avg_session_duration,bounce_rate
2024-01-15,300,400,1500,320,0.35
2024-01-20,280,350,1400,310,0.38
```

## 🚀 **COMO USAR**

### **1. Salve seus CSVs na pasta manual/**
### **2. Execute o dashboard:**
```bash
streamlit run streamlit_dashboard.py
```

### **3. No dashboard, selecione os CSVs manuais**
- O sistema detectará automaticamente os arquivos em `data/manual/`
- Processará os dados com a camada de tratamento
- Exibirá as visualizações organizadas

## ✅ **VANTAGENS**

- ✅ **Dados reais** do GA4
- ✅ **Processamento automático** pela camada de tratamento
- ✅ **Visualizações organizadas** no dashboard
- ✅ **Formatação consistente** (números, percentuais, durações)
- ✅ **Validação de dados** automática
- ✅ **Detecção de tipos** automática

## 🔄 **PRÓXIMOS PASSOS**

1. **Salve seus CSVs** na pasta `data/manual/`
2. **Teste no dashboard** para verificar a organização
3. **Ajuste a camada de tratamento** se necessário
4. **Depois testamos a API GA4** para baixar automaticamente

**Desenvolvido com ❤️ para análise completa de dados GA4**
