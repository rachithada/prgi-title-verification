from app.data.existing_titles import EXISTING_TITLES

def violates_combination_rule(normalized_title: str):
    """
    Returns:
    (violates: bool, matched_titles: list)
    """

    matched = []

    for existing in EXISTING_TITLES:
        if existing in normalized_title:
            matched.append(existing)

    if len(matched) >= 2:
        return True, matched
    
    return False, []