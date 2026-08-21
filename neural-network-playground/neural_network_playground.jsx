import React, { useState, useMemo } from 'react';

const ACTIVATIONS = {
  relu: { label: 'ReLU', fn: (z) => Math.max(0, z), range: [0, 2] },
  sigmoid: { label: 'Sigmoide', fn: (z) => 1 / (1 + Math.exp(-z)), range: [0, 1] },
  tanh: { label: 'Tanh', fn: (z) => Math.tanh(z), range: [-1, 1] },
};

const SLATE = [51, 65, 85];
const CYAN = [34, 211, 238];
const ROSE = [251, 113, 133];

function lerp(a, b, t) { return a + (b - a) * t; }
function lerpColor(c1, c2, t) {
  const r = Math.round(lerp(c1[0], c2[0], t));
  const g = Math.round(lerp(c1[1], c2[1], t));
  const b = Math.round(lerp(c1[2], c2[2], t));
  return `rgb(${r},${g},${b})`;
}

function activationColor(value, range) {
  const [lo, hi] = range;
  if (lo < 0) {
    if (value >= 0) return lerpColor(SLATE, CYAN, Math.min(1, value / hi));
    return lerpColor(SLATE, ROSE, Math.min(1, value / lo));
  }
  return lerpColor(SLATE, CYAN, Math.min(1, Math.max(0, value / hi)));
}

function randWeight() { return +(Math.random() * 2 - 1).toFixed(2); }

function buildWeights(sizes) {
  const weights = [];
  const biases = [];
  for (let l = 1; l < sizes.length; l++) {
    const prev = sizes[l - 1], curr = sizes[l];
    weights.push(Array.from({ length: curr }, () => Array.from({ length: prev }, randWeight)));
    biases.push(Array.from({ length: curr }, randWeight));
  }
  return { weights, biases };
}

function forwardPass(input, weights, biases, actFn) {
  const activations = [input];
  const zs = [];
  let prev = input;
  for (let l = 0; l < weights.length; l++) {
    const z = weights[l].map((row, i) => row.reduce((s, w, j) => s + w * prev[j], 0) + biases[l][i]);
    const a = z.map(actFn);
    zs.push(z);
    activations.push(a);
    prev = a;
  }
  return { activations, zs };
}

const WIDTH = 760, HEIGHT = 440, MARGIN_X = 70, MARGIN_Y = 40;

