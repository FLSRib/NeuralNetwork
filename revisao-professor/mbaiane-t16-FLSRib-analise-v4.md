# Análise v4 — Fabio Lima da Silva Ribeiro (`FLSRib`)

**Projeto:** Chatbot de atendimento CRM — classificação de sentimento em tickets
**Repositório:** [FLSRib/NeuralNetwork](https://github.com/FLSRib/NeuralNetwork)
**Commits analisados:** `80ce10d2` (14/09) e `bde00aed` (15/09), sobre a pasta `chatbot-atendimento-CRM_rev_V4/`
**Nota v1:** 3,0/10 → v2: 7,2/10 → v3: 8,0/10 → **Nota v4: 8,3/10**

---

## 1. Abertura

Fabio, os dois pedidos que fechavam a v3 foram atendidos com seriedade e rapidez — menos de 24h e 48h depois da nota, respectivamente. O achado mais grave dela ("ninguém consegue reexecutar seu notebook do zero") está resolvido. Reexecutei tudo 3 vezes de forma independente (2 no mesmo ambiente, 1 em venv criado do zero) para confirmar.

## 2. Os pedidos da v3 — verificação item a item

| # | Pedido da v3 | Situação na v4 |
|---|---|---|
| 1 | Commitar `generate_rev_v3_artifacts.py` (dependência ausente que impedia execução do zero) | **Corrigido.** Commitado em `rev_V3` e `rev_V4`, com `try/except` adicional no notebook como fallback. |
| 2 | Pinar `scipy` para eliminar variação de acurácia entre execuções | **Parcialmente.** `scipy==1.11.4` pinado — e isso resolveu a variação *dentro* da mesma máquina (minhas 3 reexecuções bateram bit-idênticas entre si). Mas a variação *entre máquinas diferentes* continua: os números do seu README (teste MLP 69,4%, CV 78,8%/78,4%) não batem com o que reproduzi aqui (teste MLP 76,1%/74,9%, CV 82,0%/81,0%) — mesma versão de scipy, hardware diferente (Windows vs. macOS), afetando a otimização não-convexa do MLP via BLAS. |
| 3 (opcional) | Mencionar `rev_V3` no README de `rev_V4` | **Corrigido.** |

**Ponto importante sobre o item 2:** não é desonestidade. Extraí os pesos que você embutiu no `playground.html` (gerados na sua própria máquina) e repliquei a inferência em Python puro — bateu quase exatamente com a tabela do seu README (mesmas 4 frases erradas no teste de estresse, confiança muito próxima). Isso confirma que os números do README são reais, genuínos, não fabricados. O que falta é reconhecer no próprio README que os resultados não são reprodutíveis bit-a-bit fora da sua máquina, mesmo com dependências pinadas — isso é uma limitação legítima de reprodutibilidade (comum em MLPs, não é erro seu), mas precisa estar escrita, não escondida.

## 3. Vazamentos da v3 — nenhuma regressão

Os dois vazamentos mais graves do histórico do projeto (quase-duplicidade por frase-base no split; `TfidfVectorizer.fit` fora da validação cruzada) foram corrigidos na v3 via `Pipeline`+`GroupKFold`. Confirmei que o código das células 6 e 8 é **byte-a-byte idêntico** ao já avaliado na v3 — nenhuma regressão, ao contrário do que já vimos acontecer em outros projetos da turma quando uma correção anterior é silenciosamente desfeita numa rodada seguinte.

## 4. Achado novo — upgrade real do playground, mas fora da trilha de reprodutibilidade

Você trocou o `playground.html` de um classificador por palavras-chave (a mesma técnica que seu próprio README argumenta ser inferior) para uma reimplementação real em JavaScript de TF-IDF + forward-pass de MLP, com os pesos do modelo embutidos. Verifiquei as dimensões (500×32, 32×3) e batem exatamente com `TfidfVectorizer(max_features=500)` + `MLPClassifier(hidden_layer_sizes=(32,))`. É uma melhoria genuína e transparente — você nunca alegou antes que o playground refletia o modelo real, então não há retrocesso de honestidade aqui.

O ponto a ajustar: o script que gera esses pesos (`generate_rev_v3_artifacts.py`) roda no nível de módulo (sem `if __name__ == "__main__":`), então cada `import` duplica silenciosamente todo o treino/validação. E ele cria pastas reais em paths absolutos do seu Windows pessoal (`C:\Users\fribeiro\...`) — confirmei que isso de fato cria diretórios espúrios ao rodar localmente. Nenhum script commitado gera o JSON de pesos do playground a partir do pipeline principal — é um artefato à parte.

## 5. Nota final

**8,3 / 10** *(v3: 8,0/10)* — Os dois pedidos obrigatórios foram atendidos com seriedade e no prazo, nenhum dos vazamentos históricos regrediu, e a honestidade do teste de estresse (o achado mais grave do histórico, corrigido desde a v2) continua de pé. A nota sobe modestamente porque o item de reprodutibilidade cross-máquina não foi de fato fechado (só documentado como "pin de dependência", sem reconhecer a limitação real), e porque o `generate_rev_v3_artifacts.py` introduz um efeito colateral de execução (import não guardado) e artefatos de máquina pessoal commitados sem limpeza.

## 6. O que ainda vale corrigir (não bloqueante)

1. Adicione uma frase no README reconhecendo que os resultados exatos (acurácia, desvio-padrão) podem variar entre máquinas diferentes mesmo com dependências pinadas — é uma limitação real de MLP via Adam/BLAS, não um erro seu, mas precisa estar escrita.
2. Envolva a execução de `generate_rev_v3_artifacts.py` em `if __name__ == "__main__":` para que um `import` não duplique o treino inteiro.
3. Remova os paths absolutos do Windows pessoal (`C:\Users\fribeiro\...`) do script commitado, ou parametrize via variável de ambiente/argumento.
