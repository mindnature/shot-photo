# Personal Taste Learning

Shot Photo v0.3 uses explicit feedback to build a personal photographer profile over time.

The purpose is not to freeze the system into one look. It is to make preferred photographic decisions more likely while preserving exploration.

## Core principle

Personal Taste is a probability layer, not a hard preset.

The base order remains:

```text
user hard anchors
> physical photography compatibility
> selected photographer profile
> personal taste weights
> novelty / exploration
```

Taste must never override an explicit user request or force an impossible camera/light relationship.

## What can be learned

The profile can accumulate preference evidence for:

- photographer profiles
- scenes
- moments
- expressions
- wardrobe styles
- shot sizes
- lenses
- camera positions
- compositions
- foregrounds
- lighting
- palettes
- controlled imperfections

The profile intentionally stores photography choices instead of vague labels such as “高级” or “好看”.

## Feedback scale

Use four practical levels:

```text
strong like      +2
like             +1
dislike          -1
strong dislike   -2
```

Stored scores are clipped to `[-3, +3]`.

A single rating should influence the next batch but should not permanently define the style. Repeated evidence gradually raises confidence.

## Evidence rule

Each preference item stores:

```json
{
  "score": 1.75,
  "evidence": 3,
  "last_feedback": "2026-09-08T13:30:00+00:00"
}
```

`score` expresses direction and strength. `evidence` records how often the preference has been explicitly supported.

The generator dampens low-evidence signals, so one accidental “like” cannot dominate future work.

## Do not infer too aggressively

Do not write a preference merely because an image contains an element.

Example:

- image uses 35mm
- user says “I like the expression, but the perspective is ordinary”

Correct learning:

```text
expression +1
35mm no update
```

Incorrect learning:

```text
expression +1
35mm +1
composition +1
lighting +1
```

Only learn dimensions that the feedback actually supports.

## When user says only “喜欢这张”

If the user gives a global approval without specifying why, first identify the 2–4 most visually causal photographic decisions from the generated plan or Reference DNA.

Record only those high-confidence dimensions. Do not award every element in the image.

Example:

```text
strong evidence:
- camera position: 从门框后方拍
- composition: 人物放在极侧边
- lighting: 窗边高反差自然光

weak / incidental:
- wardrobe
- exact foreground object
```

Prefer updating the strong dimensions.

## When user says “不喜欢”

Do not assume every selected variable is bad.

If the user identifies the cause, update that dimension only.

If the cause is unclear, treat the global result as diagnostic evidence, not as permission to punish all variables. The next generation should vary the most likely failure dimensions first.

## Taste versus Reference DNA

Reference DNA answers:

> Why does this specific reference photo work?

Personal Taste answers:

> Across many accepted and rejected results, what photographic decisions does this user repeatedly prefer?

They can work together:

```text
reference image
→ extract DNA
→ generate transfer variants
→ user selects preferred results
→ update Personal Taste
→ future transfers become more personally aligned
```

## CLI workflow

Start with the neutral example:

```bash
cp examples/siran_taste.json taste_profile.json
```

Record explicit feedback:

```bash
python scripts/update_taste.py taste_profile.json \
  --like lenses=35mm \
  --strong-like compositions=人物放在极侧边 \
  --dislike imperfections=轻微数码噪点
```

Generate with learned taste:

```bash
python scripts/generate.py "一位短发中国女性" \
  --intent "广州盛夏生活感" \
  --taste-profile taste_profile.json \
  --count 6 \
  --seed 42
```

## Feedback JSON

For programmatic workflows, create:

```json
{
  "rating": 2,
  "dimensions": {
    "lenses": ["35mm"],
    "camera_positions": ["从门框后方拍"],
    "compositions": ["人物放在极侧边"]
  },
  "note": "喜欢观察距离和人物偏位，不是因为服装"
}
```

Then run:

```bash
python scripts/update_taste.py taste_profile.json --feedback feedback.json
```

## Exploration rule

Negative taste never equals a permanent ban unless the user explicitly creates a hard constraint.

The generator keeps a small probability for low-scored choices because personal taste can be context dependent. A lens disliked in a tight indoor portrait may still work in another subject or scene.

## Quality gate

Before using personal taste, verify:

1. the taste signal came from explicit or strongly inferable feedback;
2. it does not conflict with current hard anchors;
3. it does not break scene/lens/light compatibility;
4. it does not make a batch repetitive;
5. it still leaves meaningful exploration space;
6. sample count and evidence are sufficient before calling something a stable personal preference.

Do not describe a preference as stable based on one or two isolated examples.
