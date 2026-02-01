import re

def normalize_title(title: str) -> str:
    """
    Normalize a title by:
    
    - Lowercasing
    - Removing special character
    - Removing extra spaces
    """
    if not title:
        return ""
    
    title = title.lower()

    title = re.sub(r"[^a-z\s]", " ", title)

    title = re.sub(r"\s+", " ", title).strip()

    return title