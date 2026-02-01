from rapidfuzz import fuzz
from app.data.existing_titles import EXISTING_TITLES

def fuzzy_similarity(normalized_title: str, threshold: int = 70):
    """
    Returns:
    (is_similar, closest_match, similarity_score)
    """

    best_score = 0
    closest_match = None

    for existing in EXISTING_TITLES:
        score_1 = fuzz.ratio(normalized_title, existing)
        score_2 = fuzz.partial_ratio(normalized_title, existing)
        score_3 = fuzz.token_sort_ratio(normalized_title, existing)

        score = max(score_1, score_2, score_3)

        if score > best_score:
            best_score = score
            closest_match = existing

    return best_score >= threshold, closest_match, float(best_score)