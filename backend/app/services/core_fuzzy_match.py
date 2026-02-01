from rapidfuzz import fuzz
from app.data.existing_titles import EXISTING_CORE_TITLES, EXISTING_TITLES
from app.utils.core_title import extract_core_title

def core_fuzzy_similarity(normalized_title: str, threshold: int = 70):
    input_core = extract_core_title(normalized_title)

    best_score = 0
    closest_match = None

    for idx, existing_core in enumerate(EXISTING_CORE_TITLES):
        if not existing_core or not input_core:
            continue

        score = fuzz.ratio(input_core, existing_core)

        if score > best_score:
            best_score = score
            closest_match = EXISTING_TITLES[idx]

    return best_score >= threshold, closest_match, float(best_score)