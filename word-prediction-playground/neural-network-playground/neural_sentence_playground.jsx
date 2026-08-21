import React, { useState, useEffect, useMemo } from 'react';

/* ---------- corpus: um punhado de frases curtas em português ---------- */

const RAW_SENTENCES = [
  'o gato dorme no sofá da sala.',
  'o café está quente e forte.',
  'a manhã chegou fria e cinza.',
  'o gato pula para a janela.',
  'a chuva cai sobre o telhado.',
  'eu tomo café antes do trabalho.',
  'o sol nasce atrás das montanhas.',
  'o gato mia perto da porta.',
  'a cidade acorda devagar hoje.',
  'o vento sopra forte pela manhã.',
  'eu escrevo código durante a tarde.',
  'o gato brinca com a bola.',
  'a noite chega calma e silenciosa.',
  'eu leio um livro antes de dormir.',
  'o café da manhã está pronto.',
  'o gato observa os pássaros lá fora.',
  'a tarde passa rápido demais hoje.',
  'eu caminho até o trabalho todos os dias.',
  'o gato dorme durante quase todo o dia.',
  'a chuva para antes do meio-dia.',
  'eu bebo água depois do café.',
  'o sol se põe atrás do mar.',
  'o gato corre atrás do rato de brinquedo.',
  'a manhã traz um silêncio agradável.',
  'eu trabalho em frente ao computador.',
  'o vento balança as árvores da rua.',
  'o gato dorme no sofá durante a tarde.',
  'a noite traz estrelas e silêncio.',
  'eu preparo o jantar depois do trabalho.',
  'o café esfria rápido na cozinha.',
  'o gato olha pela janela da sala.',
  'a chuva molha as ruas da cidade.',
  'eu durmo cedo durante a semana.',
  'o sol aquece a sala pela manhã.',
  'o gato mia alto de manhã cedo.',
  'eu assisto um filme antes de dormir.',
  'a tarde fica quente durante o verão.',
  'o gato salta para cima da mesa.',
  'eu escuto música enquanto trabalho.',
  'a noite fica fria durante o inverno.',
];

const START = '<início>';
const END = '<fim>';

function buildVocabAndPairs(sentences) {
  const tokenized = sentences.map((s) =>
    s.toLowerCase().replace(/[.,]/g, '').trim().split(/\s+/)
  );
  const wordSet = new Set([START, END]);
  tokenized.forEach((ws) => ws.forEach((w) => wordSet.add(w)));
  const vocab = Array.from(wordSet);
  const word2idx = {};
  vocab.forEach((w, i) => (word2idx[w] = i));
  const pairs = [];
  tokenized.forEach((ws) => {
    const seq = [START, ...ws, END];
    for (let i = 0; i < seq.length - 1; i++) {
      pairs.push([word2idx[seq[i]], word2idx[seq[i + 1]]]);
    }
  });
  return { vocab, word2idx, pairs };
}

/* ---------- rede: embedding -> camada oculta (tanh) -> softmax ---------- */

function randSmall() { return (Math.random() * 2 - 1) * 0.3; }

function initModel(V, H) {
  return {
    W1: Array.from({ length: V }, () => Array.from({ length: H }, randSmall)),
    b1: Array.from({ length: H }, () => 0),
    W2: Array.from({ length: H }, () => Array.from({ length: V }, randSmall)),
    b2: Array.from({ length: V }, () => 0),
  };
}

function softmax(logits) {
  const max = Math.max(...logits);
  const exps = logits.map((l) => Math.exp(l - max));
  const sum = exps.reduce((a, b) => a + b, 0);
  return exps.map((e) => e / sum);
}

function forward(model, ctxIdx) {
  const H = model.b1.length, V = model.b2.length;
  const h = new Array(H);
  for (let j = 0; j < H; j++) h[j] = Math.tanh(model.W1[ctxIdx][j] + model.b1[j]);
  const logits = new Array(V);
  for (let v = 0; v < V; v++) {
    let s = model.b2[v];
    for (let j = 0; j < H; j++) s += h[j] * model.W2[j][v];
    logits[v] = s;
  }
  return { h, probs: softmax(logits) };
}

