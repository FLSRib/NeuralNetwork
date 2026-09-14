# Análise v3 — Fabio Lima da Silva Ribeiro (`FLSRib`)

**Projeto:** Chatbot de Atendimento a Trouble Tickets com Análise de Sentimento via Redes Neurais
**Repositório:** [FLSRib/NeuralNetwork](https://github.com/FLSRib/NeuralNetwork) — pastas `chatbot-atendimento-CRM_rev_V3/` e `chatbot-atendimento-CRM_rev_V4/`
**Nota v1:** 3,0/10 → v2: 7,2/10 → **Nota v3: 8,0/10**

---

## 1. Abertura

Fabio, os dois achados críticos da v2 foram corrigidos de verdade — verifiquei reexecutando tudo do zero, mais de uma vez, em ambientes diferentes. O vazamento por quase-duplicidade agora tem correção estrutural (split por frase-base com `assert` de zero sobreposição) e a validação cruzada não vaza mais o vocabulário do TF-IDF. O teste de estresse, que na v2 omitia seletivamente os 2 casos que o modelo errava, agora reporta todos os 7 casos no README, batendo exatamente com o notebook. A rev_V4 ainda trouxe uma contribuição nova e honesta: uma prova empírica real comparando a rede neural contra um classificador por regras, usando a métrica certa (recall da classe negativa, não acurácia).

O que impede a nota de subir ainda mais é um problema novo, introduzido nesta mesma correção: o notebook agora depende de um arquivo que nunca foi commitado — ninguém consegue reexecutá-lo do zero, nem eu, nem você mesmo em uma máquina limpa.

## 2. Estrutura desta entrega

Você criou duas pastas novas e paralelas — `chatbot-atendimento-CRM_rev_V3/` (11/09) e `chatbot-atendimento-CRM_rev_V4/` (14/09) — mantendo a v2 intocada em `chatbot-atendimento-CRM_revisado/`. Confirmei que `rev_V4` é evolução direta de `rev_V3` (o código de produção `chatbot_tickets.py`, o CSV e o `requirements.txt` são byte-a-byte idênticos entre as duas pastas; só README e notebook mudam) — avaliei `rev_V4` como o estado atual, citando V3 onde relevante para a evolução.

## 3. Os dois achados críticos da v2 — verificados como corrigidos

### 3.1 Vazamento por quase-duplicidade — corrigido estruturalmente

A célula 6 agora separa as 195 frases-base (65 por classe) em treino/teste **antes** de gerar as variações com prefixo/sufixo, com um `assert len(sobreposicao) == 0` explícito no próprio notebook. Reexecutei e confirmei: `Sobreposição de frases-base entre Treino e Teste: 0`.

### 3.2 Vazamento na validação cruzada (TF-IDF fit fora do fold) — corrigido

A célula 8 agora usa `Pipeline([("tfidf", TfidfVectorizer(...)), ("clf", modelo)])` inteiro dentro de `cross_val_score(..., groups=frase_base_id, cv=GroupKFold(n_splits=5))` — o vetorizador só vê o vocabulário do treino de cada fold.

**Números reais, reexecutados de forma independente 3 vezes** (ambiente atual, ambiente com as versões exatas do `requirements.txt`, e com bibliotecas pinadas em execução single-thread): a acurácia fica consistentemente na faixa de **~69% a 82%** para MLP e Regressão Logística — muito longe dos ~98,9%-100% da v2 com vazamento. A conclusão qualitativa (vazamento eliminado, comparação MLP-vs-LR ainda válida) é robusta nas 3 reexecuções. Ver ressalva na seção 4.2 sobre a precisão dos números pontuais específicos.

### 3.3 Omissão seletiva no teste de estresse — corrigida

A tabela de teste de estresse do README de `rev_V4` (seção 7) agora reporta **todos os 7 casos** do notebook, incluindo os 4 que erram — batendo célula a célula com o output salvo (confiança, rótulo predito e motivo idênticos). Diferente da v2, que escondia justamente os casos desfavoráveis.

## 4. O que é novo nesta rodada

### 4.1 Prova empírica real para o critério "Necessidade real de IA" (novidade da rev_V4)

As células 19 e 21 implementam um classificador determinístico por dicionário de palavras (vocabulário de telecom plausível, não um espantalho artificialmente fraco) e o comparam ao MLP no mesmo split sem vazamento. Reexecutei e reproduzi exatamente os números do README: acurácia da regra 66,7%, recall-negativo 41,2% — e o MLP supera as regras em recall da classe negativa em toda reexecução, por margem de 17-28 p.p. É uma prova real, não retórica, e a métrica escolhida (recall da classe negativa, o que importa para não perder um cliente insatisfeito) é a correta para o argumento de negócio.

### 4.2 Achado novo — dependência não commitada quebra a reprodutibilidade do zero

A célula 6 de ambos os notebooks (V3 e V4) faz `from generate_rev_v3_artifacts import (...)`. Esse arquivo **nunca foi commitado** em nenhum commit do repositório. Confirmei rodando em clone limpo: `ModuleNotFoundError: No module named 'generate_rev_v3_artifacts'`. A v2 era 100% autocontida — este é um passo atrás em reprodutibilidade, introduzido justamente na correção que deveria aumentar o rigor. Só consegui reexecutar reconstruindo as mesmas listas/funções a partir do `chatbot_tickets.py` (que está commitado).

Relacionado: mesmo com esse "atalho" e as versões exatas do `requirements.txt`, os números de MLP/LR não batem de forma exata entre reexecuções (faixa de ~69% a 82%, ver seção 3.2) — o `requirements.txt` não fixa `scipy` (dependência interna sensível a BLAS/plataforma). A direção da conclusão (sem vazamento) é robusta; a precisão dos números pontuais citados no README não é.

### 4.3 Achados menores

- `registro_sentimentos_tickets.csv` (commitado) tem duas levas de logs quase idênticos em timestamps próximos — artefato de execução esquecido, não erro de lógica.
- O README de `rev_V4` não menciona `rev_V3` em nenhum lugar (por decisão explícita, conforme a mensagem do commit) — nada foi apagado do histórico do git, mas quem ler só o README de V4 não saberá que existiu uma etapa intermediária que introduziu o guardrail pt-BR e a correção de vazamento.
- O guardrail pt-BR (introduzido em V3) sobrevive intacto em V4 e funciona corretamente em toda reexecução (interceptação determinística antes do modelo estatístico).
- O roadmap de evolução (TF-IDF → Embeddings → Transformers) é só texto/plano, corretamente rotulado como fases futuras — sem alegação enganosa de que já está implementado.

## 5. Nota por critério (atualizada)

### Critérios de negócio (peso maior)

**1. Aderência ao negócio — 9,2/10** *(mantido, v2: 9,2/10)*

**2. Viabilidade econômica (ROI) — 8,1/10** *(mantido, v2: 8,1/10)*

### Critérios técnicos (peso menor)

**3. Necessidade real de IA — 9,5/10** *(v2: 7,5/10)*
3.1. Discute e testa alternativa de regra determinística: **5** *(v2: 4)* — agora testada de fato, não só discutida em texto (seção 4.1).

**4. ML tradicional vs. Redes Neurais — 10,0/10** *(mantido)*

**5. Aderência ao conteúdo do curso — 5,8/10** *(mantido)*

**6. Aderência ao template de projeto — 8,75/10** *(mantido)*

**7. Correção técnica — 7,5/10** *(v2: 8,75/10)*
7.1. Código executa sem erro: **3** *(v2: 5)* — o notebook depende de um módulo nunca commitado; não executa do zero em clone limpo (seção 4.2).
7.2. Split antes de pré-processamento: **5** *(v2: 3)* — corrigido, `Pipeline` dentro de `GroupKFold`.

**8. Qualidade do código — 8,0/10** *(v2: 9,2/10)* — dependência ausente (seção 4.2) e CSV com logs duplicados (seção 4.3).

**9. Honestidade dos resultados — 8,5/10** *(v2: 3,75/10)*
9.1. Múltiplas execuções/seeds: **4** *(v2: 3)* — validação cruzada agora livre do vazamento; conclusão qualitativa robusta em 3 reexecuções independentes.
9.2. Seção de limitações / teste de estresse completo: **5** *(v2: 2)* — os 7 casos agora reportados integralmente, batendo com o notebook. Este era o achado mais grave da v2 e foi resolvido sem ressalvas.

## 6. Nota final

**8,0 / 10** *(v2: 7,2/10)* — Os dois achados que travaram a v2 foram corrigidos de verdade, e verifiquei isso de forma independente, não apenas lendo o README: o vazamento por quase-duplicidade tem correção estrutural com `assert` de zero sobreposição, a validação cruzada não vaza mais o TF-IDF, e o teste de estresse — o achado mais grave, por atingir diretamente a honestidade dos resultados — agora reporta todos os 7 casos, incluindo os desfavoráveis. A rev_V4 ainda soma uma contribuição real ao critério de necessidade de IA, com a métrica de negócio certa.

A nota não sobe mais porque a correção introduziu um problema novo: o notebook depende de um arquivo nunca commitado, quebrando a reprodutibilidade do zero — e, mesmo contornando isso, os números pontuais de acurácia variam (~69% a 82%) entre reexecuções idênticas em código, por falta de uma dependência (`scipy`) sem versão fixada. A direção dos resultados é sólida; a precisão dos números específicos citados no README, não.

**Nível de maturidade: piloto controlado (no núcleo técnico).** O vazamento de dados que impedia confiar nos números foi eliminado e a honestidade do teste de estresse foi restaurada — os dois requisitos que faltavam para avançar além de "PoC com problema de confiança". O que falta agora é reprodutibilidade de ambiente, não mais honestidade ou vazamento.

## 7. O que preciso que você corrija (não é necessário v4 formal por conta disso, mas recomendo)

1. **Commite o arquivo `generate_rev_v3_artifacts.py`** (ou remova a dependência, inline no notebook) — sem isso, ninguém reproduz o projeto do zero.
2. **Fixe `scipy` no `requirements.txt`** (além das libs já pinadas) para reduzir a variação de ~13 p.p. observada entre reexecuções idênticas em código.
3. Opcional: mencione `rev_V3` no README de `rev_V4`, mesmo que brevemente, para preservar a rastreabilidade de que o guardrail e a correção de vazamento vieram de uma etapa intermediária.

Parabéns pela correção dos dois pontos mais importantes — em especial o teste de estresse, que era o achado mais sério de toda a análise até aqui.
