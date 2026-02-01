from app.data.disallowed_words import DISALLOWED_WORDS

def contains_disallowed_word(normalized_title: str):
    words = normalized_title.split()

    found = [w for w in words if w in DISALLOWED_WORDS]

    return len(found) > 0, found