import urllib.request
import re
import os

gutenberg_ids = [
    ("Dom Casmurro", 55752),
    ("Memórias Póstumas de Brás Cubas", 54829),
    ("Esaú e Jacó", 55698),
    ("Helena", 55753),
    ("Papéis Avulsos", 55754)
]

output_path = r"C:\Users\A57441456\.gemini\antigravity\scratch\corpus_literatura_brasileira.txt"

combined_text = []

print("=== BAIXANDO OBRAS EM DOMÍNIO PÚBLICO DO PROJECT GUTENBERG ===")

for title, ebook_id in gutenberg_ids:
    url = f"https://www.gutenberg.org/cache/epub/{ebook_id}/pg{ebook_id}.txt"
    print(f"Baixando: {title} (ID: {ebook_id})...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            raw_data = response.read()
            # tenta UTF-8 depois Latin-1
            try:
                content = raw_data.decode('utf-8')
            except Exception:
                content = raw_data.decode('latin-1')

            # Limpeza dos cabeçalhos/rodapés do Gutenberg
            start_idx = content.find("*** START OF THE PROJECT GUTENBERG EBOOK")
            if start_idx != -1:
                start_idx = content.find("\n", start_idx) + 1
                content = content[start_idx:]
            
            end_idx = content.find("*** END OF THE PROJECT GUTENBERG EBOOK")
            if end_idx != -1:
                content = content[:end_idx]

            cleaned = re.sub(r'\r\n', '\n', content)
            cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()

            print(f"  -> Sucesso: {len(cleaned):,} caracteres baixados para '{title}'.")
            combined_text.append(f"\n\n=== {title.upper()} ===\n\n" + cleaned)
    except Exception as e:
        print(f"  -> Erro ao baixar {title}: {e}")

final_corpus = "".join(combined_text)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_corpus)

print(f"\n=== SUCESSO! Corpus literário total salvo em {output_path} ===")
print(f"Tamanho total: {len(final_corpus):,} caracteres ({len(final_corpus)/1024/1024:.2f} MB)")
