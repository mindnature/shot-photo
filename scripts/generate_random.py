#!/usr/bin/env python3
"""Shot Photo v0.6 — Images 2.5 Random Director.

High-diversity photography exploration for GPT Image / Images 2.5.
Randomness is intentionally strong at the photographer-profile, scene-cluster,
observation-relationship and camera-language levels. The planner keeps the existing
scene/lens/light compatibility logic, while the final prompt is deliberately shorter
than Standard Director prompts so Images 2.5 retains room to invent.
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
    "observation_relationship",
]

OBSERVATION_RELATIONSHIPS = [
    "像同行同学顺手拍到一样近距离观察",
    "从几步之外的中距离安静观察",
    "从路过者视角偶然记录",
    "在人物行进方向侧前方跟拍",
    "从人物身后略偏侧的位置观察",
    "从人群边缘留出一点遮挡观察",
    "隔着门框边缘观察",
    "隔着玻璃反射轻微观察",
    "从台阶下方略低的位置观察",
    "从楼梯或栏杆上方略高的位置观察",
    "在街道或走廊另一侧远距离观察",
    "让人物经过镜头而不是为镜头停下",
    "在人群流动中抓住一瞬间",
    "像朋友坐在旁边随手记录",
    "从环境物边缘探入画面观察",
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
    matches = [(key, values) for key, values in expansions.items() if key in scene or scene in key]
    if not matches:
        return [scene]
    matches.sort(key=lambda item: len(item[0]), reverse=True)
    return list(matches[0][1])


def dilute_taste(taste: Dict[str, Any] | None, strength: str) -> Dict[str, Any] | None:
    if not taste:
        return None
    # Images 2.5 v0.6: exploration should dominate in strong/wild.
    factor = {"balanced": 0.60, "strong": 0.15, "wild": 0.05}[strength]
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

    # Strong/wild rotate through the entire profile library instead of converging early.
    schedule: List[Dict[str, Any]] = []
    while len(schedule) < count:
        pool = list(profiles)
        rng.shuffle(pool)
        schedule.extend(pool)
    return schedule[:count]


def choose_observation(
    rng: random.Random,
    previous: List[Dict[str, str]],
    strength: str,
) -> str:
    used = {shot.get("observation_relationship") for shot in previous}
    if strength in {"strong", "wild"}:
        unused = [item for item in OBSERVATION_RELATIONSHIPS if item not in used]
        if unused:
            return rng.choice(unused)
    return rng.choice(OBSERVATION_RELATIONSHIPS)


def too_similar(candidate: Dict[str, str], previous: List[Dict[str, str]], strength: str) -> bool:
    if not previous:
        return False
    # Lower threshold means stronger diversity pressure.
    threshold = {"balanced": 5, "strong": 3, "wild": 2}[strength]
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
    """Break stylistic convergence while preserving compatibility-sensitive fields."""
    shot = dict(shot)
    shot["expression"] = rng.choice(variables["expressions"])
    shot["wardrobe"] = rng.choice(variables["wardrobe_styles"])
    shot["palette"] = rng.choice(variables["palettes"])
    # Do not override lens/light/foreground after compatibility checks.
    return shot


def first_imperfection(shot: Dict[str, str]) -> str:
    value = shot.get("imperfections", "").strip()
    if not value:
        return ""
    return value.split("、")[0].strip()


def render_random_prompt(
    shot: Dict[str, str],
    subject: str,
    ratio: str,
    profile: Dict[str, Any],
    strength: str,
    rng: random.Random,
) -> str:
    """Render a shorter Images 2.5-native prompt.

    Internal planning remains rich, but the final prompt deliberately surfaces only
    the relationships that define this photograph. This prevents the random plan
    from collapsing back into one exhaustive template.
    """
    scene = shot["scene"]
    moment = shot["moment"]
    observation = shot["observation_relationship"]
    composition = shot["composition"]
    lighting = shot["lighting"]
    foreground = shot["foreground"]
    imperfection = first_imperfection(shot)

    if strength == "balanced":
        imperfection_text = f"保留一点{imperfection}。" if imperfection else ""
        return (
            f"{ratio}，真实生活摄影。{subject}在{scene}，穿着{shot['wardrobe']}，"
            f"正处于{moment}的进行中瞬间，神情{shot['expression']}。"
            f"摄影师{observation}，以{shot['camera_position']}拍摄，"
            f"用{shot['lens']}形成{shot['shot_size']}，重点采用{composition}。"
            f"{foreground}只作为轻微空间层次，主光来自{lighting}，色彩倾向{shot['palette']}。"
            f"{imperfection_text}避免影楼式精修、塑料皮肤和标准摆拍。"
        )

    if strength == "strong":
        # Surface either lens or shot size, not both every time.
        camera_cue = rng.choice([
            f"以{shot['lens']}的自然透视记录",
            f"形成{shot['shot_size']}的观看距离",
            f"从{shot['camera_position']}完成观察",
        ])
        space_cue = rng.choice([
            f"{foreground}从现场边缘轻微进入画面",
            "让真实环境保留足够空间，不把人物自动塞满画面",
            f"画面以{composition}作为唯一主要构图亮点",
        ])
        return (
            f"{ratio}，真实手机感生活摄影。{subject}在{scene}，"
            f"被拍到{moment}的未完成瞬间。摄影师{observation}，{camera_cue}；"
            f"{space_cue}。光线只强调{lighting}，保持颜色简单可信。"
            f"像偶然拍到的真实照片，避免精修摆拍感。"
        )

    # Wild: lock fewer details and leave Images 2.5 more invention space.
    camera_hint = rng.choice([
        f"采用{shot['camera_position']}这种不常见但合理的观察位置",
        f"用{shot['lens']}带来的距离感建立画面",
        f"让{shot['shot_size']}和环境比例形成明显反差",
        f"以{composition}作为这张图唯一鲜明的构图决定",
    ])
    return (
        f"{ratio}，真实生活摄影。为{subject}在{scene}创造一张意外但可信的照片："
        f"捕捉{moment}，不要摆好姿势。摄影师{observation}，{camera_hint}。"
        f"现场只使用{lighting}这一个主要光线逻辑，其余细节自由发挥。"
        f"保持日常可信，不要商业写真感。"
    )


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

        for _ in range(160):
            if scene_pool:
                used_scenes = {x["shot"]["scene"] for x in results}
                unused = [s for s in scene_pool if s not in used_scenes]
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

            shot["observation_relationship"] = choose_observation(rng, accepted_shots, strength)

            if too_similar(shot, accepted_shots, strength):
                continue
            accepted = shot
            break

        if accepted is None:
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
            accepted["observation_relationship"] = choose_observation(rng, accepted_shots, strength)

        accepted_shots.append(accepted)
        prompt = render_random_prompt(accepted, subject, ratio, profile, strength, rng)
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
        "observation_relationships": len({x["shot"]["observation_relationship"] for x in results}),
        "compositions": len({x["shot"]["composition"] for x in results}),
        "lighting": len({x["shot"]["lighting"] for x in results}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Shot Photo v0.6 Images 2.5 random director")
    parser.add_argument("subject", help="主体描述")
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--strength", choices=["balanced", "strong", "wild"], default="strong")
    parser.add_argument("--scene", help="用户锁定的宽泛或具体场景")
    parser.add_argument("--lens", help="用户明确锁定的焦段")
    parser.add_argument("--profile", help="明确锁定摄影人格；不指定时 strong/wild 会跨人格随机")
    parser.add_argument("--intent", default="", help="额外视觉意图")
    parser.add_argument("--ratio", default="9:16 竖幅")
    parser.add_argument("--taste-profile", help="可选个人偏好档案；随机模式会自动大幅弱化影响")
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

    print(f"Random Discovery: {args.strength} · Images 2.5")
    for item in results:
        print(f"\n### {item['index']:02d} · {item['profile']}")
        print(item["prompt"])

    cov = coverage(results)
    print("\n---")
    print("Coverage: " + " | ".join(f"{key}={value}" for key, value in cov.items()))


if __name__ == "__main__":
    main()
