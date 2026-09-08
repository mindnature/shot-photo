#!/usr/bin/env python3
"""Shot Photo v0.4 — coherent series planner for GPT Image.

Builds a 4–12 frame photo series with identity, wardrobe, palette, scene and shot-rhythm
continuity. It reuses the v0.3 conditional photography and Personal Taste engine, then
adds a sequence-level directing layer.

This script only plans prompts; it does not call an image API.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Sequence

from generate import (
    build_shot,
    find_profile,
    load_json,
    load_taste,
    profile_scene_names,
    render_prompt,
    scene_candidates,
    taste_multiplier,
    valid_lenses,
    weighted_preference,
)

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def load_series_recipes() -> Dict[str, Any]:
    with (REF / "series_recipes.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def scale_recipe(count: int, recipes: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Use exact 6/9 recipes, or scale the 9-frame rhythm to 4–12 frames."""
    key = str(count)
    if key in recipes["recipes"]:
        return recipes["recipes"][key]

    base = recipes["recipes"]["9"]
    if count == 1:
        return [base[0]]
    indices = [round(i * (len(base) - 1) / (count - 1)) for i in range(count)]
    return [base[i] for i in indices]


def choose_named(
    candidates: Sequence[str],
    preferred: Sequence[str],
    rng: random.Random,
    taste: Dict[str, Any] | None,
    dimension: str,
) -> str:
    return weighted_preference(
        candidates,
        preferred,
        rng,
        taste=taste,
        taste_dimension=dimension,
    )


def related_scene_pool(
    variables: Dict[str, Any],
    anchor: Dict[str, Any],
    profile: Dict[str, Any],
) -> List[Dict[str, Any]]:
    anchor_tags = set(anchor.get("tags", []))
    preferred = set(profile_scene_names(variables["scenes"], profile))
    ranked = []
    for scene in variables["scenes"]:
        if scene["name"] == anchor["name"]:
            continue
        overlap = len(anchor_tags.intersection(scene.get("tags", [])))
        bonus = 1 if scene["name"] in preferred else 0
        if overlap > 0 or bonus:
            ranked.append((overlap * 2 + bonus, scene))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [scene for _, scene in ranked]


