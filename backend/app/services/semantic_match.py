import numpy as np
from app.utils.semantic import get_embedding
from app.data.existing_titles import EXISTING_TITLES

def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2))


def semantic_similarity(normalized_title: str, threshold: float = 0.80, min_floor: float = 0.50):
    """
    Returns:
    (is_similar, closest_match, similarity_percentage)
    """
    input_vec = get_embedding(normalized_title)

    best_score = 0.0
    closest_match = None

    for existing in EXISTING_TITLES:
        existing_vec = get_embedding(existing)
        score = cosine_similarity(input_vec, existing_vec)

        if score > best_score:
            best_score = score
            closest_match = existing

    
    if best_score < min_floor:
        return False, None, round(best_score * 100, 2)

    return best_score >= threshold, closest_match, round(best_score * 100, 2)
