#!/usr/bin/env python3
"""Shot Photo v0.1 — deterministic photography shot planner for GPT Image.

This script does not call an image API. It selects a coherent photography plan from
Shot Photo's reference libraries, then renders a GPT Image-friendly natural-language
prompt. The Skill itself may reason beyond this script; the script is provided for
repeatable batches, seeds, testing and future preference learning.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any, Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def load_json(name: str) -> Dict[str, Any]:
    with (REF / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def pick(seq: Sequence[Any], rng: random.Random) -> Any:
    return seq[rng.randrange(len(seq))]


def weighted_preference(
    candidates: Sequence[Any],
    preferred: Sequence[str],
    rng: random.Random,
    value_getter=lambda x: x,
    boost: float = 4.0,
) -> Any:
    """Bias toward profile preferences without making them hard constraints."""
    if not candidates:
        raise ValueError("No candidates available")
    preferred_set = set(preferred or [])
    weights = []
    for item in candidates:
        value = value_getter(item)
        weights.append(boost if value in preferred_set else 1.0)
    return rng.choices(list(candidates), weights=weights, k=1)[0]


def infer_profile(query: str, profiles: List[Dict[str, Any]]) -> Dict[str, Any]:
    q = query.lower()
    keyword_map = {
        "东方盛夏": ["盛夏", "荷塘", "竹林", "溪", "白墙", "夏日", "夏天"],
        "都市疏离": ["都市", "天台", "停车场", "玻璃", "疏离", "冷淡"],
        "雨夜电影": ["雨夜", "雨后", "夜", "湿", "电影"],
        "日常观察": ["日常", "生活", "自然", "朋友", "居家"],
        "旅行日记": ["旅行", "海边", "渡轮", "车站", "旅馆", "公路"],
        "自然诗意": ["诗意", "自然", "山野", "芦苇", "草地", "树林"],
        "CCD青春": ["ccd", "青春", "直闪", "数码相机", "朋友"],
        "建筑人像": ["建筑", "美术馆", "长廊", "楼梯", "几何"],
        "安静室内": ["室内", "窗边", "卧室", "书桌", "安静"],
        "纪实街拍": ["街拍", "纪实", "市场", "街头", "路人"]
    }
    scores = {p["name"]: 0 for p in profiles}
    for name, words in keyword_map.items():
        for word in words:
            if word.lower() in q:
                scores[name] += 1
    best = max(profiles, key=lambda p: scores.get(p["name"], 0))
    if scores.get(best["name"], 0) == 0:
        return next(p for p in profiles if p["name"] == "日常观察")
    return best


def find_profile(value: str | None, profiles: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
    if not value:
        return infer_profile(query, profiles)
    value_lower = value.lower()
    for p in profiles:
        if value_lower in (p["id"].lower(), p["name"].lower()):
            return p
    raise SystemExit(f"Unknown profile: {value}")


def scene_candidates(variables: Dict[str, Any], profile: Dict[str, Any], fixed_scene: str | None) -> List[Dict[str, Any]]:
    scenes = variables["scenes"]
    if fixed_scene:
        matches = [s for s in scenes if fixed_scene in s["name"] or s["name"] in fixed_scene]
        if matches:
            return matches
        return [{"id": "USER", "name": fixed_scene, "tags": []}]

    preferred = profile.get("preferred_scenes", [])
    matches = [
        s for s in scenes
        if any(pref in s["name"] or s["name"] in pref for pref in preferred)
    ]
    return matches or scenes


def valid_lenses(
    lenses: List[Dict[str, Any]],
    scene: Dict[str, Any],
    compatibility: Dict[str, Any],
) -> List[Dict[str, Any]]:
    tags = set(scene.get("tags", []))
    avoid = set()
    for tag in tags:
        rule = compatibility.get("scene_rules", {}).get(tag, {})
        avoid.update(rule.get("avoid_lenses", []))
    result = [lens for lens in lenses if lens["name"] not in avoid]
    return result or lenses


def valid_lighting(
    lighting: List[Dict[str, Any]],
    scene: Dict[str, Any],
    compatibility: Dict[str, Any],
) -> List[Dict[str, Any]]:
    tags = set(scene.get("tags", []))
    avoid = set()
    preferred = set()
    for tag in tags:
        rule = compatibility.get("scene_rules", {}).get(tag, {})
        avoid.update(rule.get("avoid_lighting", []))
        preferred.update(rule.get("prefer_lighting", []))

    candidates = [light for light in lighting if light["name"] not in avoid]
    if preferred:
        preferred_items = [light for light in candidates if light["name"] in preferred]
        if preferred_items:
            return preferred_items + candidates
    return candidates or lighting


def foreground_candidates(
    foregrounds: List[Dict[str, Any]],
    scene: Dict[str, Any],
) -> List[Dict[str, Any]]:
    tags = set(scene.get("tags", []))
    matches = [fg for fg in foregrounds if tags.intersection(fg.get("tags", []))]
    return matches or foregrounds


def build_shot(
    variables: Dict[str, Any],
    compatibility: Dict[str, Any],
    profile: Dict[str, Any],
    rng: random.Random,
    fixed_scene: str | None,
    fixed_lens: str | None,
    previous: List[Dict[str, str]],
) -> Dict[str, str]:
    scenes = scene_candidates(variables, profile, fixed_scene)

    for _ in range(40):
        scene = pick(scenes, rng)
        moment = pick(variables["moments"], rng)
        expression = pick(variables["expressions"], rng)
        wardrobe = pick(variables["wardrobe_styles"], rng)
        shot_size = pick(variables["shot_sizes"], rng)

        lenses = valid_lenses(variables["lenses"], scene, compatibility)
        if fixed_lens:
            matched = [x for x in variables["lenses"] if x["name"].lower() == fixed_lens.lower()]
            lens = matched[0] if matched else {"name": fixed_lens, "tags": []}
        else:
            lens = weighted_preference(
                lenses,
                profile.get("preferred_lenses", []),
                rng,
                value_getter=lambda x: x["name"],
            )

        lens_rule = compatibility.get("lens_rules", {}).get(lens["name"], {})
        if shot_size in lens_rule.get("avoid_shots", []):
            continue

        camera_position = weighted_preference(
            variables["camera_positions"],
            profile.get("preferred_angles", []),
            rng,
        )
        composition = weighted_preference(
            variables["compositions"],
            profile.get("composition", []),
            rng,
        )
        foreground = pick(foreground_candidates(variables["foregrounds"], scene), rng)["name"]
        light = weighted_preference(
            valid_lighting(variables["lighting"], scene, compatibility),
            profile.get("lighting", []),
            rng,
            value_getter=lambda x: x["name"],
        )["name"]
        palette = weighted_preference(variables["palettes"], profile.get("palette", []), rng)

        imperfection_count = rng.choices([0, 1, 2], weights=[1, 6, 3], k=1)[0]
        imperfections = rng.sample(variables["imperfections"], k=imperfection_count) if imperfection_count else []

        shot = {
            "scene": scene["name"],
            "moment": moment,
            "expression": expression,
            "wardrobe": wardrobe,
            "shot_size": shot_size,
            "lens": lens["name"],
            "camera_position": camera_position,
            "composition": composition,
            "foreground": foreground,
            "lighting": light,
            "palette": palette,
            "imperfections": "、".join(imperfections),
        }

        # Diversity gate: adjacent shots may not repeat 3 of these 4 dimensions.
        if previous:
            prev = previous[-1]
            dimensions = ["shot_size", "lens", "camera_position", "composition"]
            repeats = sum(shot[d] == prev[d] for d in dimensions)
            if repeats >= 3:
                continue
        return shot

    raise RuntimeError("Unable to build a sufficiently diverse compatible shot")


def render_prompt(
    shot: Dict[str, str],
    subject: str,
    ratio: str,
    profile: Dict[str, Any],
) -> str:
    imperfection_text = ""
    if shot["imperfections"]:
        imperfection_text = f"保留{shot['imperfections']}，但不要为了缺陷感破坏人物身份和画面可读性。"

    return (
        f"{ratio}，真实生活摄影照片。{subject}穿着{shot['wardrobe']}，置身{shot['scene']}。"
        f"画面捕捉TA{shot['moment']}的进行中瞬间，神情是{shot['expression']}，不要刻意服务镜头。"
        f"摄影师以{shot['camera_position']}的观察关系拍摄，使用{shot['lens']}视角形成{shot['shot_size']}；"
        f"构图采用{shot['composition']}。{shot['foreground']}从真实环境中自然进入前景，只形成适度遮挡并增强空间层次。"
        f"主光为{shot['lighting']}，色彩控制为{shot['palette']}，整张图最多保留3—4个主要色块。"
        f"{imperfection_text}整体保持“{profile['name']}”的摄影气质：{profile['intent']}。"
        "不要影楼感，不要标准网红摆拍，不要过度磨皮或塑料皮肤，不要无理由复杂背景，"
        "不要自动把人物移到画面中央，也不要为了漂亮而修正有叙事理由的偏位、遮挡和留白。"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate coherent GPT Image photography prompts")
    parser.add_argument("subject", help="Subject description, e.g. '一位短发中国女性'")
    parser.add_argument("--count", type=int, default=6)
    parser.add_argument("--profile", help="Profile ID or Chinese name")
    parser.add_argument("--scene", help="Lock a scene")
    parser.add_argument("--lens", help="Lock a lens, e.g. 35mm")
    parser.add_argument("--ratio", default="9:16 竖幅")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--intent", default="", help="Free-form intent used for profile inference")
    args = parser.parse_args()

    if not 1 <= args.count <= 30:
        raise SystemExit("--count must be between 1 and 30")

    variables = load_json("variables.json")
    compatibility = load_json("compatibility.json")
    profiles = load_json("photographer_profiles.json")["profiles"]
    query = " ".join(filter(None, [args.subject, args.scene, args.intent]))
    profile = find_profile(args.profile, profiles, query)
    rng = random.Random(args.seed)

    shots: List[Dict[str, str]] = []
    for _ in range(args.count):
        shots.append(
            build_shot(
                variables,
                compatibility,
                profile,
                rng,
                args.scene,
                args.lens,
                shots,
            )
        )

    result = [
        {
            "index": i + 1,
            "profile": profile["name"],
            "plan": shot,
            "prompt": render_prompt(shot, args.subject, args.ratio, profile),
        }
        for i, shot in enumerate(shots)
    ]

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"Profile: {profile['name']}\n")
    for item in result:
        print(f"### {item['index']:02d}\n")
        print(item["prompt"])
        print()


if __name__ == "__main__":
    main()
