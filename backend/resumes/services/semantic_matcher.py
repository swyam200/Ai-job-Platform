from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"
model=SentenceTransformer(MODEL_NAME)

def calculate_semantic_similarity(text1,text2):
    embeddings=model.encode([text1,text2])
    similarity=cos_sim(embeddings[0],embeddings[1])
    return float(similarity.item())