export default function NeuralNetworkPlayground() {
  const [inputSize, setInputSize] = useState(3);
  const [hiddenLayers, setHiddenLayers] = useState([4, 4]);
  const outputSize = 2;
  const [activationKey, setActivationKey] = useState('tanh');
  const [inputs, setInputs] = useState([0.5, -0.3, 0.8]);
  const [randomizeVersion, setRandomizeVersion] = useState(0);
  const [selected, setSelected] = useState(null);
  const [pulseTrigger, setPulseTrigger] = useState(0);

  const layerSizes = [inputSize, ...hiddenLayers, outputSize];
  const architectureKey = layerSizes.join(',');

  // Pesos recalculados de forma síncrona, sempre no mesmo render em que a
  // arquitetura muda — evita um frame intermediário com dimensões
  // desencontradas entre entradas, pesos e o desenho da rede.
  const weightsState = useMemo(() => buildWeights(layerSizes), [architectureKey, randomizeVersion]);

  // Muda o número de entradas e redimensiona o array de valores no mesmo
  // gesto, para nunca existir um render com inputSize e inputs.length
  // diferentes um do outro.
  const changeInputSize = (delta) => {
    setInputSize((s) => {
      const next = Math.max(2, Math.min(4, s + delta));
      setInputs((prev) => Array.from({ length: next }, (_, i) => (prev[i] !== undefined ? prev[i] : +(Math.random() * 2 - 1).toFixed(2))));
      return next;
    });
  };

  // Se a arquitetura mudou e a seleção antiga aponta para uma camada/neurônio
  // que não existe mais, tratamos como se nada estivesse selecionado.
  const validSelected = selected && selected.layer < layerSizes.length && selected.idx < layerSizes[selected.layer] ? selected : null;

  const { activations, zs } = useMemo(
    () => forwardPass(inputs, weightsState.weights, weightsState.biases, ACTIVATIONS[activationKey].fn),
    [inputs, weightsState, activationKey]
  );

  const maxN = Math.max(...layerSizes);
  const spacingY = Math.min(60, (HEIGHT - 2 * MARGIN_Y) / Math.max(1, maxN - 1));
  const nodeX = (li) => MARGIN_X + (li * (WIDTH - 2 * MARGIN_X)) / (layerSizes.length - 1);
  const nodeY = (li, ni) => {
    const n = layerSizes[li];
    const totalHeight = (n - 1) * spacingY;
    return HEIGHT / 2 - totalHeight / 2 + ni * spacingY;
  };

  const addLayer = () => setHiddenLayers((h) => (h.length < 4 ? [...h, 4] : h));
  const removeLayer = () => setHiddenLayers((h) => (h.length > 1 ? h.slice(0, -1) : h));
  const changeNeurons = (idx, delta) =>
    setHiddenLayers((h) => h.map((n, i) => (i === idx ? Math.min(8, Math.max(1, n + delta)) : n)));

  const btnBase = 'w-6 h-6 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm focus:outline-none focus:ring-2 focus:ring-cyan-400/50';
  const range = ACTIVATIONS[activationKey].range;

  let inspector = null;
  if (validSelected) {
    if (validSelected.layer === 0) {
      inspector = (
        <div>
          <p className="text-sm font-mono text-cyan-300 mb-2">entrada · x{validSelected.idx + 1}</p>
          <p className="text-sm text-slate-300">
            valor = <span className="font-mono text-slate-100">{inputs[validSelected.idx].toFixed(3)}</span>
          </p>
          <p className="text-xs text-slate-500 mt-2">Valores de entrada não passam por cálculo — são o ponto de partida do sinal.</p>
        </div>
      );
    } else {
      const l = validSelected.layer - 1, i = validSelected.idx;
      const prevActs = activations[validSelected.layer - 1];
      const w = weightsState.weights[l][i];
      const b = weightsState.biases[l][i];
      const z = zs[l][i];
      const a = activations[validSelected.layer][i];
      inspector = (
        <div>
          <p className="text-sm font-mono text-cyan-300 mb-3">
            camada {validSelected.layer} · neurônio {i + 1}
          </p>
          <div className="grid grid-cols-2 gap-x-4 gap-y-1 mb-3 font-mono text-xs text-slate-400">
            {w.map((wj, j) => (
              <div key={j}>
                w{j + 1}·x{j + 1} = {wj.toFixed(2)} × {prevActs[j].toFixed(2)} = <span className="text-slate-200">{(wj * prevActs[j]).toFixed(2)}</span>
              </div>
            ))}
          </div>
          <p className="text-sm text-slate-300 font-mono">
            z = Σ(w·x) + b = <span className="text-slate-100">{z.toFixed(3)}</span> <span className="text-slate-600">(b = {b.toFixed(2)})</span>
          </p>
          <p className="text-sm text-slate-300 font-mono mt-1">
            a = {ACTIVATIONS[activationKey].label}(z) = <span className="text-amber-300">{a.toFixed(3)}</span>
          </p>
        </div>
      );
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8">
        <p className="text-xs font-mono uppercase tracking-widest text-cyan-400 mb-2">Playground · Redes Neurais</p>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-50">Como o sinal se propaga por camadas ocultas</h1>
        <p className="text-sm text-slate-400 mt-2 max-w-2xl">
          Ajuste a arquitetura, mude as entradas e clique em qualquer neurônio para ver a conta por trás da sua ativação.
        </p>
        <div className="inline-flex flex-wrap items-center gap-2 mt-4 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900/60 font-mono text-xs text-slate-400">
          <span className="text-cyan-400">z</span> = Σ (peso × entrada) + viés
          <span className="text-slate-600">→</span>
          <span className="text-amber-300">ativação(z)</span>
        </div>

        <div className="flex flex-col lg:flex-row gap-6 mt-6">
          {/* Sidebar */}
          <aside className="w-full lg:w-72 shrink-0 space-y-5">
            <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Arquitetura</h3>

              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-slate-300">Entradas</span>
                <div className="flex items-center gap-2">
                  <button className={btnBase} onClick={() => changeInputSize(-1)}>−</button>
                  <span className="w-5 text-center font-mono text-cyan-300 text-sm">{inputSize}</span>
                  <button className={btnBase} onClick={() => changeInputSize(1)}>+</button>
                </div>
              </div>

              {hiddenLayers.map((n, li) => (
                <div key={li} className="flex items-center justify-between mb-2 pl-3 border-l-2 border-slate-800">
                  <span className="text-sm text-slate-300">Oculta {li + 1}</span>
                  <div className="flex items-center gap-2">
                    <button className={btnBase} onClick={() => changeNeurons(li, -1)}>−</button>
                    <span className="w-5 text-center font-mono text-cyan-300 text-sm">{n}</span>
                    <button className={btnBase} onClick={() => changeNeurons(li, 1)}>+</button>
                  </div>
                </div>
              ))}

              <div className="flex gap-2 mt-3">
                <button
                  onClick={addLayer}
                  disabled={hiddenLayers.length >= 4}
                  className="flex-1 text-xs py-1.5 rounded border border-slate-700 text-slate-300 hover:bg-slate-800 disabled:opacity-30 focus:outline-none focus:ring-2 focus:ring-cyan-400/50"
                >
                  + camada
                </button>
                <button
                  onClick={removeLayer}
                  disabled={hiddenLayers.length <= 1}
                  className="flex-1 text-xs py-1.5 rounded border border-slate-700 text-slate-300 hover:bg-slate-800 disabled:opacity-30 focus:outline-none focus:ring-2 focus:ring-cyan-400/50"
                >
                  − camada
                </button>
              </div>

              <div className="flex items-center justify-between mt-3 pt-3 border-t border-slate-800">
                <span className="text-sm text-slate-300">Saídas</span>
                <span className="font-mono text-amber-300 text-sm">{outputSize}</span>
              </div>
            </div>

            <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Valores de entrada</h3>
              {inputs.map((v, i) => (
                <div key={i} className="mb-3 last:mb-0">
                  <div className="flex justify-between text-xs text-slate-400 mb-1">
                    <span>x{i + 1}</span>
                    <span className="font-mono text-cyan-300">{v.toFixed(2)}</span>
                  </div>
                  <input
                    type="range"
                    min="-1"
                    max="1"
                    step="0.05"
                    value={v}
                    onChange={(e) => setInputs((arr) => arr.map((val, idx) => (idx === i ? parseFloat(e.target.value) : val)))}
                    className="w-full accent-cyan-400"
                  />
                </div>
              ))}
            </div>

            <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Função de ativação</h3>
              <div className="grid grid-cols-3 gap-2">
                {Object.entries(ACTIVATIONS).map(([key, { label }]) => (
                  <button
                    key={key}
                    onClick={() => setActivationKey(key)}
                    className={`text-xs py-2 rounded border focus:outline-none focus:ring-2 focus:ring-cyan-400/50 ${
                      activationKey === key ? 'bg-cyan-400/10 border-cyan-400 text-cyan-300' : 'border-slate-700 text-slate-400 hover:bg-slate-800'
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <button
                onClick={() => setRandomizeVersion((v) => v + 1)}
                className="text-sm py-2 rounded border border-slate-700 text-slate-300 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400/50"
              >
                🎲 Aleatorizar pesos
              </button>
              <button
                onClick={() => setPulseTrigger((t) => t + 1)}
                className="text-sm py-2 rounded bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold focus:outline-none focus:ring-2 focus:ring-cyan-300"
              >
                ▶ Propagar sinal
              </button>
            </div>
          </aside>

          {/* Main */}
          <div className="flex-1 min-w-0">
            <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-2 sm:p-4 overflow-x-auto">
              <svg viewBox={`0 0 ${WIDTH} ${HEIGHT + 30}`} className="w-full" style={{ minWidth: 600 }}>
                <style>{`
                  @keyframes pulseRing {
                    0% { opacity: 0.9; transform: scale(1); }
                    100% { opacity: 0; transform: scale(1.9); }
                  }
                `}</style>

                {weightsState.weights.map((wMatrix, l) =>
                  wMatrix.map((row, i) =>
                    row.map((w, j) => {
                      const x1 = nodeX(l), y1 = nodeY(l, j);
                      const x2 = nodeX(l + 1), y2 = nodeY(l + 1, i);
                      const positive = w >= 0;
                      const baseOpacity = Math.min(1, Math.abs(w)) * 0.65 + 0.06;
                      const isIncoming = validSelected && validSelected.layer === l + 1 && validSelected.idx === i;
                      const opacity = validSelected ? (isIncoming ? baseOpacity : baseOpacity * 0.12) : baseOpacity;
                      return (
                        <line
                          key={`e-${l}-${i}-${j}`}
                          x1={x1} y1={y1} x2={x2} y2={y2}
                          stroke={positive ? '#22d3ee' : '#fb7185'}
                          strokeWidth={isIncoming ? 2 : 1}
                          opacity={opacity}
                        />
                      );
                    })
                  )
                )}

                {layerSizes.map((n, li) =>
                  Array.from({ length: n }).map((_, ni) => {
                    const x = nodeX(li), y = nodeY(li, ni);
                    const value = activations[li][ni];
                    const nodeRange = li === 0 ? [-1, 1] : range;
                    const fill = activationColor(value, nodeRange);
                    return (
                      <circle
                        key={`ring-${pulseTrigger}-${li}-${ni}`}
                        cx={x} cy={y} r={17} fill="none" stroke={fill} strokeWidth={3}
                        style={{
                          animation: 'pulseRing 0.7s ease-out both',
                          animationDelay: `${li * 0.22}s`,
                          transformBox: 'fill-box',
                          transformOrigin: 'center',
                        }}
                      />
                    );
                  })
                )}

                {layerSizes.map((n, li) => (
                  <g key={`layer-${li}`}>
                    {Array.from({ length: n }).map((_, ni) => {
                      const x = nodeX(li), y = nodeY(li, ni);
                      const value = activations[li][ni];
                      const nodeRange = li === 0 ? [-1, 1] : range;
                      const fill = activationColor(value, nodeRange);
                      const isSelected = validSelected && validSelected.layer === li && validSelected.idx === ni;
                      return (
                        <g key={`n-${li}-${ni}`} className="cursor-pointer" onClick={() => setSelected({ layer: li, idx: ni })}>
                          <circle
                            cx={x} cy={y} r={17} fill={fill}
                            stroke={isSelected ? '#fbbf24' : '#475569'}
                            strokeWidth={isSelected ? 3 : 1.5}
                          />
                          {n <= 6 && (
                            <text x={x} y={y + 4} textAnchor="middle" fontSize="9" fill="#0f172a" fontFamily="ui-monospace, monospace" pointerEvents="none">
                              {value.toFixed(2)}
                            </text>
                          )}
                          <title>{`Camada ${li} · Neurônio ${ni + 1}: ${value.toFixed(3)}`}</title>
                        </g>
                      );
                    })}
                  </g>
                ))}

                {layerSizes.map((n, li) => (
                  <text
                    key={`lbl-${li}`}
                    x={nodeX(li)} y={HEIGHT + 20} textAnchor="middle" fontSize="11"
                    fill="#7c88aa" fontFamily="ui-monospace, monospace"
                  >
                    {li === 0 ? 'ENTRADA' : li === layerSizes.length - 1 ? 'SAÍDA' : `OCULTA ${li}`}
                  </text>
                ))}
              </svg>
            </div>

            <div className="flex flex-wrap gap-4 mt-3 text-xs text-slate-400">
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full inline-block" style={{ background: '#22d3ee' }} /> peso ou ativação positiva
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full inline-block" style={{ background: '#fb7185' }} /> valor negativo
              </span>
              <span className="flex items-center gap-1.5">
                <span className="w-3 h-3 rounded-full inline-block" style={{ background: '#334155' }} /> neurônio pouco ativo
              </span>
            </div>

            <div className="grid sm:grid-cols-2 gap-4 mt-4">
              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Saída da rede</h3>
                <div className="space-y-2">
                  {activations[activations.length - 1].map((v, i) => {
                    const pct = Math.max(0, Math.min(100, ((v - range[0]) / (range[1] - range[0])) * 100));
                    return (
                      <div key={i}>
                        <div className="flex justify-between text-xs text-slate-400 mb-1">
                          <span>Saída {i + 1}</span>
                          <span className="font-mono text-amber-300">{v.toFixed(3)}</span>
                        </div>
                        <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
                          <div className="h-full bg-amber-400 rounded-full transition-all duration-300" style={{ width: `${pct}%` }} />
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 min-h-[110px]">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Inspetor de neurônio</h3>
                {validSelected ? inspector : (
                  <p className="text-sm text-slate-500">Clique em um neurônio na rede para ver o cálculo por trás dele.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
