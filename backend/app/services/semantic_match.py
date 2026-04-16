import numpy as np
from app.data.existing_titles import EXISTING_TITLES_LIST, TITLE_EMBEDDINGS, model
from app.data.stopwords import COMMON_STOPWORDS


# 🔥 Preprocessing (REMOVE GENERIC WORDS)
def preprocess(text):
    words = text.lower().split()
    words = [w for w in words if w not in COMMON_STOPWORDS]
    return " ".join(words)


# 🔥 Word overlap check
def word_overlap(a, b):
    set1 = set(a.split())
    set2 = set(b.split())
    return len(set1 & set2)


def semantic_similarity(normalized_title: str, threshold: float = 0.85, min_floor: float = 0.65):

    # ❌ invalid input
    if not normalized_title or len(normalized_title.split()) < 2:
        return False, None, 0.0

    if TITLE_EMBEDDINGS is None or len(TITLE_EMBEDDINGS) == 0:
        return False, None, 0.0

    # 🔥 STEP 1: preprocess input
    clean_input = preprocess(normalized_title)

    if not clean_input:
        return False, None, 0.0

    # 🔥 STEP 2: encode CLEAN text
    input_vec = model.encode([clean_input])[0]
    embeddings = TITLE_EMBEDDINGS

    similarities = np.dot(embeddings, input_vec) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(input_vec)
    )

    best_idx = int(np.argmax(similarities))
    best_score = float(similarities[best_idx])
    closest_match = EXISTING_TITLES_LIST[best_idx]

    # 🔥 STEP 3: preprocess matched title
    clean_existing = preprocess(closest_match)

    # 🔥 STEP 4: overlap check (STRONG FILTER)
    overlap = word_overlap(clean_input, clean_existing)

    # 🚨 No meaningful match
    if overlap == 0:
        return False, None, 0.0

    # 🚨 Prevent weak matches like "news"
    if overlap == 1:
        return False, None, 0.0

    # 🔥 STEP 5: reduce score for weak overlap
    if overlap <= 1:
        best_score *= 0.5

    similarity_percentage = round(best_score * 100, 2)

    # 🚨 Too low similarity
    if best_score < min_floor:
        return False, None, 0.0

    return best_score >= threshold, closest_match, similarity_percentage