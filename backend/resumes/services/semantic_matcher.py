from sentence_transformers import SentenceTransformer
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
model=SentenceTransformer(MODEL_NAME)

def calculate_semantic_similarity(text1,text2):
    embeddings=model.encode([text1,text2])
    similarity=model.similarity(embeddings[0],embeddings[2])
    return float(similarity.item())