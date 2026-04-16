from fastapi import APIRouter
from app.schemas.title import TitleRequest, TitleVerificationResponse
from app.utils.normalization import normalize_title

# Rules
from app.services.disallowed_words_rule import contains_disallowed_word
from app.services.periodicity_rule import violates_periodicity_rule
from app.services.combination_rule import violates_combination_rule

# Similarity engines
from app.services.exact_match import exact_match_exists
from app.services.core_fuzzy_match import core_fuzzy_similarity
from app.services.semantic_match import semantic_similarity
from app.services.fuzzy_match import fuzzy_similarity

# Data
from app.data.existing_titles import EXISTING_TITLES_LIST

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "API router working"
    }


@router.post("/verify-title", response_model=TitleVerificationResponse)
def verify_title(payload: TitleRequest):

    # 🚨 STEP 0: Check if data loaded
    if len(EXISTING_TITLES_LIST) == 0:
        return {
            "submitted_title": payload.title,
            "normalized_title": "",
            "status": "Initializing",
            "verification_probability": 0.0,
            "similarity_percentage": 0.0,
            "closest_match": None,
            "rejection_reasons": [
                "System is loading data, please try again in a few seconds"
            ]
        }

    # 0️⃣ Normalize
    normalized = normalize_title(payload.title) or ""

    # 1️⃣ Disallowed words
    has_bad_word, bad_words = contains_disallowed_word(normalized)
    if has_bad_word:
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": "Rejected",
            "verification_probability": 0.0,
            "similarity_percentage": 100.0,
            "closest_match": None,
            "rejection_reasons": [
                f"Contains disallowed word(s): {', '.join(bad_words)}"
            ]
        }

    # 2️⃣ Periodicity rule
    violates, periodic_words = violates_periodicity_rule(normalized)
    if violates:
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": "Rejected",
            "verification_probability": 0.0,
            "similarity_percentage": 100.0,
            "closest_match": None,
            "rejection_reasons": [
                f"Invalid use of periodicity word(s): {', '.join(periodic_words)}"
            ]
        }

    # 3️⃣ Combination rule
    violates_combo, matched_titles = violates_combination_rule(normalized)
    if violates_combo:
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": "Rejected",
            "verification_probability": 0.0,
            "similarity_percentage": 100.0,
            "closest_match": None,
            "rejection_reasons": [
                f"Title is a combination of existing titles: {', '.join(matched_titles)}"
            ]
        }

    # 4️⃣ Exact match
    if exact_match_exists(normalized):
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": "Rejected",
            "verification_probability": 0.0,
            "similarity_percentage": 100.0,
            "closest_match": normalized.title(),
            "rejection_reasons": [
                "Exact title already exists"
            ]
        }

    # 5️⃣ Core fuzzy similarity
    is_core_similar, core_closest, core_score = core_fuzzy_similarity(normalized)
    if is_core_similar:
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": "Rejected",
            "verification_probability": round(100 - core_score, 2),
            "similarity_percentage": round(core_score, 2),
            "closest_match": core_closest.title() if core_closest else None,
            "rejection_reasons": [
                "Too similar after removing common prefixes/suffixes"
            ]
        }

    # 6️⃣ Fuzzy similarity (IMPORTANT: BEFORE semantic)
    is_similar, closest, score = fuzzy_similarity(normalized)

    if score >= 80:
        status = "Rejected"
    elif score >= 60:
        status = "Risky"
    else:
        status = "Pending"

    # 7️⃣ Semantic similarity (ONLY if needed)
    if score < 60:
        is_semantic_similar, semantic_closest, semantic_score = semantic_similarity(normalized)

        if is_semantic_similar:
            return {
                "submitted_title": payload.title,
                "normalized_title": normalized,
                "status": "Rejected",
                "verification_probability": round(100 - semantic_score, 2),
                "similarity_percentage": round(semantic_score, 2),
                "closest_match": semantic_closest.title() if semantic_closest else None,
                "rejection_reasons": [
                    "Title has same meaning as an existing title",
                    f"Semantic similarity score {round(semantic_score, 2)}% exceeds threshold"
                ]
            }

    # 8️⃣ Return fuzzy result if risky/rejected
    if status in ("Rejected", "Risky"):
        return {
            "submitted_title": payload.title,
            "normalized_title": normalized,
            "status": status,
            "verification_probability": round(100 - score, 2),
            "similarity_percentage": round(score, 2),
            "closest_match": closest.title() if closest else None,
            "rejection_reasons": [
                "Title is highly similar to an existing title",
                f"Similarity score {round(score, 2)}% exceeds threshold"
            ]
        }

    # 9️⃣ Final result
    return {
        "submitted_title": payload.title,
        "normalized_title": normalized,
        "status": "Approved",
        "verification_probability": 100.0,
        "similarity_percentage": 0.0,
        "closest_match": None,
        "rejection_reasons": []
    }