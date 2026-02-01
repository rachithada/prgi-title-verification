from app.utils.normalization import normalize_title
from app.utils.core_title import extract_core_title

RAW_EXISTING_TITLES = [
    "The Hindu",
    "Indian Express",
    "Dainik Jagran",
    "Times of India",
    "Hindustan Times",
    "Pratidin Sandhya"
]

EXISTING_TITLES = []
EXISTING_CORE_TITLES = []

for t in RAW_EXISTING_TITLES:
    normalized = normalize_title(t)
    core = extract_core_title(normalized)
    EXISTING_TITLES.append(normalized)
    EXISTING_CORE_TITLES.append(core)
