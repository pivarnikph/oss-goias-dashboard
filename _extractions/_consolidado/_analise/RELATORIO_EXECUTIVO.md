# RELATÓRIO EXECUTIVO
## Auditoria das Organizações Sociais de Saúde do Estado de Goiás

**Período analisado:** 2023 — 2026
**Apresentado a:** Governador do Estado de Goiás
**Data:** {{DATA_GERACAO}}

---

## SUMÁRIO EXECUTIVO

[Esta seção será preenchida pela narrativa via Claude API após análise dos números abaixo]

**Em números:**
- **{{N_HOSPITAIS}}** hospitais analisados, sob gestão de **{{N_OSS}}** Organizações Sociais
- **{{N_DOCUMENTOS}}** documentos baixados e validados (manifesto auditável)
- **R$ {{TOTAL_EXECUTADO}}** executados no período pelas OSS
- **{{PERC_EXEC_MEDIO}}%** execução financeira média
- **{{N_OUTLIERS}}** atipicidades de custo identificadas

**Principais achados:**

1. {{ACHADO_1}}
2. {{ACHADO_2}}
3. {{ACHADO_3}}

**Recomendações priorizadas:**

1. {{RECOMENDACAO_1}}
2. {{RECOMENDACAO_2}}
3. {{RECOMENDACAO_3}}

---

## 1. METODOLOGIA

### 1.1 Coleta automatizada

Todos os documentos foram baixados automaticamente dos portais oficiais de transparência das 10 OSS gestoras, num único pipeline auditável:

- **Origem:** 14 portais públicos (URLs em `seeds.csv`)
- **Estratégia:** crawl + download + validação por hash SHA-256
- **Volume bruto:** 19.118 arquivos íntegros, 48 GB
- **Cobertura temporal:** janeiro/2023 — abril/2026

Cada documento tem registro de:
- URL original
- Status HTTP de download
- Hash SHA-256 (para auditoria de integridade)
- Tamanho em bytes
- Carimbo de tempo (ISO-8601)

### 1.2 Extração estruturada

Os documentos foram processados via **Claude Sonnet 4.6** (Anthropic), com schemas JSON estritos para 3 tipos de documentos:

- **Contratos de Gestão e Aditivos:** 394 documentos extraídos
- **Relatórios de Produção:** 531 documentos extraídos
- **Comparativo Financeiro:** 482 documentos extraídos

**Total: 1.709 extrações em batch (custo USD 76,94 ≈ R$ 385).**

A extração via IA permite estruturar dados que estavam em formato livre (PDF, planilhas), aplicando o mesmo schema a todos os hospitais — isso é o que viabiliza comparações entre OSS.

### 1.3 Limites declarados

- Documentos **anteriores a 2023** foram excluídos por escolha de escopo
- A categoria **"atos convocatórios" (compras)** foi excluída (78% do volume bruto, baixo valor analítico)
- Os hospitais **HETRIN** e **PFRE** não tiveram dados financeiros recuperados — investigação pendente
- "**% execução física**" calculada como média ponderada dos indicadores reportados pelo próprio hospital (auto-declaração — não há auditoria independente externa nesta análise)

---

## 2. VISÃO GERAL DA REDE

### 2.1 Cobertura por hospital

| OSS Gestora | Hospital | Meses analisados | % com dados financeiros | Mediana mensal executada |
|---|---|---:|---:|---:|
{{TABELA_COBERTURA}}

### 2.2 Concentração por OSS

[A análise por OSS será inserida aqui via Claude API]

{{NARRATIVA_OSS}}

### 2.3 Distribuição financeira

- **Total recebido SES (período):** R$ {{TOTAL_RECEBIDO}}
- **Total executado:** R$ {{TOTAL_EXECUTADO}}
- **Total devolvido:** R$ {{TOTAL_DEVOLVIDO}}
- **% execução financeira média ponderada:** {{PERC_EXEC}}%

---

## 3. ANÁLISE POR HOSPITAL

### 3.1 Hospitais com maior volume (top 5)

{{NARRATIVAS_TOP5}}

### 3.2 Hospitais com sinais de alerta

{{NARRATIVAS_ALERTAS}}

### 3.3 Hospitais com performance destaque

{{NARRATIVAS_DESTAQUES}}

---

## 4. ATIPICIDADES E OUTLIERS

### 4.1 Outliers de custo unitário (z-score ≥ 2.5)

{{TABELA_OUTLIERS}}

### 4.2 Explicação dos casos extremos

[Análise narrativa dos outliers — distinguindo ramp-up (legítimo) vs anomalia operacional]

{{NARRATIVA_OUTLIERS}}

---

## 5. EXECUÇÃO FÍSICA × FINANCEIRA

### 5.1 Matriz de quadrantes

```
                    ALTA EXECUÇÃO FINANCEIRA
                            |
        BAIXA              |              ALTA
        PRODUÇÃO           |              PRODUÇÃO
        =                  |              =
        SOBRE-GASTO        |              IDEAL
        ───────────────────┼───────────────────
        BAIXA              |              ALTA
        PRODUÇÃO           |              PRODUÇÃO
        =                  |              =
        PROBLEMA SÉRIO     |              SUB-EXECUÇÃO
                           |              FINANCEIRA
                    BAIXA EXECUÇÃO FINANCEIRA
```

### 5.2 Posicionamento dos hospitais

{{POSICIONAMENTO_QUADRANTES}}

---

## 6. RECOMENDAÇÕES

### 6.1 Curto prazo (até 3 meses)

[A serem definidas a partir dos achados]

### 6.2 Médio prazo (até 12 meses)

[A serem definidas]

### 6.3 Estruturais

[Padronização de relatórios, transparência ativa, auditoria recorrente]

---

## 7. ANEXOS

### 7.1 Lista completa dos documentos baixados

Disponível em: `C:\OSS-Goias\_logs\manifest_GERAL.csv` (13.845 URLs com hash, status e timestamp)

### 7.2 Datasets analíticos

Disponíveis em: `C:\OSS-Goias\_extractions\_consolidado\`

- `_analise/fato_hospital_mes.csv` — tabela fato (461 linhas, 32 colunas)
- `_analise/dim_hospital.csv` — dimensão hospital→OSS
- `_analise/cobertura_kpi.csv` — completude por hospital
- `_analise/outliers.csv` — atipicidades detectadas
- 8 CSVs detalhados (categorias_gasto, fluxo_caixa, producao_vs_meta, etc.)

### 7.3 Modelo Power BI

Schema, relacionamentos e medidas DAX em `_analise/POWER_BI_SCHEMA.md`.

### 7.4 Reprodutibilidade

Todo o pipeline (download, extração, análise) está em `C:\OSS-Goias\_scripts\` — scripts numerados de 01 a 92, comentados, com logs de auditoria.

---

**Custo total do projeto:** USD 76,94 + 23 USD reservados = **USD 100 ≈ R$ 500** em API.

**Tempo total:** ~6 horas distribuídas em 3 dias (download + validação + extração + análise).
