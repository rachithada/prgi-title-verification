from app.data.periodicity_words import PERIODICITY_WORDS
from app.data.existing_titles import EXISTING_CORE_TITLES
from app.utils.core_title import extract_core_title

def violates_periodicity_rule(normalized_title: str):
    words = normalized_title.split()

    found_periodicity = [w for w in words if w in PERIODICITY_WORDS]

    if not found_periodicity:
        return False, []
    
    core_title = extract_core_title(normalized_title)

    if core_title in EXISTING_CORE_TITLES:
        return True, found_periodicity
    
    return False, []