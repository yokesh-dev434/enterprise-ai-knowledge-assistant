from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

text = "Employees use VPN for secure remote access."

def generate_embeddings(chunks):

    embeddings = model.encode(chunks)

    return embeddings