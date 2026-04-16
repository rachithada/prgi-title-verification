from rapidfuzz import fuzz
from app.data.existing_titles import EXISTING_TITLES


def word_overlap(a, b):
    set1 = set(a.split())
    set2 = set(b.split())
    return len(set1 & set2)


def fuzzy_similarity(normalized_title: str, threshold: int = 70):

    if not normalized_title or len(normalized_title.split()) < 2:
        return False, None, 0.0

    best_score = 0
    closest_match = None

    for existing in EXISTING_TITLES:

        if not existing or len(existing.split()) < 2:
            continue

        # 🔥 NEW: word overlap check
        overlap = word_overlap(normalized_title, existing)

        if overlap == 0:
            continue  # ❌ skip unrelated titles

        score_1 = fuzz.ratio(normalized_title, existing)
        score_2 = fuzz.partial_ratio(normalized_title, existing)
        score_3 = fuzz.token_sort_ratio(normalized_title, existing)

        score = max(score_1, score_2, score_3)

        if score > best_score:
            best_score = score
            closest_match = existing

    return best_score >= threshold, closest_match, float(best_score)