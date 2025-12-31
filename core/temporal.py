import numpy as np
from datetime import datetime

# -----------------------------
# Time parsing
# -----------------------------
def _parse_time(t):
    if isinstance(t, (int, float)):
        return float(t)

    if isinstance(t, str):
        try:
            return datetime.fromisoformat(t).timestamp()
        except Exception:
            return None

    return None

# -----------------------------
# Feature extraction
# -----------------------------
def _temporal_features(times):
    parsed = [_parse_time(t) for t in times]
    parsed = [t for t in parsed if t is not None]

    if len(parsed) < 3:
        return None

    parsed.sort()
    intervals = np.diff(parsed)

    return {
        "mean_interval": float(np.mean(intervals)),
        "std_interval": float(np.std(intervals)),
        "active_span": parsed[-1] - parsed[0],
    }

# -----------------------------
# Similarity scoring
# -----------------------------
def _compare_features(f1, f2):
    diffs = []

    for k in f1:
        denom = max(f1[k], f2[k], 1e-6)
        diffs.append(abs(f1[k] - f2[k]) / denom)

    return max(0.0, 1.0 - np.mean(diffs))

# -----------------------------
# Public API
# -----------------------------
def score(times1, times2) -> float:
    """
    Returns temporal similarity score in range 0–100
    """

    f1 = _temporal_features(times1)
    f2 = _temporal_features(times2)

    if not f1 or not f2:
        return 0.0

    similarity = _compare_features(f1, f2)
    return round(similarity * 100, 2)
