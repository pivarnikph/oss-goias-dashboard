# Modelo Power BI — Auditoria OSS Saúde Goiás

## 📁 Arquivos a importar

Em **Power BI Desktop → Get Data → Text/CSV**, importe os 12 CSVs de `_extractions/_consolidado/`:

### Tabelas FATO (medidas)
| Arquivo | Granularidade | Uso |
|---|---|---|
| `_analise/fato_hospital_mes.csv` | 1 linha por hospital × ano × mês | **Tabela principal** — todos os KPIs |
| `producao_vs_meta.csv` | 1 linha por hospital × período × indicador | Drill-down de % atingimento por meta |
| `producao_por_especialidade.csv` | 1 linha por hospital × período × especialidade | Análise por especialidade médica |
| `categorias_gasto.csv` | 1 linha por hospital × período × categoria | Composição da despesa |
| `rubricas_contabeis.csv` | 1 linha por hospital × período × rubrica | Detalhamento contábil |
| `fluxo_caixa.csv` | 1 linha por hospital × ano-mês | Movimentações entrada/saída |

### Tabelas DIMENSÃO (filtros)
| Arquivo | Chave | Conteúdo |
|---|---|---|
| `_analise/dim_hospital.csv` | `hospital` | Hospital → OSS canonical |
| `contrato_gestao.csv` | `_filename` | Contratos (1 linha por documento) |

### Tabelas DETALHE (apoio)
| Arquivo | Conteúdo |
|---|---|
| `contrato_metas.csv` | Metas físicas pactuadas (por contrato) |
| `contrato_indicadores_qualidade.csv` | Indicadores de qualidade (por contrato) |
| `contrato_recursos_humanos.csv` | Quadro mínimo de pessoal (por contrato) |
| `contrato_penalidades.csv` | Cláusulas de multa (por contrato) |

---

## 🔗 Relacionamentos (Modelo → Manage Relationships)

```
dim_hospital[hospital] → fato_hospital_mes[hospital]              (1:N, ativo)
dim_hospital[hospital] → producao_vs_meta[hospital]               (1:N, ativo)
dim_hospital[hospital] → producao_por_especialidade[hospital]     (1:N, ativo)
dim_hospital[hospital] → categorias_gasto[hospital]               (1:N, ativo)
dim_hospital[hospital] → rubricas_contabeis[hospital]             (1:N, ativo)
dim_hospital[hospital] → fluxo_caixa[hospital]                    (1:N, ativo)
dim_hospital[hospital] → contrato_gestao[hospital]                (1:N, ativo)

contrato_gestao[_filename] → contrato_metas[_filename]            (1:N, ativo)
contrato_gestao[_filename] → contrato_indicadores_qualidade       (1:N, ativo)
contrato_gestao[_filename] → contrato_recursos_humanos            (1:N, ativo)
contrato_gestao[_filename] → contrato_penalidades                 (1:N, ativo)
```

### Tabela calendário (criar via DAX)
```dax
dim_calendario =
ADDCOLUMNS(
    CALENDAR(DATE(2018,1,1), DATE(2026,12,31)),
    "Ano", YEAR([Date]),
    "Mes", MONTH([Date]),
    "AnoMes", FORMAT([Date], "YYYY-MM"),
    "Trimestre", "T" & FORMAT([Date], "Q"),
    "AnoTri", YEAR([Date]) & "-T" & FORMAT([Date], "Q"),
    "MesNome", FORMAT([Date], "MMM")
)
```

Relacione `dim_calendario[AnoMes]` com `fato_hospital_mes[ano_mes]`.

---

## 📐 Medidas DAX essenciais

### Financeiro
```dax
Total Recebidos SES = SUM(fato_hospital_mes[recebidos_ses])

Total Executados = SUM(fato_hospital_mes[executados])

Total Devolvidos = SUM(fato_hospital_mes[devolvidos])

% Execução Financeira =
DIVIDE([Total Executados], [Total Recebidos SES], 0) * 100

Saldo Acumulado =
CALCULATE(
    SUM(fato_hospital_mes[saldo_final]),
    LASTDATE(dim_calendario[Date])
)

Variação YoY Executados =
VAR atual = [Total Executados]
VAR ano_anterior =
    CALCULATE(
        [Total Executados],
        SAMEPERIODLASTYEAR(dim_calendario[Date])
    )
RETURN
DIVIDE(atual - ano_anterior, ano_anterior, 0) * 100
```

### Produção
```dax
Total Consultas = SUM(fato_hospital_mes[consultas])
Total Internações = SUM(fato_hospital_mes[internacoes])
Total Cirurgias = SUM(fato_hospital_mes[cirurgias])
Total Atendimentos = [Total Consultas] + [Total Internações] + [Total Cirurgias]

Taxa Ocupação Média =
AVERAGE(fato_hospital_mes[taxa_ocupacao_perc])

% Execução Física =
AVERAGE(fato_hospital_mes[perc_exec_fisica])

Eficiência Composta =
DIVIDE([% Execução Física], [% Execução Financeira], 0) * 100
// > 100 = produção acima do gasto (mais eficiente)
// < 100 = gastando mais que produzindo
```

