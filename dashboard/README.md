# Dashboard OSS Goiás

Dashboard interativo construído em Streamlit, com IA integrada via Claude API.

## Como rodar

### Local (recomendado para apresentações)

```powershell
cd C:\OSS-Goias\dashboard
streamlit run app.py
```

Abre automaticamente em `http://localhost:8501` no seu navegador.

### Deploy gratuito no Streamlit Cloud (público)

1. Crie repositório Git com a pasta `dashboard/`
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o GitHub, selecione o repo
4. Configure secret `ANTHROPIC_API_KEY` em Settings → Secrets
5. ✅ Vira `https://oss-goias.streamlit.app` — público com link

⚠️ **Atenção**: para deploy público, você precisa hospedar os CSVs em algum lugar acessível (AWS S3, Google Cloud Storage, ou junto no repo se forem pequenos).

## Estrutura

```
dashboard/
├── app.py                         # Página inicial
├── utils.py                       # Funções compartilhadas
├── pages/
│   ├── 1_📊_Visão_Executiva.py   # KPIs, evolução, mapa de calor, outliers
│   ├── 2_🏥_Por_Hospital.py       # Drill-down por hospital
│   ├── 3_⚖️_Comparativo.py        # Comparar múltiplos hospitais/OSS
│   └── 4_🤖_Pergunte_Aos_Dados.py # Chat IA — pergunte em português
└── README.md
```

## Páginas

### 📊 Visão Executiva
- KPIs no topo: Recebido, Executado, Devolvido, % Execução
- Evolução mensal (linha): financeiro
- Top OSS e Top hospitais (barras)
- Mapa de calor: % execução financeira por hospital × mês
- Tabela de outliers

### 🏥 Por Hospital
- Selecionar 1 hospital
- Timeline financeira (barras agrupadas)
- Atendimentos mensais (linha)
- Custos unitários (mediana)
- Composição de gastos por categoria
- Atipicidades específicas

### ⚖️ Comparativo
- Switch Hospital ↔ OSS
- Multi-seleção
- Ranking financeiro
- Evolução comparada (linha)
- **Quadrantes**: Execução financeira × Execução física
- Comparação de custo unitário

### 🤖 Pergunte aos Dados (IA)
- Caixa de chat — escreva em português
- Claude Sonnet 4.6 gera código pandas + Plotly
- Código é executado **localmente** nos seus dataframes
- Resposta inclui dataframe, gráfico e análise narrativa
- Exemplos prontos pra clicar
- Custo por pergunta: ~R$ 0,02

## Customização rápida

- **Cores**: edite `OSS_COLORS` em `utils.py`
- **Adicionar métrica**: adicione no script Python e ela vira filtrável automaticamente
- **Brasão / logo**: adicione `st.image("logo.png")` no `app.py`
- **Tema**: crie `.streamlit/config.toml` com cores SES-GO

## Atualização de dados

Ao rodar nova extração:
1. Re-rode `python _scripts/73_aggregate_extractions.py`
2. Re-rode `python _scripts/91_build_kpi_dataset.py`
3. No dashboard, clique no menu Streamlit → "Clear cache" ou recarregue

Os CSVs são lidos com cache de 5 minutos (`@st.cache_data(ttl=300)`).
