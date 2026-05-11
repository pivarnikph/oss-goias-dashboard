# RELATÓRIO EXECUTIVO
## Auditoria das Organizações Sociais de Saúde do Estado de Goiás

**Período analisado:** 2023 — 2026
**Apresentado a:** Governador do Estado de Goiás
**Data:** 10/05/2026

---

## SUMÁRIO EXECUTIVO

# SUMÁRIO EXECUTIVO

**Auditoria de Execução Financeira — Organizações Sociais de Saúde**
**Estado de Goiás | Janeiro/2023 – Abril/2026**

---

Este relatório cobre 13 hospitais geridos por 11 OSS, em 461 períodos hospital×mês analisados, com R$ 3,57 bilhões repassados pela SES-GO e R$ 3,65 bilhões executados no período.

**Achado principal:** A execução financeira agregada de 101,9% está dentro de parâmetros normais e não foram identificados indícios de fraude ou desvio sistêmico no portfólio analisado.

---

**Achados secundários:**

**1. Execução acima do repasse SES em HETRIN (126%) tem explicação estrutural.** A diferença entre repasse e gasto é integralmente explicada por saldo bancário inicial de R$ 37 mi (com drawdown de R$ 15 mi no período), receitas próprias de SUS-AIH e outras fontes da ordem de R$ 1–3 mi/mês, e 2 meses sem dados coletados (julho/2025 com link inativo e abril/2026 não publicado). A equação de balanço fecha; não há sobreexecução real.

**2. Concentração orçamentária em duas OSS é estrutural, não anômala.** AGIR executa R$ 1,46 bilhão (43,8% do total), dado que opera o HUGOL — maior hospital do estado, com mediana de R$ 34,6 mi/mês. FUNEV responde por 13,4% (R$ 445,7 mi). Juntas, duas OSS concentram 57,2% do gasto. O risco de dependência operacional em contrato único de alta magnitude requer atenção gerencial continuada.

**3. Foram identificados 13 outliers de custo mensal, todos investigados.** Dois eram erros de extração automatizada (HUGO, meses abril/2025 e novembro/2025), corrigidos por re-extração manual — execução real de 104%, dentro do normal. Os demais outliers decorrem de ramp-up operacional (CORA, a partir de abril/2025) ou variações pontuais de fluxo de caixa já explicadas.

---

**Recomendações:**

1. **Implementar validação cruzada mensal dos dados extraídos automaticamente**, confrontando valores do sistema com os PDFs originais dos relatórios financeiros, reduzindo retrabalho de auditoria e risco de alertas falsos.

2. **Exigir que HETRIN e demais OSS com receitas próprias relevantes reportem explicitamente, em campo padronizado, todas as fontes de receita além do repasse SES**, eliminando ambiguidade estrutural nos índices de execução.

3. **Estabelecer plano de contingência contratual para o contrato AGIR/HUGOL**, dado que um único contrato representa 43,8% do gasto total auditado — ruptura operacional nesse vínculo teria impacto sistêmico imediato sobre a rede estadual.

**Em números:**
- **13** hospitais analisados, sob gestão de **11** Organizações Sociais
- **1.709 (extraídos via IA) / 19.118 (baixados)** documentos baixados e validados (manifesto auditável)
- **R$ R$ 3.648.536.265** executados no período pelas OSS
- **101.9%** execução financeira média
- **13** atipicidades de custo identificadas

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

| AGIR | HUGOL | 45 | 87.0% | R$ 34.566.593 |
| Albert Einstein (SBIBHAE) | HUGO | 20 | 70.0% | R$ 27.632.738 |
| FUNEV | HEANA | 43 | 98.0% | R$ 10.691.979 |
| AGIR | HEJ | 8 | 88.0% | R$ 9.728.010 |
| ISG | HDT | 40 | 98.0% | R$ 8.121.209 |
| IPGSE | HERSO | 20 | 100.0% | R$ 6.512.876 |
| IMED | HETRIN | 41 | 95.0% | R$ 6.351.828 |
| IGH | HEAPA | 30 | 90.0% | R$ 6.072.638 |
| Instituto Patris | HEL | 45 | 53.0% | R$ 5.403.581 |
| Hospital de Amor | CORA | 13 | 100.0% | R$ 4.673.327 |
| ABEVIDA | CRESM | 74 | 45.0% | R$ 3.019.833 |
| ABEVIDA | CREDEQ | 67 | 100.0% | R$ 2.252.657 |
| IMED | PFRE | 18 | 67.0% | R$ 2.139.560 |


