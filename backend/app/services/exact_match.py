from app.data.existing_titles import EXISTING_TITLES

def exact_match_exists(normalized_title: str) -> bool:
    return normalized_title in EXISTING_TITLES