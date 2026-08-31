# Análise — Fabio Lima da Silva Ribeiro (`FLSRib`)

**Projeto:** Chatbot de Atendimento a Trouble Tickets com Análise de Sentimento via Redes Neurais
**Repositório:** [FLSRib/NeuralNetwork](https://github.com/FLSRib/NeuralNetwork) — pasta `chatbot-atendimento-CRM/`
**Arquivos analisados:** `04-chatbot-trouble-tickets-sentimento.ipynb`, `README.md`, `requirements.txt`, `chatbot_tickets.py` (estrutura), `apresentacao_3pages_chatbot_trouble_tickets.pptx` (3 slides)

O repositório contém mais 3 pastas (`Neural_Network_Playground`, `mini-llm-litBR-playground`, `word-prediction-playground`) que são, de fato, playgrounds exploratórios sem apresentação correspondente — não fazem parte da avaliação, mas mostram que você explorou o conteúdo do curso além do trabalho final.

---

## 1. Abertura

Fabio, parabéns por concluir o projeto! Como Engenheiro de Telecomunicações e Tech Leader em Inovação e Chaos Engineering, atuando na área de Engenharia e no conselho de IA da empresa, faz todo sentido você ter escolhido justamente automatizar e priorizar trouble tickets — é um problema que você provavelmente vive de perto na operação de NOC/suporte técnico, e a lente de chaos engineering (pensar em falhas, escalonamento e criticidade) aparece na forma como o chatbot prioriza tickets por sentimento. O chatbot de trouble tickets com escalonamento por sentimento é uma ideia de produto bem definida e o fluxo conversacional está claramente pensado; falta agora aterrissar essa ideia em números de negócio e em uma validação mais rigorosa do modelo.

## 2. Resumo do projeto

O projeto implementa um chatbot que consulta o status de Trouble Tickets de uma central NOC/telecom e, quando o cliente digita uma mensagem adicional, classifica o sentimento (`negativo`, `positivo`, `neutro`) usando `TfidfVectorizer` + `MLPClassifier` (1 camada oculta de 32 neurônios), acionando escalonamento ao NOC Nível 2 em caso de sentimento negativo. Todos os dados — tanto a base de tickets quanto o corpus de treinamento de sentimento — são sintéticos, gerados programaticamente pelo próprio aluno. Não há comparação com nenhum modelo de baseline (ML tradicional ou regra simples) no notebook.

## 3. Nota por critério

### Critérios de negócio (peso maior)

**1. Aderência ao negócio — 1,7/10**
1.1. Métrica de sucesso nomeada como receita/custo: **3** — o slide de Conclusão do pptx fala em "retenção da planta" e "reduzir risco de churn", que é uma métrica de receita/retenção, mas nunca é nomeada como tal de forma direta (ex: "reduzir churn em X p.p." ou "custo evitado").
1.2. Métrica quantificada: **1** — nenhum número de churn, receita ou custo aparece em nenhum lugar (README, notebook ou pptx).
1.3. Conexão entre métrica técnica e impacto de negócio: **1** — a acurácia de 98,9% do MLP e o score de confiança nunca são traduzidos em "quantos tickets seriam escalonados corretamente" ou "quanto isso evita em churn/SLA"; a ausência é total (não indício fraco), o que corresponde a nota 1 na escala Likert do critério.

**2. Viabilidade econômica (ROI) — 0,0/10**
2.1. Custo de construção estimado: **1** — ausente em README, notebook e pptx.
2.2. Custo de sustentação estimado: **1** — ausente; não há qualquer menção a custo de reprocessamento, retraining ou infraestrutura de produção.
2.3. Retorno esperado com número: **1** — ausente.
2.4. Comparação custo vs. retorno: **1** — ausente; nenhum payback, ROI% ou breakeven é mencionado.

### Critérios técnicos (peso menor)

**3. Necessidade real de IA — 7,5/10**
3.1. Discute alternativa de automação/regra determinística: **4** — o slide "A limitação atual" do pptx afirma explicitamente: *"Consultar status e aplicar regras fixas não revela, por si só, o contexto emocional do cliente nem orienta a ação de forma consistente e auditável."* É uma discussão real, mas breve, presente só no pptx (não no notebook) e sem comparar custo/precisão de uma alternativa simples (ex: lista de palavras-chave negativas).

**4. ML tradicional vs. Redes Neurais — 0,0/10**
4.1. Compara explicitamente contra ML tradicional: **1** — não há qualquer menção a Naive Bayes, Regressão Logística ou análise de sentimento baseada em léxico, nem no notebook nem no pptx.
4.2. Baseline simples de fato executado e comparado: **1** — não existe nenhuma célula de baseline no notebook; o `MLPClassifier` é avaliado sozinho, sem ponto de comparação.

**5. Aderência ao conteúdo do curso — 5,0/10**
5.1. Nomeia arquitetura vista em aula: **5** — `MLPClassifier(hidden_layer_sizes=(32,), activation='relu', ...)` (célula 8 do notebook), MLP é conteúdo da Aula 2/3.
5.2. Arquitetura adequada ao tipo de dado: **3** — TF-IDF + MLP é uma combinação clássica e funcional para texto, mas é exatamente o ponto de partida "estatístico" que a Aula 5 (Da Estatística aos Embeddings) descreve como anterior às representações vetoriais mais ricas.
5.3. Se o problema é de texto, usa embeddings ou atenção: **1** — o projeto usa apenas `TfidfVectorizer(max_features=500, ngram_range=(1,2))` (célula 8) — nenhum embedding (Word2Vec/GloVe/BERT) nem mecanismo de atenção (Aula 5/6) é utilizado; é literalmente uma MLP genérica sobre representação estatística de bag-of-words, o cenário que a rubrica sinaliza como insuficiente.

**6. Aderência ao template de projeto — 3,75/10**
6.1. Cobre os 7 blocos do `templates_projetos_ia.md`: **4** — presentes: (1) Visão Geral (pptx, slides "O desafio atual"/"A limitação atual"/"A visão com IA"); (2) Coleta e Preparação de Dados (notebook, seções 2-3, dados sintéticos de tickets e de sentimento); (3) Estratégia de Bases e Separação (célula 8, `train_test_split` 75/25 estratificado); (4) Seleção de Algoritmos (MLP justificado no README seção 7, sem comparação com alternativas); (5) Estratégia de Treinamento (célula 8, `max_iter=500`, `random_state=42`, mas sem busca de hiperparâmetros); (6) Testes e Métricas (célula 8-9, acurácia + classification_report + matriz de confusão, mas sem matriz de impacto de negócio nem teste de viés/generalização). Ausente: (7) MLOps — não há qualquer menção a estratégia de deploy, monitoramento ou drift em README, notebook ou pptx. 6/7 blocos presentes (vários de forma superficial) → nota proporcional 4.
6.2. Profundidade do bloco 7 (MLOps): **1** — confirmado por leitura direta do `README.md` (a seção numerada "7" existente ali é "Arquitetura da Rede Neural", não MLOps) e por busca de palavras-chave (`MLOps`, `monitor`, `drift`, `deploy`, `retrain`, `produção`) no notebook `04-chatbot-trouble-tickets-sentimento.ipynb` e no texto extraído do `apresentacao_3pages_chatbot_trouble_tickets.pptx`: nenhuma menção a estratégia de implantação, monitoramento de drift, frequência de retreino ou critério de revisão/aposentadoria do modelo em nenhum dos três documentos — o bloco 7 está simplesmente ausente do projeto.

**7. Correção técnica — 7,5/10**
7.1. Código executa sem erro: **5** — confirmado; `execution_count` sequencial de 1 a 10 em todas as células de código, sem saída de erro.
7.2. Split antes de pré-processamento: **5** — `train_test_split` (célula 8) executado antes de `vectorizer.fit_transform(X_train)`; `X_test` só passa por `.transform()`, sem vazamento.
7.3. Métrica adequada à distribuição: **5** — dataset perfeitamente balanceado (120 exemplos por classe) e `classification_report` (precision/recall/f1 por classe) é reportado, adequado.
7.4. Baseline avaliado no mesmo split: **1** — não se aplica porque não existe baseline algum no notebook (consistente com a nota 0 em "ML tradicional vs. Redes Neurais").

**8. Qualidade do código — 10,0/10**
8.1. Seeds fixadas: **5** — `RANDOM_STATE = 42`, `random.seed(RANDOM_STATE)`, `np.random.seed(RANDOM_STATE)` (célula 2) e propagado ao `MLPClassifier(random_state=RANDOM_STATE)` (célula 8).
8.2. Dependências declaradas: **5** — `requirements.txt` presente e versionado (numpy, pandas, scikit-learn, matplotlib, jupyter).
8.3. Organização em funções/seções: **5** — notebook segmentado em 8 seções markdown (numeração 0, 2-8 — a numeração não é contígua, o aluno pulou a seção "1") e lógica encapsulada em funções reutilizáveis (`consultar_ticket`, `classificar_sentimento_texto`, `registrar_em_arquivo_csv`, `executar_fluxo_chatbot`, `gerar_variacoes_suporte`), sem duplicação relevante.

**9. Honestidade dos resultados — 0,0/10**
9.1. Múltiplas seeds/execuções ou justificativa: **1** — acurácia de 98,9% (célula 8) obtida em uma única execução, sobre um corpus sintético gerado por template (16/16/12 frases-base por classe — negativas/positivas/neutras, respectivamente — combinadas com poucos prefixos/sufixos fixos — célula 6), o que infla artificialmente a separabilidade das classes; nenhuma validação cruzada, nenhuma segunda seed, nenhum teste com dados fora do padrão de geração.
9.2. Seção de limitações presente: **1** — ausente em README, notebook e pptx; em nenhum momento o projeto reconhece que o corpus de treino é sintético/templated e que a acurácia de ~99% não se sustenta necessariamente em mensagens reais de clientes.

## 4. Pontos fortes

- **7.2 Split antes de pré-processamento** (5/5): `train_test_split` (célula 8) executado antes de `vectorizer.fit_transform(X_train)`; `X_test` só passa por `.transform()`, sem vazamento.
- **8.1 Seeds fixadas** (5/5): `RANDOM_STATE = 42`, `random.seed(RANDOM_STATE)`, `np.random.seed(RANDOM_STATE)` (célula 2), propagado ao `MLPClassifier(random_state=RANDOM_STATE)` (célula 8).
- **8.2 Dependências declaradas** (5/5): `requirements.txt` presente e versionado (numpy, pandas, scikit-learn, matplotlib, jupyter).
- **8.3 Organização em funções/seções** (5/5): notebook segmentado em 8 seções markdown (numeração 0, 2-8 — a numeração não é contígua, o aluno pulou a seção "1") e lógica encapsulada em funções reutilizáveis (`consultar_ticket`, `classificar_sentimento_texto`, `registrar_em_arquivo_csv`, `executar_fluxo_chatbot`, `gerar_variacoes_suporte`), sustentando um fluxo conversacional completo — consulta de ticket, classificação de sentimento e escalonamento condicional, com auditoria em CSV (`registro_sentimentos_tickets.csv`) — sem duplicação relevante.

## 5. Pontos de melhoria

- **2.4 Comparação custo vs. retorno** (1/5): nenhum payback ou ROI% calculado — é o item de maior peso na rubrica e o que mais penaliza a nota final.
- **2.1/2.2 Custo de construção e sustentação** (1/5): sem estimativa de custo de dados reais, treino, integração ao NOC, retraining ou infraestrutura de produção — ausente em README, notebook e pptx.
- **1.2 Métrica quantificada** (1/5): nenhum número de churn, receita ou custo evitado aparece em nenhum documento do projeto — mesmo a menção a "retenção da planta" no pptx fica sem qualquer quantificação.
- **6.2 Profundidade do bloco 7 (MLOps)** (1/5, novo): o bloco de MLOps está completamente ausente do README, do notebook e do pptx — nenhuma estratégia de implantação, monitoramento de drift ou critério de retreino é definida, o que derrubou a nota do critério 6 de 7,5 para 3,75/10.

## 6. Nota final

**3,0 / 10** — O chatbot funciona tecnicamente (código limpo, sem vazamento, seeds fixadas), mas o trabalho não sustenta nenhuma das duas dimensões que mais pesam na rubrica: não há qualquer estimativa de custo/retorno (ROI = 0) e a métrica de negócio nunca é quantificada; no lado técnico, a ausência total de baseline e uma acurácia de ~99% obtida sobre dados sintéticos templated e uma única execução, sem seção de limitações, são sinais de honestidade de resultados que precisam ser corrigidos antes de qualquer outra evolução.

**Nível de maturidade: PoC/protótipo.** Todos os sub-itens de viabilidade econômica (2.1-2.4) e o novo 6.2 (profundidade do bloco de MLOps) tiraram nota 1 — não há nenhuma estimativa de custo, retorno ou estratégia de monitoramento/retreino em nenhum documento do projeto. O chatbot existe apenas como demonstração de fluxo conversacional em notebook/script local; falta toda a base (custo, retorno, plano de deploy e monitoramento) para sequer cogitar um piloto controlado.

## 7. Task list para evoluir o trabalho

**1. Aderência ao negócio**
- [ ] **1.1 Métrica de sucesso nomeada como receita/custo (3/5):** o Bloco B é direto — "Qual métrica de negócio define sucesso? Não acurácia técnica — receita, custo evitado, tempo economizado, risco reduzido." O pptx já aponta na direção certa ao falar em "retenção da planta" e "reduzir risco de churn" (slide de Conclusão), mas isso ainda precisa virar uma métrica nomeada explicitamente como receita ou custo evitado (ex: "reduzir churn em X p.p." ou "evitar R$ Y/mês em retrabalho de SLA"). — ver slide "CONCLUSÃO / Valor estratégico" do pptx
- [ ] **1.2 Métrica quantificada (1/5):** o Bloco D recomenda usar placeholders visíveis quando não há o dado exato: "utilize placeholders visíveis como [Inserir % de economia]... em vez de inventar números irreais." Nenhum número aparece hoje em nenhum documento do projeto; formalize algo como `[Inserir nº de tickets/mês] × [Inserir % de churn evitado] × [Inserir ticket médio ou custo de SLA]` em vez de deixar a métrica só qualitativa. — ausente em README, notebook e pptx
- [ ] **1.3 Conexão entre métrica técnica e impacto de negócio (1/5):** o Bloco D pede para "traduzir a complexidade técnica em valor financeiro e operacional" — a acurácia de 98,9% e o score de confiança do MLP (célula 8-9) nunca viram um número de negócio. Um caminho concreto, no espírito do que `01-deteccao-fraude.ipynb` (célula 21) faz ao ponderar custo assimétrico de FP/FN: aqui, um falso negativo é uma mensagem negativa não escalonada (risco de churn/SLA) e um falso positivo é um escalonamento desnecessário ao NOC N2 (custo operacional) — pondere os dois e estime quantos tickets/mês seriam corretamente escalonados. — ver célula 8-9 do notebook

**2. Viabilidade econômica (ROI)**
- [ ] **2.1 Custo de construção (1/5):** o Bloco C trata isso como "custo computacional — treino e inferência têm custo, meça contra o orçamento disponível" e "tempo de treinamento". Como todo o corpus de sentimento é sintético (célula 6, `gerar_variacoes_suporte`), o maior custo real de construção seria coletar/rotular mensagens reais de clientes — estime isso, além do custo de treino do MLP e de integração ao sistema de tickets do NOC. — ausente em README, notebook e pptx
- [ ] **2.2 Custo de sustentação (1/5):** o Bloco B contrasta automação com IA — "atualiza-se a regra manualmente" vs. "retreina-se o modelo periodicamente" — esse é exatamente o custo recorrente que falta: frequência de retreino do MLP à medida que o vocabulário de tickets muda, e custo de monitorar a qualidade da classificação em produção. — ausente em README, notebook e pptx
- [ ] **2.3 Retorno esperado com número (1/5):** o Bloco D chama isso de "Métrica-Alvo de Negócio: a métrica que traduz o resultado estatístico em dinheiro", com a mesma recomendação de placeholder citada em 1.2 — formalize o retorno como `[Inserir % de churn evitado] × [Inserir ticket médio ou custo de SLA]`, mesmo que hipotético, em vez de deixar a seção "Valor estratégico" do pptx sem nenhum número. — ver slide "Valor estratégico" do pptx
- [ ] **2.4 Comparação custo vs. retorno (1/5):** o Bloco C fecha o raciocínio de seleção de algoritmo com "um modelo mais complexo só se justifica se o ganho superar o custo". Depois de estimar 2.1/2.2 (custo) e 2.3 (retorno), calcule `ROI = (retorno - custo) / custo` ou um payback em meses — o curso não formaliza essa fórmula específica, mas a régua "o ganho supera o custo?" já basta para justificar o MLP frente a uma alternativa mais simples. — ausente em todo o material

**3. Necessidade real de IA**
- [ ] **3.1 Discute alternativa de automação/regra determinística (4/5):** o Bloco B traz o teste direto: "a lógica pode virar regras fixas (se-então)? Há dados históricos suficientes? Três "sim" seguidos = provavelmente um projeto de IA — se não, automação simples resolve com menos custo." Você já tem essa discussão no slide "A limitação atual" do pptx, mas ela não aparece no notebook nem é testada na prática. O curso ilustra esse teste em `aplicacoes-de-negocio/04-chatbot-atendimento.ipynb` (célula 11 — a célula 10 é só a introdução em markdown), que usa um dicionário simples de palavras boas/ruins como baseline — implemente algo equivalente (ex: lista de palavras negativas/positivas) e compare precisão/custo contra o MLP. — ver slide "A limitação atual" do pptx; nenhuma menção no notebook

**4. ML tradicional vs. Redes Neurais**
- [ ] **4.1 Compara explicitamente contra ML tradicional (1/5):** o Bloco C recomenda "comece sempre por um baseline simples. Se ele já resolve, um modelo mais complexo só se justifica se o ganho superar o custo" — nem Regressão Logística, Naive Bayes nem um léxico de sentimento são mencionados como alternativa ao MLP em nenhum documento. — ausente em README, notebook e pptx
- [ ] **4.2 Baseline simples de fato executado e comparado (1/5):** o mesmo princípio do Bloco C citado em 4.1 vale aqui — treine um baseline de fato (ex: `LogisticRegression` sobre o mesmo `TfidfVectorizer`, ou o dicionário de palavras do exemplo `04-chatbot-atendimento.ipynb` célula 11) no mesmo split já criado na célula 8, e reporte a comparação de acurácia/f1 lado a lado com o MLP. — ver célula 8 do notebook (`04-chatbot-trouble-tickets-sentimento.ipynb`)

**5. Aderência ao conteúdo do curso**
- [ ] **5.2 Arquitetura adequada ao tipo de dado (3/5):** a própria Aula 5 descreve a progressão do curso: "começar pelo modelo mais simples (contagens estatísticas), sentir suas limitações na prática, e só então introduzir a próxima arquitetura como resposta a essa limitação — até chegar aos embeddings, a forma como redes neurais modernas representam palavras como vetores de números." Seu TF-IDF (célula 8) é exatamente esse ponto de partida estatístico — vale reconhecer essa limitação explicitamente no projeto e, se possível, comparar contra pelo menos um embedding simples. — ver célula 8 do notebook
- [ ] **5.3 Usa embeddings ou atenção, se o problema é de texto (1/5):** mesma citação da Aula 5 acima — o projeto usa apenas `TfidfVectorizer(max_features=500, ngram_range=(1,2))` (célula 8), sem avançar para Word2Vec/GloVe/FastText/BERT (Aula 5) nem mecanismos de atenção (Aula 6). Como o corpus de sentimento é pequeno e sintético, mesmo um embedding pré-treinado simples tende a generalizar melhor que bag-of-words para mensagens reais de clientes. — ver célula 8 do notebook

**6. Aderência ao template de projeto**
- [ ] **6.1 Cobre os 7 blocos do template (4/5):** falta só o bloco 7 (MLOps) para completar 7/7 — ver dica detalhada em 6.2 abaixo. Os outros 6 blocos já estão presentes, mas vários de forma superficial (ex: bloco 4 sem comparação de alternativas, bloco 6 sem matriz de impacto de negócio) — vale revisar cada um à luz das dicas de 1.x-5.x acima. — ver README.md e notebook
- [ ] **6.2 Profundidade do bloco 7/MLOps (1/5, novo):** o `templates_projetos_ia.md` define esse bloco como "Estratégia de Implantação: como o modelo será consumido (API REST, processamento em lote)" e "Monitoramento Contínuo: como será monitorado o Data Drift e o Concept Drift" — nenhum desses dois pontos aparece no README, no notebook ou no pptx. Como ponto de partida, descreva como o `MLPClassifier` seria servido no fluxo real do chatbot (ex: API interna consumida pelo `chatbot_tickets.py`), com que frequência ele seria retreinado à medida que o vocabulário de tickets muda, e um critério numérico de quando revisar o modelo (ex: "retreinar se a taxa de escalonamentos incorretos reportados pelo NOC N2 ultrapassar X% no mês"). — ausente em README.md, no notebook e no pptx

**7. Correção técnica**
- [ ] **7.4 Baseline avaliado no mesmo split (1/5):** consequência direta de 4.1/4.2 — não há baseline para avaliar. Assim que implementar o baseline (4.2), garanta que ele use exatamente o mesmo `X_train`/`X_test` já produzidos pelo `train_test_split` da célula 8, para a comparação ser justa. — ver célula 8 do notebook

**9. Honestidade dos resultados**
- [ ] **9.1 Múltiplas seeds/execuções ou justificativa (1/5):** o Bloco A é direto — "cada comparação foi rodada com 3 sementes aleatórias diferentes, para separar ganho real de sorte da rodada" — e mostra casos reais onde isso muda a conclusão (ex: CNN variando de 40% a 83% de acurácia conforme a seed). O notebook `09-score-credito.ipynb` (células 22-25) faz esse teste e conclui literalmente que "um vencedor que só vence em uma seed não é um vencedor confiável"; `01-deteccao-fraude.ipynb` (células 22-25) faz o mesmo teste de múltiplas seeds, mas com um achado próprio — o MLP colapsa em 2 das 3 seeds testadas, sem usar essa frase exata. Sua acurácia de 98,9% é ainda mais suspeita por vir de um corpus sintético templated (célula 6) em execução única. Repita o treino do MLP com pelo menos 3 seeds (ex: 42, 7, 123) e teste também com frases fora do padrão de geração das 16/16/12 frases-base por classe, para separar desempenho real de memorização do template. — ver célula 6 (`gerar_variacoes_suporte`) e célula 8
- [ ] **9.2 Seção de limitações presente (1/5):** o curso não tem um tópico específico sobre "seção de limitações" como formato (é mais prática de honestidade científica do que conteúdo de IA de negócio), mas o espírito é o mesmo do Bloco A citado em 9.1 — separar o que foi de fato validado do que é só demonstração. Adicione uma seção explícita reconhecendo que o corpus de treino é sintético/templated e que a acurácia de ~99% não necessariamente se sustenta em mensagens reais de clientes. — ausente em README.md, no notebook e no pptx

## 8. Tópicos para o aluno revisar

- **ROI e viabilidade econômica de projetos de IA** (Bloco C — Design de Projetos de IA / `templates_projetos_ia.md`, bloco MLOps) — motivado pela ausência total de qualquer número de custo ou retorno no `README.md` e no pptx: o template pede explicitamente essa análise, e ela não aparece em nenhum documento do projeto.
- **Validação de robustez / múltiplas execuções** (Bloco C — Design de Projetos de IA) — motivado pela célula 8 do notebook: 98,9% de acurácia em execução única sobre corpus sintético templated é exatamente o tipo de resultado que a disciplina pede para desconfiar antes de reportar como conclusivo.
- **Baseline e ML tradicional antes de redes neurais** (Bloco B — Redes Neurais / `aplicacoes-de-negocio/`) — motivado pela ausência completa de comparação no notebook: os 13 notebooks de referência do curso sempre comparam a rede neural contra um baseline mais simples, o que não foi replicado aqui.
- **Da Estatística aos Embeddings** (Aula 5) — motivado pela célula 8 (`TfidfVectorizer`): o projeto para no estágio "estatístico" (TF-IDF) descrito como ponto de partida na Aula 5, sem avançar para embeddings densos, que teriam melhor capacidade de generalização para linguagem natural real de clientes.
- **Mecanismos de Atenção e Transformers** (Aula 6) — motivado pela escolha de uma MLP genérica sobre TF-IDF para o problema de sentimento: vale revisitar por que arquiteturas com atenção lidam melhor com contexto textual do que uma MLP sobre bag-of-words.