### Custos unitários
```dax
Custo Médio/Consulta =
AVERAGEX(
    FILTER(fato_hospital_mes, fato_hospital_mes[custo_por_consulta] > 0),
    fato_hospital_mes[custo_por_consulta]
)

Custo Médio/Internação =
AVERAGEX(
    FILTER(fato_hospital_mes, fato_hospital_mes[custo_por_internacao] > 0),
    fato_hospital_mes[custo_por_internacao]
)

Custo Médio/Leito-Mês =
AVERAGEX(
    FILTER(fato_hospital_mes, fato_hospital_mes[custo_por_leito_mes] > 0),
    fato_hospital_mes[custo_por_leito_mes]
)

Custo Médio/Cirurgia =
AVERAGEX(
    FILTER(fato_hospital_mes, fato_hospital_mes[custo_por_cirurgia] > 0),
    fato_hospital_mes[custo_por_cirurgia]
)
```

### Outliers (alertas)
```dax
Hospitais com Outlier =
CALCULATE(
    DISTINCTCOUNT(fato_hospital_mes[hospital]),
    OR(
        ABS(fato_hospital_mes[custo_por_consulta_zscore]) >= 2.5,
        ABS(fato_hospital_mes[custo_por_internacao_zscore]) >= 2.5
    )
)

Total Outliers =
COUNTROWS(
    FILTER(
        fato_hospital_mes,
        OR(
            ABS(fato_hospital_mes[custo_por_consulta_zscore]) >= 2.5,
            OR(
                ABS(fato_hospital_mes[custo_por_internacao_zscore]) >= 2.5,
                OR(
                    ABS(fato_hospital_mes[custo_por_leito_mes_zscore]) >= 2.5,
                    ABS(fato_hospital_mes[custo_por_cirurgia_zscore]) >= 2.5
                )
            )
        )
    )
)
```

### Conformidade (cobertura de dados)
```dax
Hospitais com Reporte Completo =
CALCULATE(
    DISTINCTCOUNT(fato_hospital_mes[hospital]),
    NOT(ISBLANK(fato_hospital_mes[executados])),
    NOT(ISBLANK(fato_hospital_mes[consultas]))
)

Meses sem Reporte Financeiro =
CALCULATE(
    COUNTROWS(fato_hospital_mes),
    ISBLANK(fato_hospital_mes[executados])
)
```

---

## 📊 Visualizações sugeridas (5 abas)

### Aba 1 — Visão Executiva (1 página)
- **Cards (topo)**: Total Recebidos, Total Executados, % Exec Financeira média, Total Outliers
- **Gráfico de barras**: Total Executados por OSS (top 10)
- **Gráfico de linha**: Evolução mensal de Recebidos × Executados
- **Mapa de calor**: Hospital × Mês — % Execução Financeira (verde > 90%, amarelo 70-90%, vermelho < 70%)
- **Tabela**: Top 10 outliers com hospital, métrica, valor, z-score

### Aba 2 — Por Hospital
- Slicer: Hospital (default = HUGOL)
- Card: Total Recebidos do hospital, % Exec Financeira, Custo/Consulta médio
- Linha mensal: Recebidos × Executados × Devolvidos
- Tabela: meses com seus valores
- Gauge: % Execução Física (média do hospital vs meta de 100%)

### Aba 3 — Comparativo entre OSS
- Slicer: Período (ano)
- Barras: Total Executados por OSS
- Scatter: Custo/Consulta vs % Execução Financeira (cada bolha = hospital, tamanho = volume)
- Tabela: OSS, hospitais, total executado, mediana custo/internação

### Aba 4 — Performance Física vs Financeira
- Scatter: % Exec Financeira (X) × % Exec Física (Y) — quadrantes:
  - Superior direito (verde): alta execução em ambos = ideal
  - Inferior direito (amarelo): gastou bem mas produziu pouco = ineficiência
  - Superior esquerdo (azul): produziu sem gastar = sub-execução financeira
  - Inferior esquerdo (vermelho): baixa em ambos = problema sério
- Pontos coloridos por OSS

### Aba 5 — Auditoria & Outliers
- Tabela detalhada de outliers (z-score >= 2.5)
- Drill-through para o doc original
- Filtros: hospital, métrica, período
- Notas explicativas (hover)

---

## 🎨 Padrões visuais

- **Cores OSS**: paleta categórica de 10 cores distintas (uma por OSS)
- **Cores % Execução**: gradiente vermelho → amarelo → verde (0% → 50% → 100%+)
- **Formato de moeda**: "R$ " + `#.##0;(R$ #.##0)`
- **Formato %**: 1 casa decimal, ex: 87,5%

---

## 🔄 Atualização

Os CSVs ficam em `C:\OSS-Goias\_extractions\_consolidado\`. Quando re-rodar a extração (Fase 4 — pipeline incremental), o Power BI pode atualizar via **Refresh** sem perder o modelo.
