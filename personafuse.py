#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import argparse
import os
import re
from difflib import SequenceMatcher
from typing import Any

# -----------------------------
# Dependency handling (SAFE)
# -----------------------------
DEPENDENCIES = {
    "rich": "rich",
    "requests": "requests",
    "beautifulsoup4": "bs4",
    "numpy": "numpy",
    "scikit-learn": "sklearn",
    "Pillow": "PIL",
}

def ensure_packages():
    for pip_name, import_name in DEPENDENCIES.items():
        try:
            __import__(import_name)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

ensure_packages()

from rich.console import Console

# -----------------------------
# Local imports
# -----------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
package_dir = os.path.join(current_dir, "personafuse")
sys.path.insert(0, package_dir)

from platforms import reddit, twitter, instagram, facebook, google
from core import stylometry, temporal
from output.export import save

# -----------------------------
# Optional image matching
# -----------------------------
try:
    from core.image_match import compare_faces
    IMAGE_MATCH_AVAILABLE = True
except Exception:
    IMAGE_MATCH_AVAILABLE = False

# -----------------------------
# Helpers
# -----------------------------
def flatten_to_text(data: Any) -> str:
    if not data:
        return ""

    if isinstance(data, str):
        return data

    if isinstance(data, dict):
        return " ".join(flatten_to_text(v) for v in data.values())

    if isinstance(data, (list, tuple, set)):
        return " ".join(flatten_to_text(i) for i in data)

    return str(data)

def safe_fetch(fetch_func, username, platform, console):
    try:
        return flatten_to_text(fetch_func(username))
    except Exception:
        console.print(f"[yellow]{platform} skipped[/yellow]")
        return ""

def normalize_username(u):
    return re.sub(r"[^a-z0-9]", "", u.lower())

def username_similarity(u1, u2):
    return SequenceMatcher(
        None,
        normalize_username(u1),
        normalize_username(u2)
    ).ratio()

def platform_overlap_score(p1, p2):
    overlap = sum(1 for a, b in zip(p1, p2) if a.strip() and b.strip())
    return overlap / len(p1) if p1 else 0

def confidence_label(score):
    if score < 35:
        return "Inconclusive"
    elif score < 55:
        return "Weak similarity"
    elif score < 75:
        return "Moderate similarity"
    else:
        return "Strong similarity"

# -----------------------------
# Main
# -----------------------------
def main():
    console = Console()

    parser = argparse.ArgumentParser(
        description="PersonaFuse: OSINT username correlation (Level 2)"
    )
    parser.add_argument("user1")
    parser.add_argument("user2")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    # -----------------------------
    # Exact username shortcut
    # -----------------------------
    if normalize_username(args.user1) == normalize_username(args.user2):
        console.print(f"[bold cyan]{args.user1} ↔ {args.user2}[/bold cyan]")
        console.print("Similarity score: [bold]95%[/bold]")
        console.print("Assessment: Strong similarity")
        console.print("[green]Exact normalized username match[/green]")
        return

    # -----------------------------
    # Fetch platform data
    # -----------------------------
    platforms_1 = [
        safe_fetch(reddit.fetch, args.user1, "Reddit", console),
        safe_fetch(twitter.fetch, args.user1, "Twitter", console),
        safe_fetch(instagram.fetch, args.user1, "Instagram", console),
        safe_fetch(facebook.fetch, args.user1, "Facebook", console),
        safe_fetch(google.fetch, args.user1, "Google", console),
    ]

    platforms_2 = [
        safe_fetch(reddit.fetch, args.user2, "Reddit", console),
        safe_fetch(twitter.fetch, args.user2, "Twitter", console),
        safe_fetch(instagram.fetch, args.user2, "Instagram", console),
        safe_fetch(facebook.fetch, args.user2, "Facebook", console),
        safe_fetch(google.fetch, args.user2, "Google", console),
    ]

    text1 = " ".join(platforms_1).strip()
    text2 = " ".join(platforms_2).strip()

    wc1, wc2 = len(text1.split()), len(text2.split())
    min_wc = min(wc1, wc2)

    # -----------------------------
    # Signal extraction
    # -----------------------------
    uname_score = username_similarity(args.user1, args.user2)
    platform_score = platform_overlap_score(platforms_1, platforms_2)
    stylo_score = stylometry.score(text1, text2) * 100 if min_wc >= 120 else 0
    temporal_score = temporal.score([], []) * 100

    # -----------------------------
    # Weighted fusion (Level 2)
    # -----------------------------
    confidence = (
        (uname_score * 100) * 0.30 +
        (platform_score * 100) * 0.35 +
        stylo_score * 0.35
    )

    # Reliability scaling
    if min_wc < 300:
        confidence *= 0.75
    if min_wc < 150:
        confidence *= 0.6

    confidence = int(max(0, min(100, round(confidence))))
    label = confidence_label(confidence)

    # -----------------------------
    # Output
    # -----------------------------
    console.print(f"[bold cyan]{args.user1} ↔ {args.user2}[/bold cyan]")
    console.print(f"Similarity score: [bold]{confidence}%[/bold]")
    console.print(f"Assessment: {label}")

    console.print(f"[dim]• Username similarity: {int(uname_score*100)}%[/dim]")
    console.print(f"[dim]• Platform overlap: {int(platform_score*100)}%[/dim]")

    if min_wc < 120:
        console.print("[yellow]• Stylometry skipped (insufficient text)[/yellow]")
    else:
        console.print(f"[dim]• Stylometry score: {int(stylo_score)}%[/dim]")

    if not IMAGE_MATCH_AVAILABLE:
        console.print("[dim]• Image matching: unavailable on this system[/dim]")

    if min_wc < 300:
        console.print("[yellow]Note: Limited text reduces confidence reliability[/yellow]")

    # -----------------------------
    # JSON export
    # -----------------------------
    if args.json:
        save({
            "users": [args.user1, args.user2],
            "word_count": {
                args.user1: wc1,
                args.user2: wc2,
            },
            "scores": {
                "username_similarity": uname_score,
                "platform_overlap": platform_score,
                "stylometry": stylo_score,
                "temporal": temporal_score,
                "image_available": IMAGE_MATCH_AVAILABLE,
            },
            "final_confidence": confidence,
            "assessment": label,
        })
        console.print("[green]Saved to personafuse_output.json[/green]")

if __name__ == "__main__":
    main()
