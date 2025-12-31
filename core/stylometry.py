import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# -----------------------------
# Feature extraction
# -----------------------------
def _safe_mean(arr):
    return float(np.mean(arr)) if arr else 0.0

def extract_style(text: str) -> dict:
    if not text:
        return {
            "avg_word_len": 0.0,
            "sentence_len": 0.0,
            "punct_ratio": 0.0,
            "digit_ratio": 0.0,
            "uppercase_ratio": 0.0,
        }

    words = re.findall(r"\b\w+\b", text)
    sentences = re.split(r"[.!?]", text)
    chars = list(text)

    return {
        "avg_word_len": _safe_mean([len(w) for w in words]),
        "sentence_len": _safe_mean([len(s.split()) for s in sentences if s.strip()]),
        "punct_ratio": sum(c in "!?.,;:" for c in chars) / len(chars),
        "digit_ratio": sum(c.isdigit() for c in chars) / len(chars),
        "uppercase_ratio": sum(c.isupper() for c in chars) / len(chars),
    }

# -----------------------------
# Similarity scoring
# -----------------------------
def _behavioral_similarity(f1: dict, f2: dict) -> float:
    diffs = []

    for k in f1:
        denom = max(f1[k], f2[k], 1e-6)
        diffs.append(abs(f1[k] - f2[k]) / denom)

    avg_diff = np.mean(diffs)
    return max(0.0, 1.0 - avg_diff)

def _lexical_similarity(t1: str, t2: str) -> float:
    try:
        vec = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=5000,
        )
        tfidf = vec.fit_transform([t1, t2])
        return float(cosine_similarity(tfidf)[0][1])
    except Exception:
        return 0.0

# -----------------------------
# Public API
# -----------------------------
def score(text1: str, text2: str) -> float:
    """
    Returns stylistic similarity score in range 0–100
    """

    if not text1 or not text2:
        return 0.0

    lex = _lexical_similarity(text1, text2)
    f1 = extract_style(text1)
    f2 = extract_style(text2)
    beh = _behavioral_similarity(f1, f2)

    final = (lex * 0.65) + (beh * 0.35)
    return round(final * 100, 2)
