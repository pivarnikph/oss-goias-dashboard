# RELATÓRIO DE VALIDAÇÃO DOS DADOS
**Auditoria das OSS de Saúde · Estado de Goiás**
**Gerado em:** 10/05/2026 20:57

---

## Sumário Executivo da Validação

| Indicador | Valor |
|---|---:|
| URLs no manifesto | 20,178 |
| URLs com hash SHA-256 | 20,139 (98.8%) |
| Downloads 200 OK | 20,087 |
| Downloads 404 (links quebrados) | 206 |
| Arquivos em disco | 19,669 |
| **Taxa de download bem-sucedido** | **98.82%** |
| Extrações estruturadas (JSON) | 1,460 |
| Linhas fato_hospital_mes | 465 |
| Hospitais distintos | 13 |
| OSS distintas | 11 |
| Outliers de custo (z ≥ 2,5) | 13 |
| Duplicatas SHA-256 (grupos) | 864 |
| **Checks PASSOU** | **15** |
| **Checks FALHOU** | **0** ⚠️ |

---

## 1. Integridade dos Downloads

- **20,381** entradas no log de download
- **20,178** URLs únicas atendidas
- **20,087** sucesso (HTTP 200) + **53** já existentes
- **206** links quebrados (404)
- **0** outras falhas
- **100%** dos arquivos baixados possuem hash SHA-256 para verificação posterior

---

## 2. Conformidade Manifesto ↔ Disco

- Manifesto: **20,178** URLs catalogadas
- Disco: **19,669** arquivos íntegros
- Cobertura efetiva: **99.81%** dos URLs estão em disco
- Lacuna documentada: **38** docs com 404 permanente (ver `RELATORIO_AUSENCIAS.md`)

---

## 3. Cobertura das Extrações via IA

| Categoria | JSONs extraídos | Linhas no CSV |
|---|---:|---:|
| Contratos de Gestão | 394 | 394 |
| Relatórios de Produção | 531 | 531 |
| Comparativo Financeiro | 535 | 535 |

---

## 4. Qualidade dos Dados Estruturados

### 4.1 Cobertura por campo crítico

| Campo | Preenchidos | Total | % |
|---|---:|---:|---:|
| Recebido SES | 374 | 465 | 80.4% |
| Executado | 374 | 465 | 80.4% |
| Consultas | 395 | 465 | 84.9% |
| Internações | 258 | 465 | 55.5% |
| % Execução Financeira | 362 | 465 | 77.8% |
| % Execução Física | 140 | 465 | 30.1% |
| Custo / Consulta | 305 | 465 | 65.6% |
| Custo / Internação | 217 | 465 | 46.7% |
| Custo / Leito-Mês | 88 | 465 | 18.9% |

### 4.2 Sinais de extração parcial

- **69** períodos com financeiro mas sem produção
- **87** períodos com produção mas sem financeiro (atenção: pode indicar relatórios não extraídos)
- **0** valores negativos em campos monetários/contagens (deve ser zero)

---

## 5. Consistência Financeira por Hospital

Equação esperada: `executado ≤ recebido + saldo_anterior`. Hospitais com **% execução > 150%** demandam investigação.

| Hospital | OSS | Meses | Recebido | Executado | % Exec | Sinal |
|---|---|---:|---:|---:|---:|:--:|
| HETRIN | IMED | 41 | R$ 211.223.086 | R$ 254.497.331 | 120.5% | ⚠ |
| HEAPA | IGH | 30 | R$ 120.792.094 | R$ 129.341.191 | 107.1% | ✓ |
| CORA | Hospital de Amor | 13 | R$ 52.279.830 | R$ 55.935.224 | 107.0% | ✓ |
| CREDEQ | ABEVIDA | 67 | R$ 147.202.608 | R$ 157.484.842 | 107.0% | ✓ |
| HUGO | Albert Einstein (SBIBHAE) | 20 | R$ 381.404.949 | R$ 396.802.244 | 104.0% | ✓ |
| HEANA | FUNEV | 43 | R$ 442.247.446 | R$ 445.696.291 | 100.8% | ✓ |
| HUGOL | AGIR | 45 | R$ 1.393.361.012 | R$ 1.398.412.726 | 100.4% | ✓ |
| HDT | ISG | 40 | R$ 323.007.421 | R$ 323.400.239 | 100.1% | ✓ |
| CRESM | ABEVIDA | 74 | R$ 106.155.059 | R$ 104.342.013 | 98.3% | ✓ |
| HERSO | IPGSE | 20 | R$ 136.929.869 | R$ 131.976.223 | 96.4% | ✓ |
| HEL | Instituto Patris | 45 | R$ 137.337.410 | R$ 130.298.883 | 94.9% | ✓ |
| PFRE | IMED | 19 | R$ 27.944.903 | R$ 26.499.160 | 94.8% | ✓ |
| HEJ | AGIR | 8 | R$ 71.166.876 | R$ 59.575.821 | 83.7% | ✓ |

---

## 6. Cruzamentos e Anomalias

### 6.1 Outliers de custo unitário
**13** períodos com z-score ≥ 2,5 detectados. Distribuição:

| Hospital | Qtd outliers |
|---|---:|
| CORA | 8 |
| CREDEQ | 2 |
| HDT | 1 |
| HUGO | 1 |
| HETRIN | 1 |

### 6.2 Duplicatas (SHA-256)
- **864** grupos de arquivos com conteúdo idêntico (mesmo hash)
- **1001** cópias 'extras' (documentos republicados em URLs diferentes)

### 6.3 Nomes de hospitais potencialmente duplicados

| Nome A | Nome B |
|---|---|
| HUGO | HUGOL |

---

## 7. Cobertura Temporal

| Ano | Períodos hospital × mês |
|---:|---:|
| 2018 | 23 |
| 2019 | 12 |
| 2020 | 24 |
| 2021 | 18 |
| 2022 | 37 |
| 2023 | 89 |
| 2024 | 101 |
| 2025 | 122 |
| 2026 | 39 |

**Hospitais sem dados financeiros em 2025:** CREDEQ

---

## Checks Automatizados — Resultado

### ✓ Todos os checks passaram

**Total: 15 passou, 0 falhou** (de 15 checks)

---

## Metodologia

Esta validação executa **6 camadas independentes** de verificação:

1. **Integridade de download**: hash SHA-256, status HTTP, contagem de URLs
2. **Conformidade manifesto ↔ disco**: cada URL declarada deve ter arquivo correspondente íntegro
3. **Cobertura das extrações**: contagem de JSONs estruturados vs CSVs consolidados
4. **Qualidade dos dados**: preenchimento de campos críticos, ranges plausíveis, ausência de valores impossíveis
5. **Consistência financeira**: equação de balanço por período (executado vs recebido)
6. **Cruzamentos e anomalias**: outliers via z-score, duplicatas por SHA-256, nomes similares

**Reproduzibilidade**: rode `python _scripts/96_validacao_completa.py` a qualquer momento — o relatório é regerado.

**Audit trail**: cada check fica registrado em `_logs/validacao_detalhada.csv` (1 linha por verificação).
