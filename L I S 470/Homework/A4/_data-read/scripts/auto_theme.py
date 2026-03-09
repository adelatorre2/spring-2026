import re
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


# -------------------------
# 1) Read + clean
# -------------------------

 # Resolve paths relative to the A4 project folder (../ from this scripts/ directory)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
IN_CSV  = PROJECT_ROOT / "output" / "notes_to_code.csv"
OUT_CSV = PROJECT_ROOT / "output" / "notes_to_code_autothemed.csv"

if not IN_CSV.exists():
    raise FileNotFoundError(
        f"Could not find input coding sheet: {IN_CSV}\n"
        "Make sure you have generated it first (e.g., run a4.py with --make_coding_sheet), "
        "or adjust IN_CSV to point to the correct file."
    )

df = pd.read_csv(IN_CSV)

def is_junk_row(text: str) -> bool:
    if not isinstance(text, str):
        return True
    t = text.strip().lower()

    # common template / section-header junk
    junk_exact = {
        "observation notes",
        "interpretations",
        "post-session reflection",
        "biggest surprise",
        "questions / follow-up",
        "questions for follow-up / things to explore:",
        "breakdowns / successes",
        "breakdowns & successes",
        "notable quotes (approx / paraphrased if ocr missed)",
        "photos taken (from ale)",
        "areas to document",
        "team debrief notes:",
        "activity being observed:",
        "beliefs / expectations",
        "assumptions — what beliefs or expectations guide their behavior?",
        "needs / values — what matters to the participant? what are they trying to achieve?",
        "observations (what you see/hear) interpretations (what it might mean)",
    }
    if t in junk_exact:
        return True

    # page markers
    if t.startswith("=== page"):
        return True

    # very short fragments are usually noise
    if len(t) < 12:
        return True

    return False

df["text"] = df["text"].fillna("").astype(str).str.strip()
df = df[~df["text"].map(is_junk_row)].copy()

# OPTIONAL: focus on content-rich rows
keep_types = {"observation", "insight", "breakdown", "question"}
df = df[df["note_type"].isin(keep_types)].copy()

# -------------------------
# 2) Vectorize
# -------------------------

def basic_normalize(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[\u2019’]", "'", s)
    s = re.sub(r"[^a-z0-9\s'\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

texts = df["text"].map(basic_normalize).tolist()

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1,2),
    min_df=3,          # ignore super-rare terms
    max_df=0.70,       # ignore ultra-common terms
)
X = vectorizer.fit_transform(texts)

# -------------------------
# 3) Cluster
# -------------------------

# Pick k (themes). Start with 8–14 for LIS470.
k = 10

km = KMeans(n_clusters=k, random_state=7, n_init="auto")
labels = km.fit_predict(X)
df["theme_cluster"] = labels

# -------------------------
# 4) Auto-label clusters (top keywords)
# -------------------------

feature_names = np.array(vectorizer.get_feature_names_out())
centroids = km.cluster_centers_

def label_for_cluster(c: int, topn: int = 6) -> str:
    idx = np.argsort(centroids[c])[::-1][:topn]
    terms = feature_names[idx]

    # turn keyword list into a readable label
    # e.g., "price, deals, budget" -> "Price / Deals / Budget"
    words = []
    for t in terms:
        t = t.replace("-", " ").strip()
        if len(t) <= 2:
            continue
        # keep only first token of bigrams for label cleanliness OR keep full bigram if good
        words.append(t)
    # dedupe, keep order
    seen = set()
    cleaned = []
    for w in words:
        if w not in seen:
            cleaned.append(w)
            seen.add(w)

    pretty = " / ".join([w.title() for w in cleaned[:4]])
    return pretty if pretty else f"Theme {c+1}"

cluster_labels = {c: label_for_cluster(c) for c in range(k)}
df["theme_auto"] = df["theme_cluster"].map(cluster_labels)

# If you want the assignment column filled:
df["theme"] = df["theme_auto"]

# -------------------------
# 5) Write out
# -------------------------

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT_CSV, index=False)

print(f"Wrote: {OUT_CSV}")
print("\nCluster labels:")
for c in range(k):
    print(f"{c}: {cluster_labels[c]}")