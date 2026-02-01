from app.data.stopwords import COMMON_STOPWORDS

def extract_core_title(normalized_title: str) -> str:
    words = normalized_title.split()
    core_words = [w for w in words if w not in COMMON_STOPWORDS]
    return " ".join(core_words)
