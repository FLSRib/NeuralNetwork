# Neural Network Playgrounds

Dois playgrounds interativos em React para explorar, na prática, como uma
rede neural do tipo MLP (perceptron multicamadas) funciona — da propagação de
sinal ao treinamento de verdade.

1. **`neural_network_playground.jsx` / `index.html`** (raiz) — arquitetura
   livre, forward pass e inspeção de neurônio por neurônio.
2. **`word-prediction/word_prediction_playground.jsx` / `index.html`** —
   uma rede pequena que **aprende ao vivo, no navegador**, a prever a
   próxima palavra de uma frase.

Cada playground tem seu `index.html` autocontido (React + Babel + Tailwind
via CDN) — basta abrir no navegador, sem instalar nada.

---

## 1. Camadas ocultas (forward pass)

## O que dá para fazer

- **Editar a arquitetura**: número de entradas (2–4), quantidade de camadas
  ocultas (1–4) e neurônios por camada (1–8).
- **Mudar os valores de entrada** via sliders e ver o efeito imediato na rede.
- **Trocar a função de ativação** entre ReLU, Sigmoide e Tanh.
- **Clicar em qualquer neurônio** para abrir o inspetor e ver o cálculo exato
  por trás dele: `z = Σ(peso · entrada) + viés` seguido da ativação.
- **Aleatorizar os pesos** para gerar uma nova rede do zero.
- **Disparar uma animação de propagação** que percorre as camadas da esquerda
  para a direita, camada por camada.

## Como ler a visualização

- Cor do neurônio = intensidade da sua ativação (ciano = positivo, rosa =
  negativo, cinza = pouco ativo).
- Cor da conexão = sinal do peso (ciano = positivo, rosa = negativo);
  opacidade = magnitude do peso.
- Ao selecionar um neurônio, as conexões que alimentam ele ficam em destaque
  e as demais são esmaecidas.

## Stack

- React (hooks: `useState`, `useEffect`, `useMemo`)
- SVG puro para o diagrama da rede (sem bibliotecas de gráfico)
- Tailwind CSS (classes utilitárias padrão) para o layout e os controles

## Arquivo principal

`neural_network_playground.jsx` — componente único, sem dependências externas
além de `react`. Pode ser aberto diretamente como artifact no Claude.ai ou
integrado a qualquer projeto React/Vite/Next que já tenha Tailwind
configurado.

## Rodando localmente (fora do Claude.ai)

```bash
npm create vite@latest meu-playground -- --template react
cd meu-playground
npm install
# copie neural_network_playground.jsx para src/
# configure o Tailwind (https://tailwindcss.com/docs/guides/vite)
# importe e renderize <NeuralNetworkPlayground /> em src/App.jsx
npm run dev
```

Ou simplesmente abra `index.html` direto no navegador — não precisa de nada disso.

---

## 2. Completar frase (previsão de próxima palavra)

Uma rede pequena (contexto de 2 palavras → 16 neurônios ocultos → softmax
sobre o vocabulário) treinada, do zero, com ~45 frases curtas em português.
Não é um modelo de linguagem geral — é proposital: o objetivo é ver o
treinamento (gradiente descendente, perda caindo, pesos mudando) acontecer
de verdade, e não apenas simular um forward pass com pesos aleatórios.

### O que dá para fazer

- **Treinar** a rede em lotes de épocas, ou ligar o treino automático e ver
  a perda cair ao vivo (com um mini-gráfico de tendência).
- **Digitar o início de uma frase** e ver as top-6 próximas palavras
  previstas, com probabilidade — clicar numa palavra a acrescenta à frase e
  gera uma nova previsão.
- **Ver o diagrama da rede**: os pesos reais que ligam as duas palavras de
  contexto à camada oculta, e quais neurônios mais "empurram" a rede para a
  palavra escolhida.
- **Reiniciar os pesos** para comparar uma rede destreinada com uma treinada.
- Consultar o vocabulário completo que a rede conhece (ela ignora qualquer
  palavra fora dele).

### Arquivo principal

`word-prediction/word_prediction_playground.jsx` — mesmo princípio do outro
componente: React puro, sem dependências além de `react`, forward/backward
pass implementados manualmente (sem TensorFlow.js nem outra lib de ML).
