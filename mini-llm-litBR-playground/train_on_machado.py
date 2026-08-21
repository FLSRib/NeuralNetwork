import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print("=== TREINANDO MINI-LLM COM OBRAS DE MACHADO DE ASSIS ===")

path = r"C:\Users\A57441456\.gemini\antigravity\scratch\corpus_literatura_brasileira.txt"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Usa um trecho de 50.000 caracteres para treino rápido e de alta qualidade
corpus = text[500:50500]
print(f"Corpus carregado com {len(corpus):,} caracteres da literatura brasileira.")

# Tokenização em nível de caractere
vocab = sorted(list(set(corpus)))
char2idx = {c: i for i, c in enumerate(vocab)}
idx2char = {i: c for i, c in enumerate(vocab)}

seq_len = 40
step = 3
sentences = []
next_chars = []

for i in range(0, len(corpus) - seq_len, step):
    sentences.append([char2idx[c] for c in corpus[i : i + seq_len]])
    next_chars.append(char2idx[corpus[i + seq_len]])

X = np.array(sentences)
y = np.array(next_chars)

print(f"Exemplos de treino: {len(X):,} sequências de tamanho {seq_len}.")

# Modelo Keras: Embedding + LSTM + Dense
model = keras.Sequential([
    layers.Embedding(input_dim=len(vocab), output_dim=32, input_length=seq_len),
    layers.LSTM(128),
    layers.Dense(len(vocab), activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Treinando o modelo por 15 épocas...")
model.fit(X, y, batch_size=128, epochs=15, verbose=1)

# Função de geração com Temperatura
def generate_sample(prompt, length=200, temp=0.7):
    current = prompt.lower()
    # garante que os chars do prompt estejam no vocab
    current_idx = [char2idx.get(c, 0) for c in current]
    generated = prompt

    for _ in range(length):
        sub = current_idx[-seq_len:]
        if len(sub) < seq_len:
            sub = [0] * (seq_len - len(sub)) + sub
        
        preds = model.predict(np.array([sub]), verbose=0)[0]
        preds = np.asarray(preds).astype('float64')
        preds = np.log(np.maximum(preds, 1e-9)) / temp
        exp_preds = np.exp(preds)
        probs = exp_preds / np.sum(exp_preds)
        
        next_idx = np.random.choice(len(vocab), p=probs)
        next_char = idx2char[next_idx]
        
        generated += next_char
        current_idx.append(next_idx)

    return generated

print("\n=== TEXTO GERADO NO ESTILO MACHADO DE ASSIS ===")
prompt = "Capitu olhou para mim "
print(generate_sample(prompt, length=250, temp=0.6))
