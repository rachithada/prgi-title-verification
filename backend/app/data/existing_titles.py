import pandas as pd
import os
import numpy as np

from app.utils.normalization import normalize_title
from app.utils.core_title import extract_core_title
from app.data.stopwords import COMMON_STOPWORDS
from sentence_transformers import SentenceTransformer

# 🔥 Load model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

CSV_FILES = [
    os.path.join(BASE_DIR, "dataset", "PRGI1.csv"),
    os.path.join(BASE_DIR, "dataset", "PRGI2.csv"),
    os.path.join(BASE_DIR, "dataset", "PRGI3.csv"),
    os.path.join(BASE_DIR, "dataset", "PRGI4.csv"),
    os.path.join(BASE_DIR, "dataset", "PRGI5.csv"),
]

# ✅ GLOBAL STORAGE
EXISTING_TITLES_LIST = []
EXISTING_CORE_TITLES_LIST = []

# 🔥 Embeddings
TITLE_EMBEDDINGS = None

LOADED = False


# 🔥 REMOVE STOPWORDS FUNCTION
def remove_stopwords(text):
    words = text.lower().split()
    words = [w for w in words if w not in COMMON_STOPWORDS]
    return " ".join(words)


def load_titles():
    global EXISTING_TITLES_LIST, EXISTING_CORE_TITLES_LIST, TITLE_EMBEDDINGS, LOADED

    if LOADED:
        print("⚡ Titles already loaded")
        return

    print("🚀 Loading titles...")

    all_titles = []

    # 🔥 STEP 1: Load CSVs
    for file in CSV_FILES:
        try:
            df = pd.read_csv(file)

            if "Title" in df.columns:
                titles = df["Title"]
            else:
                print(f"⚠️ 'Title' column missing in {file}")
                continue

            titles = titles.dropna().astype(str).tolist()
            all_titles.extend(titles)

        except Exception as e:
            print(f"❌ Error reading {file}: {e}")

    # 🔥 STEP 2: Remove duplicates
    all_titles = list(set(all_titles))
    print(f"📊 Raw unique titles: {len(all_titles)}")

    # 🔥 STEP 3: Normalize + Clean + Filter
    for t in all_titles:
        try:
            normalized = normalize_title(t)
            core = extract_core_title(normalized)

            # 🚨 Basic filtering
            if (
                not normalized
                or not core
                or len(normalized) < 4
                or len(normalized.split()) < 2
            ):
                continue

            # 🔥 REMOVE STOPWORDS (CRITICAL FIX)
            clean_title = remove_stopwords(normalized)

            if not clean_title or len(clean_title.split()) < 1:
                continue

            EXISTING_TITLES_LIST.append(clean_title)
            EXISTING_CORE_TITLES_LIST.append(core)

        except Exception as e:
            print(f"⚠️ Error processing '{t}': {e}")

    print(f"✅ Titles loaded successfully: {len(EXISTING_TITLES_LIST)}")

    # 🔥 STEP 4: Generate embeddings on CLEAN titles
    print("🧠 Generating embeddings...")

    TITLE_EMBEDDINGS = model.encode(
        EXISTING_TITLES_LIST,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    print("✅ Embeddings ready!")

    LOADED = True


# ✅ Backward compatibility
EXISTING_TITLES = EXISTING_TITLES_LIST
EXISTING_CORE_TITLES = EXISTING_CORE_TITLES_LIST