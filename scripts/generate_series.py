#!/usr/bin/env python3
"""Shot Photo v0.8 — Series Entropy / Controlled Chaos planner.

Builds a 4–12 frame GPT Image photo series that strongly preserves identity,
wardrobe, place world and time continuity while deliberately varying camera
position, action state, observation relationship, subject scale, composition,
foreground interference and controlled imperfection.

This script plans prompts only; it does not call an image API.
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
    scene_candidates,
    valid_lenses,
    weighted_preference,
)

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references"


def load_series_recipes() -> Dict[str, Any]:
    with (REF / "series_recipes.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def load_entropy_rules() -> Dict[str, Any]:
    with (REF / "series_entropy_rules.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def scale_recipe(count: int, recipes: Dict[str, Any]) -> List[Dict[str, Any]]:
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


ENTROPY_BLUEPRINTS: List[Dict[str, str]] = [
    {
        "entropy_role": "environment_small_subject",
        "observation_relationship": "稍远处安静观察",
        "subject_scale": "人物小比例大环境",
        "shot_size": "人物小比例大环境",
        "camera_position": "街对面远距离观察",
        "composition": "人物只占画面很小一角",
        "moment": "沿栈道缓慢行走",
        "text_visibility_level": "partial",
    },
    {
        "entropy_role": "walking_companion",
        "observation_relationship": "同行朋友边走边拍",
        "subject_scale": "全身环境关系",
        "shot_size": "全身环境人像",
        "camera_position": "摄影师边走边拍",
        "composition": "不对称构图",
        "moment": "经过镜头时被偶然捕捉",
        "text_visibility_level": "blurred",
    },
    {
        "entropy_role": "object_interaction",
        "observation_relationship": "人物停下来做自己的事时被记录",
        "subject_scale": "三分之二身体与环境",
        "shot_size": "膝上中景",
        "camera_position": "自然平视抓拍",
        "composition": "多层街道空间",
        "moment": "看路牌时短暂停住",
        "text_visibility_level": "partial",
    },
    {
        "entropy_role": "close_emotion",
        "observation_relationship": "从人群空隙里抓到",
        "subject_scale": "近距离情绪",
        "shot_size": "胸像近景",
        "camera_position": "人群之间寻找空隙拍摄",
        "composition": "人物放在极侧边",
        "moment": "听见声音后分神",
        "text_visibility_level": "blurred",
    },
    {
        "entropy_role": "quiet_pause",
        "observation_relationship": "人物停下来做自己的事时被记录",
        "subject_scale": "半身观察",
        "shot_size": "半身环境人像",
        "camera_position": "从椅背后方拍",
        "composition": "中心附近但被真实前景轻微遮挡",
        "moment": "坐在边缘短暂发呆",
        "foreground": "椅背或桌角",
        "imperfection": "边缘路人或物体偶然进入画面",
        "text_visibility_level": "occluded",
    },
    {
        "entropy_role": "reflection_layer",
        "observation_relationship": "从街边店内向外拍",
        "subject_scale": "三分之二身体与环境",
        "shot_size": "半身环境人像",
        "camera_position": "从玻璃门另一侧拍",
        "composition": "玻璃反射与真人局部重叠",
        "moment": "刚走出商店门口",
        "foreground": "玻璃反射",
        "imperfection": "玻璃反射叠影",
        "text_visibility_level": "occluded",
    },
    {
        "entropy_role": "low_angle_motion",
        "observation_relationship": "从台阶或地面低处向上拍",
        "subject_scale": "全身环境关系",
        "shot_size": "全身环境人像",
        "camera_position": "人物腰部以下的低机位",
        "composition": "对角线构图",
        "moment": "从阴影走进阳光",
        "imperfection": "轻微运动模糊",
        "text_visibility_level": "blurred",
    },
    {
        "entropy_role": "foreground_interruption",
        "observation_relationship": "隔着玻璃或门框观察",
        "subject_scale": "半身观察",
        "shot_size": "腰部中近景",
        "camera_position": "从门框后方拍",
        "composition": "门框式框景",
        "moment": "伸手推开半扇门",
        "foreground": "门框",
        "imperfection": "边缘路人或物体偶然进入画面",
        "text_visibility_level": "occluded",
    },
    {
        "entropy_role": "back_view_exit",
        "observation_relationship": "从人物背后跟拍",
        "subject_scale": "背影或半背影",
        "shot_size": "全身环境人像",
        "camera_position": "从人物背后跟拍",
        "composition": "人物即将走出画面",
        "moment": "准备离开画面",
        "imperfection": "轻微倾斜的手持瞬间",
        "text_visibility_level": "none",
    },
    {
        "entropy_role": "passing_subject",
        "observation_relationship": "人物经过摄影师时被捕捉",
        "subject_scale": "三分之二身体与环境",
        "shot_size": "膝上中景",
        "camera_position": "自然平视抓拍",
        "composition": "强烈近大远小",
        "moment": "走到一半突然停住",
        "imperfection": "小范围自然过曝",
        "text_visibility_level": "blurred",
    },
    {
        "entropy_role": "high_observation",
        "observation_relationship": "稍远处安静观察",
        "subject_scale": "全身环境关系",
        "shot_size": "全身环境人像",
        "camera_position": "明显高位俯拍",
        "composition": "地面占画面大半",
        "moment": "低头调整鞋带",
        "text_visibility_level": "none",
    },
    {
        "entropy_role": "partial_close",
        "observation_relationship": "隔着玻璃或门框观察",
        "subject_scale": "近距离情绪",
        "shot_size": "肩部特写",
        "camera_position": "从窗帘后方拍",
        "composition": "只展示人物局部但保留身份线索",
        "moment": "刚喝完一口冰水",
        "imperfection": "边缘高光轻微溢出",
        "text_visibility_level": "none",
    },
]


def entropy_sequence(count: int, strength: str, rng: random.Random) -> List[Dict[str, str]]:
    """Return diverse deterministic blueprints; wild perturbs their order more strongly."""
    pool = [dict(x) for x in ENTROPY_BLUEPRINTS]
    if strength == "wild":
        rng.shuffle(pool)
    elif strength == "strong" and len(pool) > 3:
        middle = pool[1:-1]
        rng.shuffle(middle)
        pool = [pool[0], *middle, pool[-1]]

    if count <= len(pool):
        # Spread selections across the pool so 4–6 frame series do not sample only one cluster.
        if count == 1:
            return [pool[0]]
        idx = [round(i * (len(pool) - 1) / (count - 1)) for i in range(count)]
        return [dict(pool[i]) for i in idx]

    result: List[Dict[str, str]] = []
    for i in range(count):
        result.append(dict(pool[i % len(pool)]))
    return result


def apply_entropy_blueprint(
    shot: Dict[str, str],
    blueprint: Dict[str, str],
    variables: Dict[str, Any],
) -> None:
    valid_camera = set(variables["camera_positions"])
    valid_comp = set(variables["compositions"])
    valid_moments = set(variables["moments"])
    valid_shots = set(variables["shot_sizes"])
    valid_foregrounds = {x["name"] for x in variables["foregrounds"]}
    valid_imperfections = set(variables["imperfections"])

    for key, valid in (
        ("camera_position", valid_camera),
        ("composition", valid_comp),
        ("moment", valid_moments),
        ("shot_size", valid_shots),
        ("foreground", valid_foregrounds),
        ("imperfection", valid_imperfections),
    ):
        value = blueprint.get(key)
        if value and value in valid:
            shot[key] = value

    shot["observation_relationship"] = blueprint["observation_relationship"]
    shot["subject_scale"] = blueprint["subject_scale"]
    shot["entropy_role"] = blueprint["entropy_role"]
    shot["text_visibility_level"] = blueprint.get("text_visibility_level", "blurred")
    shot["entropy_imperfection"] = "yes" if blueprint.get("imperfection") else "no"


def quota_for_count(count: int, rules: Dict[str, Any]) -> Dict[str, int]:
    raw = rules["nine_image_series"] if count >= 9 else rules["six_image_series"]
    return {k: min(int(v), count) for k, v in raw.items()}


def series_coverage(shots: List[Dict[str, str]]) -> Dict[str, int]:
    occlusion_names = {"玻璃反射", "椅背或桌角", "门框", "窗框", "路过行人的虚影", "栏杆"}
    return {
        "shot_sizes": len({s.get("shot_size") for s in shots}),
        "camera_positions": len({s.get("camera_position") for s in shots}),
        "action_states": len({s.get("moment") for s in shots}),
        "compositions": len({s.get("composition") for s in shots}),
        "observation_relationships": len({s.get("observation_relationship") for s in shots}),
        "occlusion_or_reflection_images": sum(
            1 for s in shots
            if s.get("foreground") in occlusion_names
            or "反射" in s.get("composition", "")
            or "遮挡" in s.get("composition", "")
        ),
        "small_subject_environment_images": sum(
            1 for s in shots
            if s.get("subject_scale") == "人物小比例大环境"
            or s.get("shot_size") == "人物小比例大环境"
        ),
        "back_or_partial_back_images": sum(
            1 for s in shots
            if "背后" in s.get("observation_relationship", "")
            or "背影" in s.get("subject_scale", "")
        ),
        "imperfect_images": sum(1 for s in shots if s.get("entropy_imperfection") == "yes"),
    }


def validate_coverage(coverage: Dict[str, int], quota: Dict[str, int]) -> List[str]:
    mapping = {
        "min_unique_shot_sizes": "shot_sizes",
        "min_unique_camera_positions": "camera_positions",
        "min_unique_action_states": "action_states",
        "min_unique_compositions": "compositions",
        "min_unique_observation_relationships": "observation_relationships",
        "min_occlusion_or_reflection_images": "occlusion_or_reflection_images",
        "min_small_subject_environment_images": "small_subject_environment_images",
        "min_back_or_partial_back_images": "back_or_partial_back_images",
        "min_imperfect_images": "imperfect_images",
    }
    failures = []
    for quota_key, coverage_key in mapping.items():
        if coverage.get(coverage_key, 0) < quota.get(quota_key, 0):
            failures.append(
                f"{coverage_key}: {coverage.get(coverage_key, 0)} < {quota.get(quota_key, 0)}"
            )
    return failures


def render_series_prompt(
    shot: Dict[str, str],
    subject: str,
    ratio: str,
    role: Dict[str, Any],
    identity_anchor: str,
    wardrobe: str,
    time_arc: str,
    text_suppression: bool,
) -> str:
    identity = identity_anchor or "保持同一人物身份、发型、年龄感和体型比例，不换脸。"
    time_note = (
        "与整组保持同一短时间段和天气。"
        if time_arc == "static"
        else "与整组保持同一次拍摄的自然时间推进。"
    )
    text_note = (
        "背景招牌只作为环境纹理，文字优先局部、模糊、被遮挡或裁切，不生成大段完整宣传文字。"
        if text_suppression
        else ""
    )
    imperfection = ""
    if shot.get("entropy_imperfection") == "yes":
        imperfection = f"允许{shot.get('imperfection', '轻微真实摄影不完美')}，但不要做成统一滤镜。"

    return (
        f"{ratio}真实生活摄影。{identity}保持同一套{wardrobe}，{time_note}"
        f"这一张在系列中是“{role['name']}”，摄影差异角色是 {shot['entropy_role']}。"
        f"{subject}在{shot['scene']}，{shot['moment']}。"
        f"摄影师以“{shot['observation_relationship']}”记录，人物尺度为{shot['subject_scale']}，"
        f"采用{shot['composition']}，机位为{shot['camera_position']}。"
        f"光线保持{shot['lighting']}的真实现场关系。{imperfection}{text_note}"
        "不要标准摆拍，不要把每一张都做成旅游宣传片或商业写真。"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a controlled-chaos GPT Image photo series")
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
    parser.add_argument(
        "--entropy-strength",
        choices=["balanced", "strong", "wild"],
        default="strong",
        help="How aggressively camera/action/composition vary while continuity stays locked",
    )
    parser.add_argument("--identity-anchor", default="", help="Extra same-person continuity instruction")
    parser.add_argument("--wardrobe", help="Lock wardrobe wording for all frames")
    parser.add_argument(
        "--allow-readable-text",
        action="store_true",
        help="Allow clearly readable background signage; suppressed by default",
    )
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    if not 4 <= args.count <= 12:
        raise SystemExit("--count must be between 4 and 12")

    variables = load_json("variables.json")
    compatibility = load_json("compatibility.json")
    profiles = load_json("photographer_profiles.json")["profiles"]
    taste = load_taste(args.taste_profile)
    recipes = load_series_recipes()
    entropy_rules = load_entropy_rules()
    rng = random.Random(args.seed)

    query = " ".join(filter(None, [args.subject, args.scene, args.intent]))
    profile = find_profile(args.profile, profiles, query, taste)
    roles = scale_recipe(args.count, recipes)
    blueprints = entropy_sequence(args.count, args.entropy_strength, rng)
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

    for i, (role, blueprint) in enumerate(zip(roles, blueprints)):
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
        apply_entropy_blueprint(shot, blueprint, variables)
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

        if args.time_arc == "static":
            if base_light is None:
                base_light = shot["lighting"]
            else:
                shot["lighting"] = base_light

        shot["series_role"] = role["name"]
        shots.append(shot)

    coverage = series_coverage(shots)
    quota = quota_for_count(args.count, entropy_rules)
    failures = validate_coverage(coverage, quota)
    if failures:
        raise SystemExit("Series Entropy coverage failed: " + "; ".join(failures))

    text_suppression = bool(entropy_rules.get("text_suppression_default", True)) and not args.allow_readable_text
    result = []
    for i, (shot, role) in enumerate(zip(shots, roles), start=1):
        result.append(
            {
                "index": i,
                "role": role["name"],
                "purpose": role["purpose"],
                "entropy_role": shot["entropy_role"],
                "profile": profile["name"],
                "plan": shot,
                "prompt": render_series_prompt(
                    shot,
                    args.subject,
                    args.ratio,
                    role,
                    args.identity_anchor,
                    wardrobe,
                    args.time_arc,
                    text_suppression,
                ),
            }
        )

    series_plan = {
        "version": "0.8",
        "profile": profile["name"],
        "series_mode": args.series_mode,
        "time_arc": args.time_arc,
        "entropy_strength": args.entropy_strength,
        "wardrobe": wardrobe,
        "palette": palette,
        "scenes": [s["name"] for s in scenes],
        "count": args.count,
        "taste_profile": args.taste_profile,
        "text_suppression": text_suppression,
        "coverage": coverage,
        "quota": quota,
    }

    if args.format == "json":
        print(json.dumps({"series": series_plan, "shots": result}, ensure_ascii=False, indent=2))
        return

    print(f"Series Profile: {profile['name']}")
    print(f"Mode: {args.series_mode} | Time: {args.time_arc} | Entropy: {args.entropy_strength}")
    print(f"Wardrobe: {wardrobe}")
    print(f"Palette: {palette}")
    print(f"Coverage: {coverage}")
    print()

    for item in result:
        print(f"### {item['index']:02d}｜{item['role']}｜{item['entropy_role']}\n")
        print(item["prompt"])
        print()


if __name__ == "__main__":
    main()
