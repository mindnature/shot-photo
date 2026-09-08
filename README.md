# Shot Photo

面向 GPT Image 的个人 AI 摄影导演 Skill。

Shot Photo 不把摄影当成 Prompt 词库，而是把创作拆成：

```text
意图理解
→ Hard / Soft Anchors
→ Photographer Profile
→ Reference DNA（如有）
→ Personal Taste（如有）
→ 摄影兼容性
→ Series Director / Batch Diversity
→ GPT Image Prompt
→ Quality Gate
```

当前版本：`v0.4 Series Director`。

## 核心能力

- 主要服务 GPT Image，使用完整自然语言而不是参数堆砌
- 先判断摄影逻辑，再选择焦段、机位、构图、前景、光线和瞬间
- 支持 Reference Photo DNA：学参考图“为什么成立”，不是机械复制内容
- 支持 Personal Taste：把明确的喜欢 / 不喜欢逐步转成摄影选择权重
- 支持 Series Director：把 6–9 张图片组织成同一次拍摄中的连续组照，而不是随机拼盘
- 系列模式默认控制同一人物、同一服装世界、有限场景、统一色彩与镜头节奏

## 目录

```text
shot-photo/
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── photographer_profiles.json
│   ├── variables.json
│   ├── compatibility.json
│   ├── gpt_image_prompting.md
│   ├── quality_gate.md
│   ├── reference_dna.md
│   ├── reference_dna_schema.json
│   ├── personal_taste.md
│   ├── taste_profile.schema.json
│   ├── series_director.md
│   └── series_recipes.json
├── scripts/
│   ├── generate.py
│   ├── generate_series.py
│   └── update_taste.py
└── examples/
    ├── USAGE.md
    ├── REFERENCE_DNA.md
    ├── SERIES.md
    └── siran_taste.json
```

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/
```

普通调用：

```text
使用 $shot-photo，一个短发中国女生，广州盛夏，生活感，9:16，生成 6 组。
```

## Reference DNA

上传参考图后可以说：

```text
使用 $shot-photo，学这张图的拍法，不复制人物和服装。
换成广州盛夏街头的一位短发中国女生，9:16，生成 4 组。
```

Shot Photo 会提取主体占比、摄影距离、可能焦段、机位高度、摄影师与主体关系、构图重心、空间层次、光线结构、主色块、动作阶段、真实感来源和情绪机制。

三种模式：

1. `structure_transfer`：学拍法，换内容。默认推荐。
2. `mood_transfer`：只迁移情绪机制、光线、距离和色块。
3. `close_rebuild`：明确要求复刻时，尽量保留构图、机位、光线和主要关系。

详细规则见 `references/reference_dna.md`。

## Personal Taste

初始档案保持中性：

```bash
cp examples/siran_taste.json taste_profile.json
```

记录反馈：

```bash
python scripts/update_taste.py taste_profile.json \
  --like lenses=35mm \
  --strong-like compositions=人物放在极侧边 \
  --like camera_positions=从门框后方拍 \
  --dislike imperfections=轻微数码噪点
```

支持四级反馈：

```text
strong-like      +2
like             +1
dislike          -1
strong-dislike   -2
```

每项保存 `score (-3~+3)`、`evidence` 和 `last_feedback`。单次评价不会永久锁死风格，重复证据才逐渐提高影响。

带个人偏好生成：

```bash
python scripts/generate.py "一位短发中国女性" \
  --intent "广州盛夏生活感" \
  --taste-profile taste_profile.json \
  --count 6 \
  --seed 42
```

如果用户只说“喜欢这张”，不要把整张图所有变量全部奖励；先找 2–4 个最可能造成喜欢的摄影决策再回灌。

详细规则见 `references/personal_taste.md`。

## Series Director

v0.4 新增真正的组照导演层。

用户说：

```text
做一套 6 张连续组照。
同一个短发中国女生，广州盛夏，同一套衣服，同一地点同一时间段。
不要 6 张独立好图，要有开场、靠近、动作、停顿和离场。
```

系统默认设计：

```text
01 建立空间
02 进入人物
03 动作发生
04 靠近情绪
05 重新拉开
06 离场收束
```

九张组照则使用：

```text
01 建立空间
02 人物进入
03 第一次动作
04 情绪近景
05 细节停顿
06 空间过渡
07 第二次动作
08 情绪回落
09 离场结尾
```

Series Director 默认锁定：

- 同一人物身份
- 同一发型、年龄感、体型比例
- 同一服装，或最多一次合理换装
- 同一 Photographer Profile
- 同一主色彩世界
- 一个主地点，或 2–3 个可自然衔接的地点
- 同一时间段，或自然渐进的 Time Arc

### CLI：单地点 6 张

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州盛夏生活感" \
  --series-mode single-location \
  --time-arc static \
  --seed 42
```

### CLI：9 张 micro-journey

```bash
python scripts/generate_series.py "一位中国女性" \
  --count 9 \
  --profile 雨夜电影 \
  --intent "雨后城市短途步行" \
  --series-mode micro-journey \
  --time-arc progressive \
  --seed 42
```

### 带 Personal Taste 的系列

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州夏日街头" \
  --taste-profile taste_profile.json \
  --series-mode single-location \
  --seed 42
```

Series Director 会保留个人偏好，但不会让偏好把所有照片压成同一个焦段、同一种构图。

详细规则见 `references/series_director.md`，调用案例见 `examples/SERIES.md`。

## 为什么 Series Director 和 Batch Diversity 不一样

Batch Diversity 解决的是“不要重复”。

Series Director 解决的是：

```text
这一组为什么从这张开始？
为什么此时靠近人物？
什么时候需要动作？
什么时候重新拉远？
最后一张为什么像结束？
```

因此系列中的差异不是随机差异，而是叙事与观看节奏。

## 版本演进

### v0.1 Photography Director

建立 Anchor Budget、Conditional Photography、Moment First、Batch Diversity、GPT Image Native Prompt 和 Quality Gate。

### v0.2 Reference DNA

加入参考图摄影 DNA、三种迁移模式、多图共同 DNA、No Fake EXIF 与 Reference Anchor Budget。

### v0.3 Personal Taste

加入个人审美 Schema、反馈更新器、偏好证据计数、概率权重生成，以及 Reference DNA → 结果反馈 → Personal Taste 的闭环。

### v0.4 Series Director

加入连续组照规划、6/9 张镜头谱、Identity / Wardrobe / Palette Continuity、single-location / micro-journey、Time Arc 与系列质量门。

下一阶段适合继续做：更强的人物身份一致性、系列参考图 Character Sheet，以及从一批历史精选图自动蒸馏 `Siran Photographer Profile`。
