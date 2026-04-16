from rapidfuzz import fuzz
from app.data.existing_titles import (
    EXISTING_CORE_TITLES_LIST,
    EXISTING_TITLES_LIST
)
from app.utils.core_title import extract_core_title


def core_fuzzy_similarity(normalized_title: str, threshold: int = 70):
    input_core = extract_core_title(normalized_title)

    best_score = 0
    closest_match = None

    # ✅ iterate over LIST (correct order)
    for idx, existing_core in enumerate(EXISTING_CORE_TITLES_LIST):
        if not existing_core or not input_core:
            continue

        score = fuzz.ratio(input_core, existing_core)

        if score > best_score:
            best_score = score
            closest_match = EXISTING_TITLES_LIST[idx]

    return best_score >= threshold, closest_match, float(best_score)