function trainModel(model, pairs, epochs, lr) {
  const H = model.b1.length, V = model.b2.length;
  const data = pairs.slice();
  for (let epoch = 0; epoch < epochs; epoch++) {
    for (let i = data.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [data[i], data[j]] = [data[j], data[i]];
    }
    for (const [ctx, target] of data) {
      const { h, probs } = forward(model, ctx);
      const dlogits = probs.slice();
      dlogits[target] -= 1;
      const dh = new Array(H).fill(0);
      for (let jx = 0; jx < H; jx++) {
        let acc = 0;
        for (let v = 0; v < V; v++) acc += model.W2[jx][v] * dlogits[v];
        dh[jx] = acc;
      }
      for (let jx = 0; jx < H; jx++) {
        for (let v = 0; v < V; v++) model.W2[jx][v] -= lr * h[jx] * dlogits[v];
      }
      for (let v = 0; v < V; v++) model.b2[v] -= lr * dlogits[v];
      for (let jx = 0; jx < H; jx++) {
        const dPre = dh[jx] * (1 - h[jx] * h[jx]);
        model.W1[ctx][jx] -= lr * dPre;
        model.b1[jx] -= lr * dPre;
      }
    }
  }
  return model;
}

/* ---------- cor: mesma paleta do playground de camadas ocultas ---------- */

const SLATE = [51, 65, 85];
const CYAN = [34, 211, 238];
const ROSE = [251, 113, 133];
function lerp(a, b, t) { return a + (b - a) * t; }
function lerpColor(c1, c2, t) {
  return `rgb(${Math.round(lerp(c1[0], c2[0], t))},${Math.round(lerp(c1[1], c2[1], t))},${Math.round(lerp(c1[2], c2[2], t))})`;
}
function activationColor(value, range) {
  const [lo, hi] = range;
  if (lo < 0) {
    if (value >= 0) return lerpColor(SLATE, CYAN, Math.min(1, value / hi));
    return lerpColor(SLATE, ROSE, Math.min(1, value / lo));
  }
  return lerpColor(SLATE, CYAN, Math.min(1, Math.max(0, value / hi)));
}

const H_SIZE = 12;
const EPOCHS = 150;
const LR = 0.15;
const TOP_K = 6;
const MAX_WORDS = 14;

const DWIDTH = 640, DHEIGHT = 360, DMARGIN_Y = 30;