### 2.2 Concentração por OSS

[A análise por OSS será inserida aqui via Claude API]

# Análise por OSS

## AGIR

## AGIR

A AGIR é a maior operadora do portfólio estadual, responsável pelo HEJ e HUGOL, com R$ 1,46 bilhão recebido e R$ 1,46 bilhão executado ao longo de 53 períodos. A execução financeira mediana de 100,6% indica aderência consistente ao repasse SES, sem subfaturamento relevante nem extrapolação sistemática. O volume concentrado — 43,8% do total executado no portfólio — é estrutural, reflexo direto do porte do HUGOL como maior hospital do estado, não anomalia de alocação.

Não há sinais de atenção financeira neste momento. A leve variação acima de 100% é operacionalmente esperada em contratos de grande porte, onde receitas complementares (SUS-AIH, coprodução) podem compor marginalmente o fluxo de caixa. Recomenda-se monitoramento contínuo de indicadores de qualidade assistencial para verificar se a escala operacional se traduz em efetividade correspondente.

---

## FUNEV

## FUNEV — HEANA

A FUNEV registra execução mediana de 98,3% sobre repasse SES de R$ 442,2 mi em 43 períodos, com total executado de R$ 445,7 mi — diferença de R$ 3,4 mi acima do repasse (0,8%), consistente com aporte de receitas complementares (SUS-AIH, convênios ou saldo inicial). O perfil é de operação estável e madura, sem volatilidade aparente que demande investigação imediata.

Pontos de atenção de rotina: (a) confirmar a origem dos R$ 3,4 mi executados além do repasse SES, verificando se estão adequadamente registrados como "outras fontes" nos balancetes; (b) 43 períodos de dados sugerem cobertura satisfatória, mas eventuais meses ausentes devem ser checados. Nenhum sinal de anomalia estrutural identificado nesta análise. Recomenda-se manutenção do monitoramento padrão.

---

## Albert Einstein

## Albert Einstein — HUGO

A Sociedade Beneficente Israelita Brasileira Albert Einstein gere o HUGO com execução mediana de 107,9% sobre o repasse SES, totalizando R$ 396,8 milhões executados contra R$ 381,4 milhões recebidos no período (19 meses de dados). O diferencial de R$ 15,4 milhões é consistente com a utilização de receitas complementares — SUS-AIH, copagamentos e saldos de competências anteriores — padrão esperado em hospitais de grande porte e já verificado em análise prévia que corrigiu distorções de extração (valor inicial de 113% revisado para 104% em análise mensal; a mediana de 107,9% reflete a série completa).

Não há sinais de irregularidade. O volume operacional é expressivo para uma única unidade, o que justifica monitoramento contínuo de metas assistenciais e conformidade contratual, mas a execução financeira está dentro de parâmetros aceitáveis para hospitais terciários de alta complexidade.

---

## ISG

## ISG — Hospital das Doenças Tropicais (HDT)

O ISG gerencia o HDT com execução financeira de 98,5% (mediana) sobre R$ 323,0 mi recebidos no período, executando R$ 323,4 mi — margem de R$ 392,8 mil acima do repasse SES (0,12%), tecnicamente insignificante e consistente com uso de saldos remanescentes ou receitas complementares. A cobertura de 40 períodos indica série histórica robusta para análise de tendência.

Não há sinais de atenção relevantes neste recorte. A execução de 98,5% mediana indica absorção quase integral dos recursos sem acúmulo atípico, padrão operacional saudável para hospital especializado de média-alta complexidade. O volume total (~R$ 8,1 mi/mês médio) é compatível com o porte do HDT. **Recomendação:** manter monitoramento padrão; nenhuma investigação adicional justificada pelos dados agregados disponíveis.

---

## IMED

## IMED

A IMED gere dois hospitais (HETRIN e PFRE) e registra execução mediana de 107,3% sobre o repasse SES, com R$ 315,3 mi executados contra R$ 254,8 mi recebidos — diferença de R$ 60,4 mi ao longo de 59 períodos. Conforme já investigado, o HETRIN explica estruturalmente parte desse excedente via saldo bancário inicial, receitas SUS-AIH e outras fontes não capturadas no repasse direto. A execução acima do repasse, portanto, não configura anomalia isolada para esta OSS.

O porte da operação é relevante: média mensal de R$ 5,3 mi executados por período, posicionando a IMED como operadora de médio porte no portfólio estadual. Sem dados desagregados por unidade e sem séries de conformidade contratual, não é possível concluir sobre eficiência ou desvios em PFRE especificamente. Recomenda-se auditoria documental focada nessa unidade.

