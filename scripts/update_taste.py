#!/usr/bin/env python3
"""Update a Shot Photo personal taste profile from explicit feedback.

Examples:
  python scripts/update_taste.py examples/siran_taste.json \
    --like lenses=35mm \
    --like compositions=人物放在极侧边 \
    --dislike imperfections=轻微数码噪点

  python scripts/update_taste.py examples/siran_taste.json \
    --feedback feedback.json

Feedback JSON format:
{
  "rating": 2,
  "dimensions": {
    "lenses": ["35mm"],
    "compositions": ["人物放在极侧边"]
  },
  "note": "喜欢摄影距离和留白"
}

rating accepts -2, -1, 1, 2. Scores are clipped to [-3, 3].
The updater stores evidence counts separately so one accidental choice cannot
immediately dominate the photographer profile.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Tuple

VALID_DIMENSIONS = {
    "profiles",
    "scenes",
    "moments",
    "expressions",
    "wardrobe_styles",
    "shot_sizes",
    "lenses",
    "camera_positions",
    "compositions",
    "foregrounds",
    "lighting",
    "palettes",
    "imperfections",
}

ALIASES = {
    "profile": "profiles",
    "scene": "scenes",
    "moment": "moments",
    "expression": "expressions",
    "wardrobe": "wardrobe_styles",
    "shot_size": "shot_sizes",
    "lens": "lenses",
    "camera_position": "camera_positions",
    "composition": "compositions",
    "foreground": "foregrounds",
    "light": "lighting",
    "palette": "palettes",
    "imperfection": "imperfections",
}


def canonical_dimension(value: str) -> str:
    key = value.strip()
    key = ALIASES.get(key, key)
    if key not in VALID_DIMENSIONS:
        raise ValueError(f"Unknown taste dimension: {value}")
    return key


def load_profile(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        profile = json.load(f)
    profile.setdefault("learning_rate", 1.0)
    profile.setdefault("sample_count", 0)
    profile.setdefault("dimensions", {})
    profile.setdefault("notes", [])
    for dimension in VALID_DIMENSIONS:
        profile["dimensions"].setdefault(dimension, {})
    return profile


def parse_pair(text: str) -> Tuple[str, str]:
    if "=" not in text:
        raise ValueError(f"Expected DIMENSION=VALUE, got: {text}")
    dimension, value = text.split("=", 1)
    return canonical_dimension(dimension), value.strip()


def clamp(value: float, minimum: float = -3.0, maximum: float = 3.0) -> float:
    return max(minimum, min(maximum, value))


def apply_feedback(profile: Dict[str, Any], dimension: str, value: str, rating: float, stamp: str) -> None:
    bucket = profile["dimensions"].setdefault(dimension, {})
    record = bucket.setdefault(value, {"score": 0.0, "evidence": 0, "last_feedback": None})
    learning_rate = float(profile.get("learning_rate", 1.0))

    # Diminishing update: repeated evidence still matters, but early single examples
    # do not permanently lock the profile.
    evidence = int(record.get("evidence", 0))
    damping = 1.0 / (1.0 + 0.18 * evidence)
    delta = float(rating) * learning_rate * damping
    record["score"] = round(clamp(float(record.get("score", 0.0)) + delta), 3)
    record["evidence"] = evidence + 1
    record["last_feedback"] = stamp


def iter_feedback_payload(payload: Dict[str, Any]) -> Iterable[Tuple[str, str, float]]:
    rating = float(payload.get("rating", 1))
    if rating == 0 or rating < -2 or rating > 2:
        raise ValueError("feedback rating must be one of -2, -1, 1, 2")
    dimensions = payload.get("dimensions", {})
    for raw_dimension, raw_values in dimensions.items():
        dimension = canonical_dimension(raw_dimension)
        values = raw_values if isinstance(raw_values, list) else [raw_values]
        for value in values:
            if str(value).strip():
                yield dimension, str(value).strip(), rating


def main() -> None:
    parser = argparse.ArgumentParser(description="Update Shot Photo personal taste weights")
    parser.add_argument("profile", type=Path, help="Path to taste profile JSON")
    parser.add_argument("--like", action="append", default=[], metavar="DIMENSION=VALUE")
    parser.add_argument("--strong-like", action="append", default=[], metavar="DIMENSION=VALUE")
    parser.add_argument("--dislike", action="append", default=[], metavar="DIMENSION=VALUE")
    parser.add_argument("--strong-dislike", action="append", default=[], metavar="DIMENSION=VALUE")
    parser.add_argument("--feedback", type=Path, help="JSON feedback payload")
    parser.add_argument("--note", action="append", default=[])
    args = parser.parse_args()

    profile = load_profile(args.profile)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    updates = []

    for item in args.like:
        dimension, value = parse_pair(item)
        updates.append((dimension, value, 1.0))
    for item in args.strong_like:
        dimension, value = parse_pair(item)
        updates.append((dimension, value, 2.0))
    for item in args.dislike:
        dimension, value = parse_pair(item)
        updates.append((dimension, value, -1.0))
    for item in args.strong_dislike:
        dimension, value = parse_pair(item)
        updates.append((dimension, value, -2.0))

    payload_note = None
    if args.feedback:
        with args.feedback.open("r", encoding="utf-8") as f:
            payload = json.load(f)
        updates.extend(iter_feedback_payload(payload))
        payload_note = payload.get("note")

    if not updates and not args.note and not payload_note:
        raise SystemExit("No feedback supplied")

    for dimension, value, rating in updates:
        apply_feedback(profile, dimension, value, rating, stamp)

    if updates:
        profile["sample_count"] = int(profile.get("sample_count", 0)) + 1
    for note in [*args.note, payload_note]:
        if note:
            profile.setdefault("notes", []).append(str(note))
    profile["updated_at"] = stamp

    with args.profile.open("w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Updated {args.profile}: {len(updates)} preference signals, sample_count={profile['sample_count']}")


if __name__ == "__main__":
    main()