def choose_anchor_scene(
    variables: Dict[str, Any],
    profile: Dict[str, Any],
    fixed_scene: str | None,
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> Dict[str, Any]:
    scenes = scene_candidates(variables, profile, fixed_scene)
    preferred_names = profile_scene_names(scenes, profile)
    return weighted_preference(
        scenes,
        preferred_names,
        rng,
        value_getter=lambda x: x["name"],
        taste=taste,
        taste_dimension="scenes",
    )


def build_scene_sequence(
    variables: Dict[str, Any],
    profile: Dict[str, Any],
    fixed_scene: str | None,
    mode: str,
    count: int,
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> List[Dict[str, Any]]:
    anchor = choose_anchor_scene(variables, profile, fixed_scene, rng, taste)
    if fixed_scene or mode == "single-location":
        return [anchor] * count

    related = related_scene_pool(variables, anchor, profile)
    cluster = [anchor]
    for scene in related:
        if len(cluster) >= 3:
            break
        cluster.append(scene)

    if len(cluster) == 1:
        return [anchor] * count

    sequence: List[Dict[str, Any]] = []
    for i in range(count):
        index = min(len(cluster) - 1, int(i * len(cluster) / count))
        sequence.append(cluster[index])
    return sequence


def role_shot_size(
    role: Dict[str, Any],
    variables: Dict[str, Any],
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> str:
    preferred = [x for x in role.get("preferred_shot_sizes", []) if x in variables["shot_sizes"]]
    pool = preferred or variables["shot_sizes"]
    return choose_named(pool, preferred, rng, taste, "shot_sizes")


def role_lens(
    role: Dict[str, Any],
    shot_size: str,
    scene: Dict[str, Any],
    variables: Dict[str, Any],
    compatibility: Dict[str, Any],
    profile: Dict[str, Any],
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> str:
    candidates = valid_lenses(variables["lenses"], scene, compatibility)
    role_lenses = set(role.get("preferred_lenses", []))
    filtered = [x for x in candidates if x["name"] in role_lenses] or candidates

    compatible = []
    for lens in filtered:
        rule = compatibility.get("lens_rules", {}).get(lens["name"], {})
        if shot_size not in rule.get("avoid_shots", []):
            compatible.append(lens)
    compatible = compatible or filtered

    return weighted_preference(
        compatible,
        profile.get("preferred_lenses", []),
        rng,
        value_getter=lambda x: x["name"],
        taste=taste,
        taste_dimension="lenses",
    )["name"]


def role_composition(
    role: Dict[str, Any],
    variables: Dict[str, Any],
    profile: Dict[str, Any],
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> str:
    keywords = role.get("composition_keywords", [])
    matches = [
        comp for comp in variables["compositions"]
        if any(keyword in comp for keyword in keywords)
    ]
    pool = matches or variables["compositions"]
    return weighted_preference(
        pool,
        profile.get("composition", []),
        rng,
        taste=taste,
        taste_dimension="compositions",
    )


def ending_moment(
    variables: Dict[str, Any],
    rng: random.Random,
    taste: Dict[str, Any] | None,
) -> str:
    keys = ["准备离开画面", "走到一半突然停住", "侧身看向远处", "靠墙短暂休息", "沿栈道缓慢行走"]
    matches = [m for m in variables["moments"] if any(k in m for k in keys)]
    return choose_named(matches or variables["moments"], [], rng, taste, "moments")


def render_series_prompt(
    shot: Dict[str, str],
    subject: str,
    ratio: str,
    profile: Dict[str, Any],
    role: Dict[str, Any],
    identity_anchor: str,
    time_arc: str,
) -> str:
    base = render_prompt(shot, subject, ratio, profile)
    identity = identity_anchor or (
        "这是同一组连续拍摄中的同一人物；保持相同面部身份、发型、年龄感和体型比例，"
        "不要换脸，不要改变核心外貌特征。"
    )
    time_note = (
        "整组发生在同一短时间段内，保持光线方向、色温与天气连续。"
        if time_arc == "static"
        else "这是同一次拍摄的连续时间推进；后续画面只允许光线自然、渐进地变化，不突然跨越到完全不同的时段。"
    )
    return (
        f"{identity}{time_note}这一张在系列中的作用是“{role['name']}”：{role['purpose']}。"
        + base
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a coherent GPT Image photo series")
    parser.add_argument("subject", help="Subject description")
    parser.add_argument("--count", type=int, default=6, help="4–12 frames; 6 or 9 recommended")
    parser.add_argument("--profile", help="Photographer Profile ID or Chinese name")
    parser.add_argument("--scene", help="Lock one scene for the whole series")
    parser.add_argument("--intent", default="", help="Free-form series intent")
    parser.add_argument("--ratio", default="9:16 竖幅")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--taste-profile", help="Path to a Personal Taste JSON file")
    parser.add_argument(
        "--series-mode",
        choices=["single-location", "micro-journey"],
        default="single-location",
    )
    parser.add_argument(
        "--time-arc",
        choices=["static", "progressive"],
        default="static",
    )
    parser.add_argument("--identity-anchor", default="", help="Extra same-person continuity instruction")
    parser.add_argument("--wardrobe", help="Lock wardrobe wording for all frames")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    if not 4 <= args.count <= 12:
        raise SystemExit("--count must be between 4 and 12")

    variables = load_json("variables.json")
    compatibility = load_json("compatibility.json")
    profiles = load_json("photographer_profiles.json")["profiles"]
    taste = load_taste(args.taste_profile)
    recipes = load_series_recipes()
    rng = random.Random(args.seed)

    query = " ".join(filter(None, [args.subject, args.scene, args.intent]))
    profile = find_profile(args.profile, profiles, query, taste)
    roles = scale_recipe(args.count, recipes)
    scenes = build_scene_sequence(
        variables,
        profile,
        args.scene,
        args.series_mode,
        args.count,
        rng,
        taste,
    )

    wardrobe = args.wardrobe or choose_named(
        variables["wardrobe_styles"], [], rng, taste, "wardrobe_styles"
    )
    palette = weighted_preference(
        variables["palettes"],
        profile.get("palette", []),
        rng,
        taste=taste,
        taste_dimension="palettes",
    )

    shots: List[Dict[str, str]] = []
    base_light: str | None = None

    for i, role in enumerate(roles):
        scene = scenes[i]
        shot = build_shot(
            variables,
            compatibility,
            profile,
            rng,
            scene["name"],
            None,
            shots,
            taste,
        )
        shot["wardrobe"] = wardrobe
        shot["palette"] = palette
        shot["shot_size"] = role_shot_size(role, variables, rng, taste)
        shot["lens"] = role_lens(
            role,
            shot["shot_size"],
            scene,
            variables,
            compatibility,
            profile,
            rng,
            taste,
        )
        shot["composition"] = role_composition(role, variables, profile, rng, taste)

        if i == len(roles) - 1:
            shot["moment"] = ending_moment(variables, rng, taste)

        if args.time_arc == "static":
            if base_light is None:
                base_light = shot["lighting"]
            else:
                shot["lighting"] = base_light

        shot["series_role"] = role["name"]
        shots.append(shot)

    result = []
    for i, (shot, role) in enumerate(zip(shots, roles), start=1):
        result.append(
            {
                "index": i,
                "role": role["name"],
                "purpose": role["purpose"],
                "profile": profile["name"],
                "plan": shot,
                "prompt": render_series_prompt(
                    shot,
                    args.subject,
                    args.ratio,
                    profile,
                    role,
                    args.identity_anchor,
                    args.time_arc,
                ),
            }
        )

    series_plan = {
        "profile": profile["name"],
        "series_mode": args.series_mode,
        "time_arc": args.time_arc,
        "wardrobe": wardrobe,
        "palette": palette,
        "scenes": [s["name"] for s in scenes],
        "count": args.count,
        "taste_profile": args.taste_profile,
    }

    if args.format == "json":
        print(json.dumps({"series": series_plan, "shots": result}, ensure_ascii=False, indent=2))
        return

    print(f"Series Profile: {profile['name']}")
    print(f"Mode: {args.series_mode} | Time: {args.time_arc}")
    print(f"Wardrobe: {wardrobe}")
    print(f"Palette: {palette}")
    if args.taste_profile:
        print(f"Taste: {args.taste_profile}")
    print()

    for item in result:
        print(f"### {item['index']:02d}｜{item['role']}\n")
        print(item["prompt"])
        print()


if __name__ == "__main__":
    main()
