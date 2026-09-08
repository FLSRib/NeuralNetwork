# Análise v2 — Fabio Lima da Silva Ribeiro (`FLSRib`)

**Projeto:** Chatbot de Atendimento a Trouble Tickets com Análise de Sentimento via Redes Neurais
**Repositório:** [FLSRib/NeuralNetwork](https://github.com/FLSRib/NeuralNetwork) — pasta `chatbot-atendimento-CRM_revisado/`
**Arquivos analisados (v2):** `04-chatbot-trouble-tickets-sentimento.ipynb`, `README.md`, `chatbot_tickets.py`, `requirements.txt`
**Nota v1:** 3,0/10 → **Nota v2: 7,2/10**

---

## 1. Abertura

Fabio, esta v2 traz um avanço real e substancial nas duas dimensões que mais pesavam contra você na v1 — viabilidade econômica e comparação com ML tradicional — e o README está muito mais completo e bem argumentado. Ao mesmo tempo, a verificação técnica independente que fiz encontrou dois problemas que preciso que você trate com atenção: o vazamento de dados por quase-duplicidade da v1 continua presente (e ganhou um segundo ponto de vazamento, na validação cruzada), e o quadro de "teste de estresse" do README não reporta 2 dos 6 casos testados no notebook — justamente os 2 que o modelo errou. Trato os dois com detalhe abaixo, porque o segundo ponto pesa diretamente no critério de honestidade, que já era o mais crítico da sua v1.

## 2. O que mudou desde a v1 (verificado de forma independente)

Toda a verificação abaixo foi feita reexecutando o notebook e o `chatbot_tickets.py` do zero (ambiente limpo), refazendo a geração do corpus para auditar sobreposição de frases-base, e recalculando manualmente a aritmética do ROI.

| Item da v1 | Situação na v1 | O que você fez na v2 | Verificado |
|---|---|---|---|
| **4.1/4.2/7.4** Sem comparação com ML tradicional | Só o MLP era avaliado, sem nenhum baseline | `LogisticRegression` treinada sobre os mesmos vetores TF-IDF, avaliada no mesmo split (célula 8), com discussão extensa no README (seção 7) sobre por que a rede neural é preferível | Implementado e reexecutado — a comparação em si (mesmo split, mesmas features) é metodologicamente correta. Ver ressalva na seção 3 sobre os números absolutos estarem inflados. |
| **2.1-2.4** ROI ausente | Nenhuma estimativa de custo, retorno ou payback | Seção 1.1 do README: Capex R$10.000, Opex R$800/mês, ARR retido R$84.000 (10 clientes × R$700/mês × 12), ROI ≈328%, payback "2,8 meses" | ARR retido e ROI conferem exatamente. Payback tem uma ressalva — ver seção 4 abaixo. |
| **6.2** MLOps ausente | Nenhuma menção a deploy, monitoramento ou retreino | Seção 1.3 do README: API REST (FastAPI/Docker), consumo via webhook, loop de feedback do operador do NOC, retreino mensal | Descrição coerente e razoável como plano, ainda sem um limiar numérico de drift (ex: "retreinar se X% dos casos forem sinalizados") — mais qualitativo que o de outros colegas que já quantificaram isso. |
| **9.1/9.2** Execução única, sem seção de limitações, resultado "bom demais" nunca investigado | Acurácia 98,9% em execução única, sem nenhuma seção reconhecendo isso | Adicionou validação cruzada 5-fold, um "Teste de Estresse" com frases fora do padrão, e uma seção explícita "1.4 Limitações Metodológicas" reconhecendo o corpus sintético | Esforço real e visível de investigar robustez — mas ver as duas ressalvas graves nas seções 3 e 4, que mostram que essa investigação não foi levada até o fim e que parte do resultado foi reportada de forma seletiva. |

## 3. Achado técnico central — o vazamento por quase-duplicidade da v1 continua, e ganhou um segundo ponto de vazamento

Este é o mesmo problema que outro colega (Sergio Murakami) teve na v1 dele e corrigiu na v2 — mas aqui ele **não foi corrigido**.

O corpus de sentimento (750 exemplos, 250 por classe) continua sendo gerado a partir de só 24 frases-base por classe, combinadas com 7 prefixos × 8 sufixos (célula 6), e o `train_test_split` (célula 8) continua separando por **exemplo individual**, não por frase-base. Reexecutei a geração e o split exatamente como no notebook e contei a sobreposição: **100% das frases-base do teste (67 de 67) também aparecem no treino** — ou seja, o "teste" é estruturalmente quase idêntico ao treino, variando só saudação/complemento.

Refiz a validação com um split por frase-base (`StratifiedGroupKFold`, garantindo zero sobreposição — a mesma correção que o Sergio aplicou):
- **MLP: acurácia média 0,752, desvio-padrão 0,112** (vs. 1,000/0,000 reportado)
- **LogisticRegression: acurácia média 0,712, desvio-padrão 0,140** (vs. 0,997/0,005 reportado)

A queda de ~25-35 pontos percentuais, e a mudança de um desvio-padrão impossível (0,0000) para um desvio-padrão real (~0,11-0,14), confirma que o "100% de acurácia com desvio-padrão zero" da v2 é o mesmo artefato de vazamento da v1 — só que agora "blindado" por uma validação cruzada de 5 folds que parece rigorosa, mas herda o mesmo defeito estrutural do corpus. Vale notar: a comparação MLP vs. LogReg em si continua válida qualitativamente mesmo sob o split correto (MLP levemente melhor, 0,752 vs. 0,712) — o problema é a magnitude dos números absolutos reportados, não a conclusão de qual modelo é melhor.

**Um segundo ponto de vazamento, novo nesta v2:** ao ler a célula 8 linha a linha, encontrei que a validação cruzada refaz o `fit_transform` do `TfidfVectorizer` sobre **todo o dataset** (`X_all_vec = vectorizer.fit_transform(df_sentimento["texto"])`) antes de rodar `cross_val_score` com o `KFold` — ou seja, o vocabulário/IDF de cada fold de treino já "viu" os documentos do fold de teste correspondente. Isso é uma violação direta do princípio "ajustar o pré-processamento só no treino" (o mesmo item 7.2 da rubrica) e some com precisão, mesmo sem qualquer relação com o problema das frases-base — é um bug técnico à parte, introduzido justamente na tentativa de adicionar rigor.

## 4. Achado de honestidade — omissão seletiva no "Teste de Estresse" do README

Este é o achado mais sério da v2, porque atinge diretamente o critério de honestidade dos resultados.

A célula 20 do notebook testa 6 frases fora do padrão (sarcasmo, abreviações, negação, ambiguidade). O modelo **erra 5 das 6** — só acerta a frase "mensagem mista". Mas a seção "8. Teste de Estresse e Limites do Modelo" do README mostra uma tabela com **apenas 4 linhas**: exatamente os casos 1, 2, 3 e 5 do notebook. Os casos 4 ("Favor checar a latência no roteador core de Curitiba" — esperado neutro, previsto NEGATIVO) e 6 ("Vocês pretendem lançar suporte a IPv6 este ano?" — esperado neutro, previsto NEGATIVO) **não aparecem em lugar nenhum do README**.

Busquei em todo o repositório (notebook, `chatbot_tickets.py`, histórico de commits) por qualquer versão anterior do teste de estresse com só 4 frases que explicasse isso como uma atualização incompleta — **não existe nenhum artefato desse tipo**. A tabela do README é um subconjunto das 6 frases do notebook, e o subconjunto excluído é exatamente os 2 únicos casos rotulados "neutro" testados — ambos errados. Isso faz a seção parecer "3 erros em 4 mostrados" quando o teste real teve "5 erros em 6" — e esconde que 100% dos casos "neutro" testados falharam.

Não estou afirmando fabricação de dados (ao contrário do caso do Roberto — aqui os números salvos no notebook são reais, resultado de execução genuína do modelo). Mas reportar seletivamente só os casos favoráveis (ou menos desfavoráveis) de um teste desenhado justamente para "validar a honestidade científica" (palavras do próprio README, seção 8) é uma forma de comprometer a honestidade dos resultados — e ela contradiz o espírito da sua própria seção "1.4 Limitações Metodológicas", que promete transparência.

## 5. Nota por critério (atualizada)

### Critérios de negócio (peso maior)

**1. Aderência ao negócio — 9,2/10** *(v1: 1,7/10)*
1.1. Métrica de sucesso nomeada como receita/custo: **5** *(v1: 3)* — churn e ARR agora nomeados e quantificados diretamente (seção 1.1 do README).
1.2. Métrica quantificada: **5** *(v1: 1)* — 20%→19% de churn, R$84.000 de ARR retido, todos com premissas explícitas.
1.3. Conexão entre métrica técnica e impacto de negócio: **4** *(v1: 1)* — a seção 7.2 ("Calibração de Risco") conecta o recall da classe negativo ao custo de churn de forma concreta, embora ainda qualitativa na ponderação exata do trade-off FP/FN.

**2. Viabilidade econômica (ROI) — 8,1/10** *(v1: 0,0/10)*
2.1. Custo de construção estimado: **5** — R$10.000 detalhado (curadoria + integração via webhook).
2.2. Custo de sustentação estimado: **5** — R$800/mês (auditoria humana e monitoramento).
2.3. Retorno esperado com número: **4** — R$84.000/ano bem fundamentado, mas a coincidência entre "redução relativa de 5% no churn" e "queda de 20% para 19%" só bate porque os dois números foram escolhidos para coincidir (5% de 20% = 1 p.p. exatamente) — não é um erro, mas vale registrar que não é uma dedução, é uma escolha de premissas convenientes.
2.4. Comparação custo vs. retorno: **3** *(v1: 1)* — o ROI% (328%) está correto, mas o "Payback de 2,8 meses" só é reproduzível por uma fórmula não-convencional ((Capex+Opex anual)/ARR×12) que mistura custo recorrente com investimento único; um payback tradicional (capex ÷ retorno líquido mensal) daria ≈1,6 meses. Não é erro de conta, mas é uma métrica não-padrão apresentada como se fosse a definição usual de payback, sem essa ressalva.

### Critérios técnicos (peso menor)

**3. Necessidade real de IA — 7,5/10** *(mantido)*
3.1 permanece em 4/5 — a discussão de personas (seção 1.2 do README) ficou mais elaborada, mas continua só no README, sem teste prático de uma alternativa por regras.

**4. ML tradicional vs. Redes Neurais — 10,0/10** *(v1: 0,0/10)*
4.1. Compara explicitamente contra ML tradicional: **5** — `LogisticRegression` implementada e discutida em profundidade (seção 7 do README).
4.2. Baseline simples de fato executado e comparado: **5** — mesmo split, mesmas features TF-IDF, ambos avaliados lado a lado (célula 8).

**5. Aderência ao conteúdo do curso — 5,8/10** *(v1: 5,0/10)*
5.2. Arquitetura adequada ao tipo de dado: **4** *(v1: 3)* — a seção 8.1 do README ("Roadmap de NLP") justifica TF-IDF+MLP como escolha deliberada de "PoC leve" com baixa latência, com um roteiro explícito para embeddings/BERTimbau como próximo passo — mais consciente que a v1.
5.3. Uso de embeddings/atenção: **1** *(mantido)* — continua ausente, corretamente reconhecido como próxima etapa.

**6. Aderência ao template de projeto — 8,75/10** *(v1: 3,75/10)*
6.1. Cobre os 7 blocos: **5** *(v1: 4)* — MLOps agora presente, completando os 7 blocos.
6.2. Profundidade do bloco 7 (MLOps): **4** *(v1: 1)* — estratégia de deploy, webhook e retreino mensal descritos com coerência, mas sem um limiar numérico de quando disparar retreino por drift (diferente de colegas que já quantificaram isso, ex: "retreinar se X% dos casos forem sinalizados pelo NOC").

**7. Correção técnica — 8,75/10** *(v1: 7,5/10)*
7.1. Código executa sem erro: **5** *(mantido)* — confirmado de forma independente, notebook e `chatbot_tickets.py` reexecutados do zero, sem erro.
7.2. Split antes de pré-processamento: **3** *(v1: 5)* — a divisão treino/teste original está corretamente ordenada (`fit` só no treino), mas a nova célula de validação cruzada reajusta o `TfidfVectorizer` sobre **todo o dataset** antes do `cross_val_score` — um vazamento direto de informação do fold de teste para o vocabulário/IDF de cada fold, introduzido justamente na tentativa de adicionar rigor estatístico. Ver seção 3 acima.
7.3. Métrica adequada à distribuição: **5** *(mantido)* — classes balanceadas, `classification_report` usado corretamente.
7.4. Baseline avaliado no mesmo split: **5** *(v1: 1)* — `LogisticRegression` e MLP avaliados sobre exatamente o mesmo `X_test`/`y_test`.

**8. Qualidade do código — 9,2/10** *(v1: 10,0/10)*
Nota à parte: `requirements.txt` não fixa versão exata do scikit-learn (`>=1.3.0`), o que explica uma pequena discrepância (1 exemplo em 188) entre a acurácia da LogReg reportada e a reexecutada — mesma observação feita para outro colega nesta rodada; boa prática de reprodutibilidade ainda ausente.

**9. Honestidade dos resultados — 3,75/10** *(v1: 0,0/10)*
9.1. Múltiplas execuções/seeds: **3** *(v1: 1)* — a validação cruzada de 5 folds é um esforço real de ir além de uma única execução, mas roda sobre um único `random_state=42` (sem variar seeds como fizeram outros colegas) e sobre um pipeline com o vazamento descrito na seção 3 — a aparência de rigor estatístico não se sustenta.
9.2. Seção de limitações presente: **2** *(v1: 1)* — a seção "1.4 Limitações Metodológicas" existe e reconhece o corpus sintético, o que é um avanço real; mas fica seriamente comprometida pela omissão seletiva de 2 dos 6 resultados do teste de estresse (seção 4 acima) — ter uma seção de limitações e, na prática, esconder resultados desfavoráveis de um teste desenhado para "validar honestidade científica" é uma contradição que pesa mais do que a simples ausência da seção pesaria.

## 6. Nota final

**7,2 / 10** *(v1: 3,0/10)* — Você deu um salto real e bem argumentado nas duas dimensões que mais pesam na rubrica (negócio e ROI) e implementou corretamente uma comparação com ML tradicional que faltava por completo na v1. Isso justifica uma subida grande na nota. Mas dois problemas seguram a nota de ir mais longe: primeiro, o vazamento por quase-duplicidade da v1 continua sem correção — e ganhou um segundo ponto de vazamento na validação cruzada, o que significa que os números de "100% de acurácia, desvio-padrão zero" não são confiáveis (a versão corrigida cai para ~75%/71%, com desvio real). Segundo, e mais importante: o teste de estresse que você mesmo desenhou para checar honestidade científica teve 2 de seus 6 resultados (ambos desfavoráveis) omitidos do README — isso pesa diretamente no critério que já era o ponto mais fraco da sua v1.

**Nível de maturidade: PoC/protótipo.** O ROI e o MLOps agora têm conteúdo real o suficiente para começar uma conversa de negócio, mas a validade técnica do modelo por trás desses números de recall/acurácia ainda não está estabelecida — o vazamento de dados precisa ser corrigido (split por frase-base, como o colega Sergio fez, e um `Pipeline` para o `TfidfVectorizer` dentro do `cross_val_score`) antes de qualquer piloto controlado.

## 7. Task list para evoluir o trabalho (itens ainda abertos)

- [ ] **7.2/9.1 (correção de fundo, prioridade máxima):** corrija o vazamento por quase-duplicidade separando as frases-base em treino/teste **antes** de gerar variações (como no `split_frases_base` do colega Sergio), e troque o `vectorizer.fit_transform(df_sentimento["texto"])` antes do `cross_val_score` por um `Pipeline([("tfidf", TfidfVectorizer(...)), ("clf", mlp)])` passado inteiro ao `cross_val_score`, para que o vocabulário seja reajustado a cada fold, só no treino daquele fold.
- [ ] **9.2 (honestidade, prioridade máxima):** reporte os 6 resultados do teste de estresse no README, não só 4 — inclusive os 2 casos "neutro" que erraram. Uma seção de limitações que omite os resultados mais desfavoráveis do próprio teste de honestidade perde a força que deveria ter.
- [ ] **2.4:** ajuste a nomenclatura do "Payback Period" ou recalcule com a fórmula tradicional (capex ÷ retorno líquido mensal, que dá ≈1,6 meses) — ou, se preferir manter a fórmula atual, deixe explícito que é uma métrica não-padrão (ex: "razão custo total/receita anual em meses").
- [ ] **6.2:** quantifique o gatilho de retreino (ex: "retreinar se X% dos casos forem sinalizados como mal classificados pelo NOC em um mês") em vez de deixar só qualitativo.
- [ ] **5.3:** embeddings/atenção seguem como próximo passo, já bem justificado no roadmap do README.

## 8. Tópicos para o aluno revisar

- **Vazamento de dados em validação cruzada** — motivado pelo achado da seção 3: `cross_val_score` só é livre de vazamento se todo o pré-processamento (incluindo `fit` do vetorizador) acontecer dentro de cada fold — a forma correta é usar `Pipeline` em vez de pré-computar `X_all_vec` uma única vez para todos os folds.
- **Honestidade na divulgação de resultados de teste** — motivado pela seção 4: um teste desenhado para expor limitações do modelo só cumpre esse papel se todos os resultados (inclusive os desfavoráveis) forem reportados; reportar um subconjunto favorável de um teste de robustez é uma forma sutil, mas real, de comprometer a honestidade dos resultados.
- **ROI e conceito de payback** — motivado pela seção 4: vale revisar a definição padrão de payback period (tempo para o fluxo de caixa líquido recuperar o investimento inicial) antes de adotar uma fórmula não-convencional.
