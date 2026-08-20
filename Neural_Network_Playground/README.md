# Neural Network Playground — Camadas Ocultas

Playground interativo em React para explorar, na prática, como uma rede neural
do tipo MLP (perceptron multicamadas) propaga um sinal da entrada até a saída,
passando por uma ou mais camadas ocultas.

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
