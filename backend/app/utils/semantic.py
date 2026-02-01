from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """
    convert text to semantic vector
    """

    return _model.encode(text, normalize_embeddings=True)