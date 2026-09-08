#!/usr/bin/env python3
"""Shot Photo v0.5 Random Discovery.

High-diversity photography exploration for GPT Image.
Randomness is intentionally strong, but every shot still passes the existing
scene/lens/light compatibility logic in generate.py.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List

from generate import (
    build_shot,
    find_profile,
    infer_profile,
    load_json,
    load_taste,
    render_prompt,
)

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"

CORE_DIMS = [
    "scene",
    "moment",
    "shot_size",
    "lens",
    "camera_position",
    "composition",
    "foreground",
    "lighting",
    "wardrobe",
]


def load_scene_expansions() -> Dict[str, List[str]]:
    path = REF / "random_scene_expansions.json"
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f).get("expansions", {})


def expanded_scene_pool(scene: str | None, expansions: Dict[str, List[str]]) -> List[str] | None:
    if not scene:
        return None
    # Prefer the longest matching key, so more specific concepts win.
    matches = [(key, values) for key, values in expansions.items() if key in scene or scene in key]
    if not matches:
        return [scene]
    matches.sort(key=lambda item: len(item[0]), reverse=True)
    return list(matches[0][1])


def dilute_taste(taste: Dict[str, Any] | None, strength: str) -> Dict[str, Any] | None:
    if not taste:
        return None
    factor = {"balanced": 0.55, "strong": 0.30, "wild": 0.10}[strength]
    clone = json.loads(json.dumps(taste, ensure_ascii=False))
    for values in clone.get("dimensions", {}).values():
        for record in values.values():
            record["score"] = float(record.get("score", 0.0)) * factor
            record["evidence"] = min(int(record.get("evidence", 0)), 2)
    return clone


def profile_schedule(
    profiles: List[Dict[str, Any]],
    count: int,
    rng: random.Random,
    strength: str,
    fixed_profile: str | None,
    query: str,
    taste: Dict[str, Any] | None,
) -> List[Dict[str, Any]]:
    if fixed_profile:
        chosen = find_profile(fixed_profile, profiles, query, taste)
        return [chosen] * count

    if strength == "balanced":
        chosen = infer_profile(query, profiles, taste)
        return [chosen] * count

    # Strong and wild deliberately rotate through different photographer profiles.
    schedule: List[Dict[str, Any]] = []
    pool = list(profiles)
    while len(schedule) < count:
        rng.shuffle(pool)
        schedule.extend(pool)
        pool = list(profiles)
    return schedule[:count]


def too_similar(candidate: Dict[str, str], previous: List[Dict[str, str]], strength: str) -> bool:
    if not previous:
        return False
    threshold = {"balanced": 4, "strong": 3, "wild": 2}[strength]
    for old in previous:
        repeated = sum(candidate.get(dim) == old.get(dim) for dim in CORE_DIMS)
        if repeated >= threshold:
            return True
    return False


def mutate_for_wild(
    shot: Dict[str, str],
    variables: Dict[str, Any],
    rng: random.Random,
) -> Dict[str, str]:
    """Break profile convergence further without breaking core photography logic."""
    shot = dict(shot)
    shot["expression"] = rng.choice(variables["expressions"])
    shot["wardrobe"] = rng.choice(variables["wardrobe_styles"])
    shot["palette"] = rng.choice(variables["palettes"])
    # Do not override lens/light/foreground after compatibility checks.
    return shot


def build_random_batch(
    subject: str,
    count: int,
    strength: str,
    scene: str | None,
    lens: str | None,
    ratio: str,
    profile_name: str | None,
    intent: str,
    taste_path: str | None,
    seed: int | None,
) -> List[Dict[str, Any]]:
    rng = random.Random(seed)
    profiles = load_json("photographer_profiles.json")["profiles"]
    variables = load_json("variables.json")
    compatibility = load_json("compatibility.json")
    expansions = load_scene_expansions()

    raw_taste = load_taste(taste_path)
    taste = dilute_taste(raw_taste, strength)
    query = f"{subject} {intent} {scene or ''}".strip()
    schedule = profile_schedule(profiles, count, rng, strength, profile_name, query, taste)
    scene_pool = expanded_scene_pool(scene, expansions)

    results: List[Dict[str, Any]] = []
    accepted_shots: List[Dict[str, str]] = []

    for index in range(count):
        profile = schedule[index]
        accepted = None
        chosen_scene = None

        for _ in range(120):
            if scene_pool:
                # Prefer scene sub-locations not yet used in the batch.
                used = {x["shot"]["scene"] for x in results}
                unused = [s for s in scene_pool if s not in used]
                chosen_scene = rng.choice(unused or scene_pool)
            else:
                chosen_scene = None

            shot = build_shot(
                variables,
                compatibility,
                profile,
                rng,
                chosen_scene,
                lens,
                accepted_shots,
                taste,
            )
            if strength == "wild":
                shot = mutate_for_wild(shot, variables, rng)

            if too_similar(shot, accepted_shots, strength):
                continue
            accepted = shot
            break

        if accepted is None:
            # Fall back to the compatible base generator rather than fail the batch.
            accepted = build_shot(
                variables,
                compatibility,
                profile,
                rng,
                chosen_scene,
                lens,
                accepted_shots,
                taste,
            )

        accepted_shots.append(accepted)
        prompt = render_prompt(accepted, subject, ratio, profile)
        results.append(
            {
                "index": index + 1,
                "random_strength": strength,
                "profile": profile["name"],
                "shot": accepted,
                "prompt": prompt,
            }
        )

    return results


def coverage(results: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "profiles": len({x["profile"] for x in results}),
        "scenes": len({x["shot"]["scene"] for x in results}),
        "shot_sizes": len({x["shot"]["shot_size"] for x in results}),
        "lenses": len({x["shot"]["lens"] for x in results}),
        "camera_positions": len({x["shot"]["camera_position"] for x in results}),
        "compositions": len({x["shot"]["composition"] for x in results}),
        "lighting": len({x["shot"]["lighting"] for x in results}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Shot Photo strong random discovery generator")
    parser.add_argument("subject", help="主体描述")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--strength", choices=["balanced", "strong", "wild"], default="strong")
    parser.add_argument("--scene", help="用户锁定的宽泛或具体场景")
    parser.add_argument("--lens", help="用户明确锁定的焦段")
    parser.add_argument("--profile", help="明确锁定摄影人格；不指定时 strong/wild 会跨人格随机")
    parser.add_argument("--intent", default="", help="额外视觉意图")
    parser.add_argument("--ratio", default="9:16 竖幅")
    parser.add_argument("--taste-profile", help="可选个人偏好档案；随机模式会自动弱化其影响")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    if not 1 <= args.count <= 30:
        raise SystemExit("--count must be between 1 and 30")

    results = build_random_batch(
        subject=args.subject,
        count=args.count,
        strength=args.strength,
        scene=args.scene,
        lens=args.lens,
        ratio=args.ratio,
        profile_name=args.profile,
        intent=args.intent,
        taste_path=args.taste_profile,
        seed=args.seed,
    )

    if args.format == "json":
        print(json.dumps({"results": results, "coverage": coverage(results)}, ensure_ascii=False, indent=2))
        return

    print(f"Random Discovery: {args.strength}")
    for item in results:
        print(f"\n### {item['index']:02d} · {item['profile']}")
        print(item["prompt"])

    cov = coverage(results)
    print("\n---")
    print(
        "Coverage: "
        + " | ".join(f"{key}={value}" for key, value in cov.items())
    )


if __name__ == "__main__":
    main()