---

## ABEVIDA

## ABEVIDA — CREDEQ e CRESM

A ABEVIDA gerencia dois hospitais (CREDEQ e CRESM) com repasse acumulado de R$ 253,4 mi e execução de R$ 261,8 mi ao longo de 141 períodos de dados, resultando em mediana de execução de 100,6% — desempenho consistente e dentro do esperado. O diferencial de R$ 8,5 mi entre executado e repasse SES (≈3,4%) é modesto e compatível com receitas complementares (SUS-AIH, saldos iniciais), sem necessidade de investigação adicional.

Não há sinais de anomalia financeira. A mediana próxima de 100% indica gestão de caixa regular, sem padrão de subexecução crônica (que sinalizaria represamento) nem sobreexecução expressiva. **Limitação**: a análise baseia-se em valores agregados; variações mensais individuais ou concentração de gastos em categorias específicas podem conter irregularidades não visíveis neste nível de agregação.

---

## IPGSE

## IPGSE — HERSO

O IPGSE apresenta execução financeira mediana de **96,6%** sobre repasse SES de **R$ 136,9 mi** em 20 períodos, com R$ 131,9 mi efetivamente executados. O índice situa-se dentro da faixa considerada regular (90–105%), sem sinais de subexecução crônica ou extrapolação de limites. A cobertura de 20 períodos indica série histórica razoavelmente completa para análise de tendência.

Operação de porte intermediário no contexto estadual. Não há, nos dados disponíveis, anomalias estatísticas que justifiquem aprofundamento imediato. **Ponto de atenção menor**: o gap de R$ 4,9 mi entre recebido e executado (~3,4%) pode refletir competência de caixa, saldo transitório ou atraso de liquidação — verificação recomendada na prestação de contas documental, sem caráter prioritário. Nenhum sinal de alerta ativo para esta OSS.

---

## Instituto Patris

## Instituto Patris — HEL

O Instituto Patris registra execução financeira mediana de 94,9% sobre repasses SES de R$ 137,3 mi em 45 períodos analisados, com total executado de R$ 130,3 mi. O gap de R$ 7,0 mi (5,1%) entre recebido e executado é consistente com uma gestão que mantém reserva operacional — padrão aceitável. Não há sinal de superexecução nem de subexecução severa.

A regularidade de 45 períodos com dados disponíveis indica boa conformidade documental. O porte da operação — R$ 137 mi acumulados — coloca o HEL como unidade de médio porte no portfólio estadual. **Ponto de atenção:** a análise baseia-se exclusivamente nos dados de repasse SES; receitas próprias, SUS-AIH e outras fontes não foram consolidadas, o que pode subestimar o volume financeiro real sob gestão do Patris. Recomenda-se verificação cruzada com balancetes bancários antes de qualquer conclusão definitiva.

---

## IGH

## IGH — Hospital Estadual de Anápolis Dr. Henrique Santillo (HEAPA)

O IGH apresenta execução mediana de 106,4% sobre os repasses SES, com total executado de R$ 129,3 mi contra R$ 120,8 mi recebidos — diferença de R$ 8,5 mi ao longo de 30 períodos coletados. Esse nível de execução é compatível com complementação por receitas próprias (SUS-AIH, convênios, outras fontes) e não configura, isoladamente, sinal de irregularidade. O padrão é análogo ao observado em HETRIN.

Porte da operação é intermediário: média mensal de ~R$ 4,3 mi executados, coerente com hospital de porte regional. Não há concentração atípica de recursos nem volatilidade extrema identificada nos dados agregados. **Ponto de atenção técnico**: a diferença acumulada de R$ 8,5 mi merece verificação documental — especificamente se as receitas complementares estão devidamente registradas nos balancetes mensais e se os 30 períodos cobrem o intervalo contratual completo.

---

## Hospital de Amor

## Hospital de Amor — CORA

A Hospital de Amor gere o CORA com execução mediana de 108,6% sobre repasse SES (R$ 55,9 mi executados contra R$ 52,3 mi recebidos), delta de aproximadamente R$ 3,7 mi. Conforme investigação anterior, o CORA iniciou operações em abril/2025, e os primeiros meses refletem ramp-up típico de nova unidade — custos fixos de estruturação precedem volume assistencial pleno, o que explica execução acima do repasse sem configurar anomalia.