export default function SentenceCompletionPlayground() {
  const [model, setModel] = useState(null);
  const [vocabData, setVocabData] = useState(null);
  const [sentence, setSentence] = useState([]);
  const [finished, setFinished] = useState(false);
  const [autoPlaying, setAutoPlaying] = useState(false);
  const [trainKey, setTrainKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setModel(null);
    const timer = setTimeout(() => {
      const vd = buildVocabAndPairs(RAW_SENTENCES);
      const m = initModel(vd.vocab.length, H_SIZE);
      trainModel(m, vd.pairs, EPOCHS, LR);
      if (!cancelled) {
        setVocabData(vd);
        setModel(m);
        setSentence([]);
        setFinished(false);
        setAutoPlaying(false);
      }
    }, 30);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [trainKey]);

  const prediction = useMemo(() => {
    if (!model || !vocabData) return null;
    const ctxWord = sentence.length ? sentence[sentence.length - 1] : START;
    const ctxIdx = vocabData.word2idx[ctxWord];
    const { h, probs } = forward(model, ctxIdx);
    const ranked = probs
      .map((p, i) => ({ word: vocabData.vocab[i], idx: i, p }))
      .filter((r) => r.word !== START)
      .sort((a, b) => b.p - a.p)
      .slice(0, TOP_K);
    return { ctxWord, ctxIdx, h, ranked };
  }, [model, vocabData, sentence]);

  useEffect(() => {
    if (!autoPlaying || !model || !vocabData || finished || !prediction) return;
    const timer = setTimeout(() => {
      const cands = prediction.ranked.slice(0, 5);
      const total = cands.reduce((s, r) => s + r.p, 0);
      let r = Math.random() * total;
      let chosen = cands[0].word;
      for (const c of cands) {
        if (r < c.p) { chosen = c.word; break; }
        r -= c.p;
      }
      if (chosen === END || sentence.length >= MAX_WORDS - 1) {
        setFinished(true);
        setAutoPlaying(false);
      } else {
        setSentence((s) => [...s, chosen]);
      }
    }, 550);
    return () => clearTimeout(timer);
  }, [autoPlaying, sentence, model, vocabData, finished, prediction]);

  function pickWord(word) {
    if (finished) return;
    if (word === END) { setFinished(true); return; }
    setSentence((s) => [...s, word]);
    if (sentence.length + 1 >= MAX_WORDS) setFinished(true);
  }
  function reset() { setSentence([]); setFinished(false); setAutoPlaying(false); }
  function retrain() { setTrainKey((k) => k + 1); }

  const loading = !model || !vocabData || !prediction;

  const maxN = Math.max(1, H_SIZE, prediction ? prediction.ranked.length : 1);
  const spacingY = Math.min(44, (DHEIGHT - 2 * DMARGIN_Y) / Math.max(1, maxN - 1));
  const colXAt = (col) => 90 + col * ((DWIDTH - 180) / 2);
  const colY = (n, i) => DHEIGHT / 2 - ((n - 1) * spacingY) / 2 + i * spacingY;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8">
        <p className="text-xs font-mono uppercase tracking-widest text-cyan-400 mb-2">Playground · Redes Neurais · Parte 2</p>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-50">Como uma rede neural completa uma frase</h1>
        <p className="text-sm text-slate-400 mt-2 max-w-2xl">
          Uma rede pequena é treinada, ao vivo, com {RAW_SENTENCES.length} frases curtas. A cada palavra escolhida, ela
          reage e sugere o que provavelmente vem a seguir.
        </p>
        <div className="inline-flex flex-wrap items-center gap-2 mt-4 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900/60 font-mono text-xs text-slate-400">
          próxima palavra ~ softmax( <span className="text-cyan-400">W2</span> · tanh(<span className="text-cyan-400">W1</span>[palavra] + b1) + b2 )
        </div>

        {loading ? (
          <div className="mt-8 rounded-lg border border-slate-800 bg-slate-900/60 p-8 text-center animate-pulse">
            <p className="text-sm text-slate-400 font-mono">treinando a rede com {RAW_SENTENCES.length} frases…</p>
          </div>
        ) : (
          <div className="flex flex-col lg:flex-row gap-6 mt-6">
            {/* Coluna esquerda: construtor de frase */}
            <div className="w-full lg:w-80 shrink-0 space-y-5">
              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Frase</h3>
                <div className="flex flex-wrap gap-2 min-h-[2.5rem]">
                  {sentence.length === 0 && <span className="text-sm text-slate-500 font-mono">{START}</span>}
                  {sentence.map((w, i) => (
                    <span key={i} className="px-2.5 py-1 rounded-full bg-slate-800 border border-slate-700 text-sm font-mono text-slate-100">
                      {w}
                    </span>
                  ))}
                  {finished && <span className="px-2.5 py-1 rounded-full bg-amber-400/10 border border-amber-400/40 text-sm font-mono text-amber-300">{END}</span>}
                </div>
                {finished && <p className="text-xs text-slate-500 mt-2">✅ a rede considerou a frase encerrada.</p>}

                <div className="flex flex-col gap-2 mt-4">
                  <button
                    onClick={() => setAutoPlaying((p) => !p)}
                    disabled={finished}
                    className="text-sm py-2 rounded bg-cyan-500 hover:bg-cyan-400 disabled:opacity-30 text-slate-950 font-semibold focus:outline-none focus:ring-2 focus:ring-cyan-300"
                  >
                    {autoPlaying ? '⏸ Parar' : '▶ Deixar a rede completar sozinha'}
                  </button>
                  <div className="flex gap-2">
                    <button onClick={reset} className="flex-1 text-xs py-1.5 rounded border border-slate-700 text-slate-300 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400/50">
                      🔁 Reiniciar frase
                    </button>
                    <button onClick={retrain} className="flex-1 text-xs py-1.5 rounded border border-slate-700 text-slate-300 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-cyan-400/50">
                      🎓 Retreinar do zero
                    </button>
                  </div>
                </div>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-3">Próxima palavra</h3>
                <div className="space-y-2">
                  {prediction.ranked.map((r) => (
                    <button
                      key={r.word}
                      onClick={() => pickWord(r.word)}
                      disabled={finished}
                      className="w-full text-left disabled:opacity-30 group"
                    >
                      <div className="flex justify-between text-xs mb-1">
                        <span className="font-mono text-slate-200 group-hover:text-cyan-300">{r.word === END ? '⏹ fim da frase' : r.word}</span>
                        <span className="font-mono text-amber-300">{(r.p * 100).toFixed(0)}%</span>
                      </div>
                      <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
                        <div className="h-full bg-amber-400 rounded-full transition-all duration-300" style={{ width: `${Math.max(2, r.p * 100)}%` }} />
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Coluna direita: diagrama da rede */}
            <div className="flex-1 min-w-0">
              <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-2 sm:p-4 overflow-x-auto">
                <svg viewBox={`0 0 ${DWIDTH} ${DHEIGHT + 30}`} className="w-full" style={{ minWidth: 500 }}>
                  {Array.from({ length: H_SIZE }).map((_, j) => {
                    const w = model.W1[prediction.ctxIdx][j];
                    const opacity = Math.min(1, Math.abs(w)) * 0.6 + 0.08;
                    return (
                      <line
                        key={`e1-${j}`}
                        x1={colXAt(0)} y1={DHEIGHT / 2}
                        x2={colXAt(1)} y2={colY(H_SIZE, j)}
                        stroke={w >= 0 ? '#22d3ee' : '#fb7185'}
                        strokeWidth={1}
                        opacity={opacity}
                      />
                    );
                  })}

                  {prediction.ranked.map((r, oi) =>
                    Array.from({ length: H_SIZE }).map((_, j) => {
                      const w = model.W2[j][r.idx];
                      const opacity = Math.min(1, Math.abs(w)) * 0.5 + 0.05;
                      return (
                        <line
                          key={`e2-${oi}-${j}`}
                          x1={colXAt(1)} y1={colY(H_SIZE, j)}
                          x2={colXAt(2)} y2={colY(prediction.ranked.length, oi)}
                          stroke={w >= 0 ? '#22d3ee' : '#fb7185'}
                          strokeWidth={1}
                          opacity={opacity}
                        />
                      );
                    })
                  )}

                  <g>
                    <rect x={colXAt(0) - 46} y={DHEIGHT / 2 - 16} width="92" height="32" rx="16" fill="#0f172a" stroke="#fbbf24" strokeWidth="1.5" />
                    <text x={colXAt(0)} y={DHEIGHT / 2 + 4} textAnchor="middle" fontSize="11" fontFamily="ui-monospace, monospace" fill="#fbbf24">
                      {prediction.ctxWord}
                    </text>
                  </g>

                  {Array.from({ length: H_SIZE }).map((_, j) => (
                    <circle key={`h-${j}`} cx={colXAt(1)} cy={colY(H_SIZE, j)} r={11} fill={activationColor(prediction.h[j], [-1, 1])} stroke="#475569" strokeWidth="1">
                      <title>{`neurônio oculto ${j + 1}: ${prediction.h[j].toFixed(3)}`}</title>
                    </circle>
                  ))}

                  {prediction.ranked.map((r, oi) => (
                    <g key={`o-${oi}`} className="cursor-pointer" onClick={() => pickWord(r.word)}>
                      <rect
                        x={colXAt(2) - 58} y={colY(prediction.ranked.length, oi) - 13}
                        width="116" height="26" rx="13"
                        fill={activationColor(r.p, [0, 1])} stroke="#475569" strokeWidth="1"
                      />
                      <text x={colXAt(2)} y={colY(prediction.ranked.length, oi) + 4} textAnchor="middle" fontSize="10" fontFamily="ui-monospace, monospace" fill="#0f172a">
                        {(r.word === END ? '⏹ fim' : r.word).slice(0, 12)}
                      </text>
                    </g>
                  ))}

                  <text x={colXAt(0)} y={DHEIGHT + 20} textAnchor="middle" fontSize="11" fill="#7c88aa" fontFamily="ui-monospace, monospace">PALAVRA ATUAL</text>
                  <text x={colXAt(1)} y={DHEIGHT + 20} textAnchor="middle" fontSize="11" fill="#7c88aa" fontFamily="ui-monospace, monospace">CAMADA OCULTA</text>
                  <text x={colXAt(2)} y={DHEIGHT + 20} textAnchor="middle" fontSize="11" fill="#7c88aa" fontFamily="ui-monospace, monospace">CANDIDATAS</text>
                </svg>
              </div>

              <div className="rounded-lg border border-slate-800 bg-slate-900/60 p-4 mt-4">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Vetor interno da palavra atual</h3>
                <div className="flex gap-1">
                  {prediction.h.map((v, j) => (
                    <div key={j} className="flex-1 h-6 rounded" style={{ background: activationColor(v, [-1, 1]) }} title={v.toFixed(3)} />
                  ))}
                </div>
                <p className="text-xs text-slate-500 mt-2">
                  Esses {H_SIZE} números são como a rede representa "{prediction.ctxWord}" por dentro. Palavras usadas em
                  contextos parecidos tendem a ter vetores parecidos.
                </p>
              </div>

              <p className="text-xs text-slate-500 mt-4 max-w-2xl">
                Essa rede só olha para a última palavra escolhida — é um modelo bem simples (um "bigrama neural"), então
                ela esquece o resto da frase. É uma limitação real desse tipo de arquitetura, e é justamente o problema
                que redes maiores (como Transformers) resolvem lembrando de contextos bem mais longos.
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
