from sentence_transformers import SentenceTransformer, util

# Laden des SBERT-Modells
model = SentenceTransformer("all-MiniLM-L6-v2")

# Definieren der zu vergleichenden Sätze
sentence1 = "shall communicate the results thereof to the other Member States and the Commission. "
sentence2 = "one shall thereof communicate the results to the other Member States and the Commission. "

# Berechnen der Einbettungen (Embeddings)
embedding1 = model.encode(sentence1, convert_to_tensor=True)
embedding2 = model.encode(sentence2, convert_to_tensor=True)

# Berechnen der Ähnlichkeit
similarity = util.pytorch_cos_sim(embedding1, embedding2)

print("Ähnlichkeit:", similarity.item())