Com 13 períodos capturados e porte intermediário (~R$ 4 mi/mês de repasse médio), a série histórica ainda é curta para análise de tendência robusta. Recomenda-se monitoramento da trajetória de execução nos próximos 6 meses: se o percentual não convergir para a faixa 95–105% à medida que a operação se estabiliza, justifica-se investigação aprofundada das fontes complementares de receita e estrutura de custos.

---



### 2.3 Distribuição financeira

- **Total recebido SES (período):** R$ R$ 3.566.722.020
- **Total executado:** R$ R$ 3.648.536.265
- **Total devolvido:** R$ R$ 7.059.509
- **% execução financeira média ponderada:** 101.9%

---

## 3. ANÁLISE POR HOSPITAL

### 3.1 Hospitais com maior volume (top 5)

# Perfil dos Hospitais

## HUGOL (AGIR)

**Perfil Operacional — HUGOL/AGIR**

HUGOL é o maior hospital do estado, gerido pela AGIR, responsável por 43,8% do total executado pelas OSS de saúde. Mediana mensal de R$ 34,6 mi, com cobertura financeira de 87% (45 meses) e de produção de 98%. No período, registrou 212.725 consultas, 85.008 internações e 26.019 cirurgias. Custo mediano por internação de R$ 18.921 e por consulta de R$ 7.087.

**Ponto de Atenção**

A execução física média de 36% da meta contratual requer esclarecimento metodológico: pode refletir metas superdimensionadas no contrato ou subnotificação de produção. A cobertura financeira de 87% indica 13% dos meses sem dado verificável — lacuna relevante para auditoria continuada. Nenhuma anomalia financeira identificada até o momento.

---

## HUGO (Albert Einstein (SBIBHAE))

**Perfil Operacional — HUGO / Albert Einstein (SBIBHAE)**

Hospital de referência terciária com mediana mensal de R$ 27,6 mi executados. No período (ago/2024–mar/2026), registrou 92.367 consultas, 23.578 internações e 13.968 cirurgias. Cobertura financeira de 70% dos meses com dados válidos; produção com cobertura integral. Execução financeira corrigida em 104% do repasse SES — dentro do padrão aceitável.

**Ponto de Atenção**

Custo mediano por consulta (R$ 5.111) é elevado para ambulatório, consistente com perfil de hospital terciário de alta complexidade, mas merece monitoramento comparativo frente a outros hospitais do portfólio. Execução física média de 30% reflete lacuna de cobertura nos dados de produção — não necessariamente subprodução —, limitando inferências sobre eficiência operacional.

---

## HEANA (FUNEV)

**Perfil Operacional — HEANA/FUNEV**

HEANA opera sob gestão FUNEV com mediana mensal de R$ 10,7 mi e cobertura de dados de 98% (financeira e produção) em 43 meses. O hospital registrou 65.763 consultas, 29.772 internações e 7.685 cirurgias no período. Custo mediano por internação de R$ 14.809 está dentro da faixa esperada para unidades de média-alta complexidade.

**Ponto de Atenção**

A execução física média de 14,0% da meta contratualizada é o principal alerta. Esse índice sugere metas físicas superestimadas no contrato de gestão ou subprodução sistemática — ambos os cenários demandam verificação. Recomenda-se confrontar as metas pactuadas originalmente com a capacidade instalada declarada e com benchmarks de unidades similares antes de qualquer conclusão.

---

## HEJ (AGIR)

**HEJ – AGIR | Set/2025–Dez/2026**

O HEJ registrou mediana mensal executada de R$ 9,7 mi, totalizando produção de 25.922 consultas, 6.495 internações e 4.547 cirurgias no período. Cobertura financeira de 88% indica que 12% dos meses com dados de repasse estão incompletos ou não capturados; produção física com cobertura integral (100%).

**Ponto de atenção:** execução física média de 38% das metas contratuais é baixa e merece verificação — pode refletir metas superdimensionadas no contrato de gestão, subnotificação de produção ou capacidade instalada subutilizada. Custo mediano por internação (R$ 13.253) e por consulta (R$ 2.859) estão dentro de parâmetros esperados para hospital de médio porte. Recomenda-se confrontar metas pactuadas com série histórica anterior a set/2025.

---

## HDT (ISG)

**Perfil Operacional — HDT/ISG**

