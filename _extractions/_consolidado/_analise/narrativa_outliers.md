## Classificação de Outliers de Custo Unitário

| Hospital | Período | Métrica | z-score | Custo Unitário | Classificação | Explicação |
|---|---|---|---|---|---|---|
| CORA (Hospital de Amor) | 2025-06 | custo_por_consulta | 14,58 | R$ 103.710 | RAMP-UP | Abertura em abr/2025. Segundo mês de operação: volume de consultas ínfimo dilui custo total de R$ 3,4 mi sobre denominador mínimo. |
| CORA (Hospital de Amor) | 2025-06 | custo_por_internacao | 9,82 | R$ 180.128 | RAMP-UP | Mesmo mês de operação acima. Leitos e internações abaixo da capacidade nominal inflarão custo unitário até estabilização do fluxo. |
| HDT (ISG) | 2023-10 | custo_por_cirurgia | 9,40 | R$ 975.397 | ESPECIALIZAÇÃO | HDT é hospital de doenças tropicais: volume cirúrgico estruturalmente baixo. Denominador pequeno amplifica custo/cirurgia. Valor absoluto executado (R$ 7,8 mi) é compatível com histórico. Exige confirmação do número de cirurgias registradas no mês. |
| HUGO (Albert Einstein) | 2025-04 | custo_por_consulta | 5,13 | R$ 39.697 | ERRO DE EXTRAÇÃO | Erro de extração em 2025-04 já documentado e corrigido com re-extração via Claude Opus 4.7. Outlier residual desta correção. Não requer nova investigação. |
| CORA (Hospital de Amor) | 2025-07 | custo_por_cirurgia | 4,31 | R$ 481.765 | RAMP-UP | Terceiro mês de operação. Volume cirúrgico ainda em crescimento. Padrão consistente com ramp-up observado nas demais métricas de jun/2025. |
| CORA (Hospital de Amor) | 2025-11 | custo_por_cirurgia | 4,19 | R$ 469.764 | ANOMALIA POTENCIAL | Sétimo mês de operação — tempo suficiente para volume cirúrgico se normalizar. Custo elevado persistente nesta métrica específica, com R$ 5,6 mi executados, não se explica mais por ramp-up. Requer verificação do número de cirurgias registradas no mês e comparação com out/2025 e dez/2025. |
| CORA (Hospital de Amor) | 2025-08 | custo_por_cirurgia | 4,01 | R$ 452.607 | RAMP-UP | Quarto mês de operação. Ainda em fase de ramp-up cirúrgico. Cirurgias eletivas tendem a ser as últimas a atingir volume pleno em hospitais novos. |
| CORA (Hospital de Amor) | 2026-01 | custo_por_internacao | 3,92 | R$ 83.880 | ANOMALIA POTENCIAL | Décimo mês de operação. Execução elevada (R$ 7,2 mi). Custo por internação fora do padrão neste estágio não se justifica por ramp-up. Verificar número de internações registradas e eventual subnotificação de produção. |
| CREDEQ (ABEVIDA) | 2020-02 | custo_por_internacao | 3,67 | R$ 79.773 | ANOMALIA POTENCIAL | Sem contexto de abertura ou especialização que justifique. Mês isolado com custo/internação elevado. Dado de 2020 — verificar se coincide com início da pandemia COVID-19 (redução abrupta de internações eletivas com manutenção do custo fixo). Se confirmado, reclassificar como evento extraordinário. |
| CORA (Hospital de Amor) | 2025-07 | custo_por_internacao | 3,61 | R$ 78.834 | RAMP-UP | Terceiro mês de operação. Consistente com os demais outliers de jul/2025 da CORA. |
| CORA (Hospital de Amor) | 2026-01 | custo_por_cirurgia | 3,26 | R$ 379.667 | ANOMALIA POTENCIAL | Décimo mês de operação, mesmo mês do outlier de internação acima (R$ 7,2 mi executados). Dois outliers simultâneos em jan/2026 com execução elevada reforçam necessidade de verificação da produção registrada neste mês. |
| HETRIN (IMED) | 2025-08 | custo_por_leito_mes | 2,95 | R$ 270.796 | ESPECIALIZAÇÃO | HETRIN tem perfil de alta complexidade com sobre-execução estrutural explicada (saldo bancário + outras receitas). Custo/leito elevado é consistente com mix assistencial de maior complexidade. Monitorar tendência, mas não acionar investigação isolada. |
| CREDEQ (ABEVIDA) | 2020-03 | custo_por_internacao | 2,70 | R$ 64.071 | ANOMALIA POTENCIAL | Mês consecutivo ao outlier de fev/2020. Dois meses seguidos com custo/internação elevado no CREDEQ reforçam a hipótese de queda de volume de internações (COVID-19 ou outro fator). Investigar junto com fev/2020 no mesmo processo. |

---

### Resumo Executivo dos Sinalizadores

| Classificação | Qtd | Casos |
|---|---|---|
| RAMP-UP | 6 | CORA jun–ago/2025 (4 registros) + CORA jul/2025 internação |
| ESPECIALIZAÇÃO | 2 | HDT out/2023, HETRIN ago/2025 |
| ERRO DE EXTRAÇÃO | 1 | HUGO abr/2025 (já resolvido) |
| ANOMALIA POTENCIAL | 4 | CORA nov/2025 e jan/2026; CREDEQ fev–mar/2020 |

**Ações recomendadas:**
- **CORA nov/2025 e jan/2026**: solicitar à SES os boletins de produção mensais com número de cirurgias e internações realizadas. Se produção for baixa sem justificativa clínica, acionar auditoria de campo.
- **CREDEQ fev–mar/2020**: cruzar com registros de internações do CNES e histórico de ocupação. Hipótese COVID-19 é plausível e, se confirmada, encerra o caso sem auditoria adicional.
- **HDT out/2023**: confirmar número de cirurgias registradas no SIGSS/CNES antes de qualquer escalada.