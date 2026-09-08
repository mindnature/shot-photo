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
→ 批次镜头设计
→ GPT Image Prompt
→ Quality Gate
```

当前版本：`v0.3 Personal Taste`。

## 核心能力

- 主要服务 GPT Image，使用完整自然语言而不是参数堆砌
- 先判断摄影逻辑，再选择焦段、机位、构图、前景、光线和瞬间
- 同批作品保持统一审美，但主动拉开镜头差异
- 支持 Reference Photo DNA：学参考图“为什么成立”，不是机械复制内容
- 支持 Personal Taste：把明确的喜欢 / 不喜欢逐步转成摄影选择权重
- 个人偏好只改变概率，不覆盖当前 Hard Anchor，也不破坏摄影合理性

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
│   └── taste_profile.schema.json
├── scripts/
│   ├── generate.py
│   └── update_taste.py
└── examples/
    ├── USAGE.md
    ├── REFERENCE_DNA.md
    └── siran_taste.json
```

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/
```

调用：

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

v0.3 开始，Shot Photo 可以逐步形成个人 Photographer Profile。

初始档案是中性的：

```bash
cp examples/siran_taste.json taste_profile.json
```

不要预设用户喜欢什么。只有用户明确反馈，或者多张被明确选中的作品出现稳定共同 DNA，才进入个人偏好。

### 记录反馈

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

每项保存：

```json
{
  "score": 1.75,
  "evidence": 3,
  "last_feedback": "2026-09-08T13:30:00+00:00"
}
```

`score` 范围 `-3 ~ +3`。`evidence` 越多，偏好对后续生成影响越稳定。

### 带个人偏好生成

```bash
python scripts/generate.py "一位短发中国女性" \
  --intent "广州盛夏生活感" \
  --taste-profile taste_profile.json \
  --count 6 \
  --seed 42
```

Personal Taste 会影响：

- Photographer Profile
- scene
- moment
- expression
- wardrobe
- shot size
- lens
- camera position
- composition
- foreground
- lighting
- palette
- controlled imperfection

但不会把低分项永久禁止，系统仍保留少量探索概率。

### 正确回灌方式

如果用户说：

```text
第2张喜欢，主要喜欢人物偏在边缘、从门框后观察和窗光。
第4张不喜欢直闪。
```

应该只更新：

```text
composition +
camera position +
lighting(window) +
lighting(direct flash) -
```

不要自动奖励第2张的服装、表情、焦段、场景，也不要自动惩罚第4张所有变量。

如果用户只说“喜欢这张”，先找 2–4 个最有因果可能的摄影决策，再回灌；不要整图全加分。

详细规则见 `references/personal_taste.md`。

## 为什么 Personal Taste 不直接锁死风格

个人审美通常是条件性的。一个人在室内不喜欢 85mm，不代表海边远距离观察也不喜欢 85mm。

因此 Shot Photo 使用：

```text
基础摄影人格
× 摄影兼容性
× Personal Taste 概率权重
× Diversity Gate
```

而不是简单的黑名单/白名单。

## 版本演进

### v0.1 Photography Director

建立 Anchor Budget、Conditional Photography、Moment First、Batch Diversity、GPT Image Native Prompt 和 Quality Gate。

### v0.2 Reference DNA

加入参考图摄影 DNA、三种迁移模式、多图共同 DNA、No Fake EXIF 与 Reference Anchor Budget。

### v0.3 Personal Taste

加入个人审美 Schema、反馈更新器、偏好证据计数、低证据阻尼、概率权重生成，以及 Reference DNA → 结果反馈 → Personal Taste 的闭环。

下一阶段适合继续做：系列拍摄连续性、同一人物身份一致性，以及从一批历史精选图自动蒸馏 `Siran Photographer Profile`。