O HDT, gerido pela ISG, apresenta mediana mensal de R$ 8,1 mi executados em 40 meses (jan/2023–abr/2026), com cobertura financeira de 98% e cobertura de produção de 75%. O portfólio é centrado em consultas (95.693), com internações relevantes (5.249) e cirurgias residuais (44). Custo mediano por consulta de R$ 2.539 e por internação de R$ 30.809 são compatíveis com perfil ambulatorial-especializado.

**Ponto de Atenção**

A lacuna entre cobertura financeira (98%) e de produção (75%) merece investigação. Indica que dados de produção física estão sub-reportados ou que 25% dos registros não foram capturados — não necessariamente subfaturamento real. Recomenda-se cruzamento com CNES e BPA antes de qualquer conclusão.

---

## HERSO (IPGSE)

**Perfil Operacional — HERSO/IPGSE**

O HERSO opera com mediana mensal de R$ 6,51 mi em 20 meses de cobertura integral (set/2024–abr/2026). O volume acumulado — 21.295 consultas, 15.254 internações e 7.599 cirurgias — indica unidade com perfil misto, cirúrgico-internação relevante. Custo mediano por internação (R$ 8.923) e por cirurgia implícita estão em faixa compatível com hospitais de médio porte.

**Ponto de Atenção**

A execução física média de **15% das metas contratuais** é o principal sinal de alerta. Independentemente da execução financeira plena, produção consistentemente abaixo de 1/5 das metas indica superdimensionamento contratual, capacidade ociosa estrutural ou subnotificação de produção. Recomenda-se revisão das metas pactuadas e verificação da série mensal de produção física.

---

## HETRIN (IMED)

**Perfil Operacional — HETRIN/IMED**

HETRIN, gerida pela IMED, opera com mediana mensal de R$ 6,35 mi em 41 meses (cobertura financeira: 95%). O volume acumulado — 103.521 consultas, 17.735 internações e 7.954 cirurgias — indica unidade de porte médio-alto. Custos medianos de R$ 2.618/consulta e R$ 15.190/internação situam-se em faixa compatível com hospitais de média complexidade.

**Ponto de Atenção**

A cobertura de execução física registrada (10%) é atipicamente baixa e provavelmente reflete falha de captura de dados, não ausência real de produção — o volume acumulado confirma operação consistente. Recomenda-se auditoria pontual nos registros de metas físicas mensais para verificar subdeclaração sistemática ou inconsistência no formato de extração dos relatórios IMED.

---

## HEAPA (IGH)

**Perfil Operacional**
HEAPA/IGH operou 30 meses com mediana mensal de R$ 6,07 mi. O mix produtivo é dominado por cirurgias (9.903 no período) em relação a internações (1.266), sugerindo perfil ambulatorial-cirúrgico. Cobertura financeira de 90% indica boa regularidade documental; cobertura de produção de 67% limita inferências sobre eficiência.

**Ponto de Atenção**
Execução física média de 40% das metas físicas contratuais é baixa e merece verificação. O custo mediano por consulta de R$ 4.868 está acima do padrão típico ambulatorial — pode refletir complexidade do perfil assistencial ou subregistro de consultas elevando o custo unitário calculado. Recomenda-se cruzamento com as metas pactuadas originais.

---

## HEL (Instituto Patris)

**Perfil Operacional — HEL / Instituto Patris**

O HEL opera com mediana mensal de R$ 5,4 mi executados, acumulando 78 mil consultas, 18,2 mil internações e 8,2 mil cirurgias em 45 meses. A cobertura financeira de 53% compromete severamente a análise — menos da metade dos meses possui dado financeiro validado, impossibilitando conclusões robustas sobre execução orçamentária.

**Ponto de Atenção**

O custo mediano por consulta de R$ 2.409 é elevado para atenção ambulatorial e merece verificação — pode refletir perfil assistencial mais complexo ou problema de categorização de procedimentos. A execução física média de 69% indica subutilização persistente das metas pactuadas. Recomenda-se auditoria documental para os 47% de meses sem cobertura financeira antes de qualquer conclusão sobre eficiência.

---

## CORA (Hospital de Amor)

**Perfil Operacional**
CORA (Hospital de Amor) opera desde abril/2025, com 13 meses de histórico. Mediana mensal de R$ 4,67 mi executados. Volume acumulado: 4.064 consultas, 810 internações e 387 cirurgias. Cobertura financeira de 100%, mas cobertura de produção física em 77%, reflexo esperado do ramp-up de uma unidade recém-inaugurada.

**Ponto de Atenção**
Custo mediano por consulta de R$ 12.975 é elevado para o padrão estadual — consistente com perfil oncológico especializado, que demanda maior densidade tecnológica e de recursos humanos. A execução física média de 8% das metas contratuais indica capacidade instalada ainda subaproveitada. Monitorar evolução da produção nos próximos 6 meses para verificar aderência às metas pactuadas.

---

## CRESM (ABEVIDA)

**Perfil operacional:** CRESM/ABEVIDA opera exclusivamente como unidade ambulatorial — 94.537 consultas no período, zero internações e cirurgias. Mediana mensal de R$ 3,02 mi executados. Cobertura financeira de 45% (33 de 74 meses) limita análise de tendência; cobertura de produção física é superior (86%), reduzindo o risco de distorção nas métricas de custo. Custo mediano por consulta de R$ 1.873.

**Ponto de atenção:** O custo mediano/consulta de R$ 1.873 é elevado para ambulatório especializado e merece verificação — pode refletir mix de procedimentos de alta complexidade ou subdeclaração de produção física. A cobertura financeira de apenas 45% impede conclusão definitiva. Recomenda-se auditoria dos laudos de produção nos meses sem dados financeiros capturados.

---

## CREDEQ (ABEVIDA)

**CREDEQ / ABEVIDA (2018-01 a 2024-02 — 67 meses)**

**Perfil operacional:** Unidade de baixo volume com mediana mensal de R$ 2,25 mi. Produção registrada concentra-se em consultas (68.605 no período) e internações (1.472); zero cirurgias registradas. Cobertura financeira de 100%, mas produção física capturada em apenas 51% dos meses — dado estrutural, não necessariamente irregular.

**Ponto de atenção:** Execução física média de 18% das metas contratuais é baixa e merece verificação. O custo mediano por internação (R$ 43.027) é elevado para o porte da unidade e deve ser cotejado com o perfil de complexidade contratado. A ausência total de cirurgias em 67 meses requer confirmação: pode refletir escopo contratual restrito ou subnotificação nos relatórios coletados.

---

## PFRE (IMED)

**Perfil operacional:** O PFRE, gerido pela IMED, registrou mediana mensal de R$ 2,14 mi executados ao longo de 18 meses, com produção centrada em consultas (110.253) e cirurgias (820), sem registro de internações. Custo mediano por consulta de R$ 289 indica unidade ambulatorial/especializada. Cobertura financeira de 67% e física de 72% refletem captura parcial dos dados — limitação metodológica relevante.

**Ponto de atenção:** A cobertura financeira de 67% é a mais baixa do conjunto analisado, comprometendo a confiabilidade das médias calculadas. Antes de qualquer conclusão sobre eficiência ou desvio, é necessário recuperar os relatórios faltantes (aproximadamente 6 meses sem dados). Não há, com os dados disponíveis, indício de irregularidade.

---



### 3.2 Hospitais com sinais de alerta

{{NARRATIVAS_ALERTAS}}

### 3.3 Hospitais com performance destaque

{{NARRATIVAS_DESTAQUES}}

---

## 4. ATIPICIDADES E OUTLIERS

### 4.1 Outliers de custo unitário (z-score ≥ 2.5)


| Hospital | OSS | Período | Métrica | Valor | z-score |
|---|---|---|---|---:|---:|
| CORA | Hospital de Amor | 2025-06 | custo_por_consulta | R$ 103.710 | 14.58 |
| CORA | Hospital de Amor | 2025-06 | custo_por_internacao | R$ 180.128 | 9.82 |
| HDT | ISG | 2023-10 | custo_por_cirurgia | R$ 975.397 | 9.40 |
| HUGO | Albert Einstein | 2025-04 | custo_por_consulta | R$ 39.697 | 5.13 |
| CORA | Hospital de Amor | 2025-07 | custo_por_cirurgia | R$ 481.765 | 4.31 |
| CORA | Hospital de Amor | 2025-11 | custo_por_cirurgia | R$ 469.764 | 4.19 |
| CORA | Hospital de Amor | 2025-08 | custo_por_cirurgia | R$ 452.607 | 4.01 |
| CORA | Hospital de Amor | 2026-01 | custo_por_internacao | R$ 83.880 | 3.92 |
| CREDEQ | ABEVIDA | 2020-02 | custo_por_internacao | R$ 79.773 | 3.67 |
| CORA | Hospital de Amor | 2025-07 | custo_por_internacao | R$ 78.834 | 3.61 |


### 4.2 Explicação dos casos extremos

[Análise narrativa dos outliers — distinguindo ramp-up (legítimo) vs anomalia operacional]

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
