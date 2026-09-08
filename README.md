# Shot Photo

面向 GPT Image 的个人 AI 摄影导演 Skill。

Shot Photo 不是简单的“摄影 Prompt 随机生成器”。它把摄影创作拆成：意图理解 → 风格人格 → 硬/软锚点 → 摄影变量选择 → 兼容性检查 → 批次差异控制 → GPT Image 提示词合成 → 质量门检查。

## 核心目标

- 主要服务 GPT Image，而不是同时兼容所有生图模型
- 用少量关键锚点控制画面，把细枝末节留给模型发挥
- 生成“有边界的随机”，避免机械抽签式变量堆砌
- 同一批作品保持统一摄影审美，但镜头、动作、构图、场景有明显差异
- 强调真实摄影逻辑、生活瞬间、空间层次、自然光线与克制后期
- 长期把个人喜欢的摄影语言沉淀为可复用风格资产

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
│   └── quality_gate.md
├── scripts/
│   └── generate.py
└── examples/
    └── USAGE.md
```

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/
```

安装后可在新的 Codex 对话中调用：

```text
使用 $shot-photo，生成 6 组夏日生活感人像摄影方案，9:16。
```

也可以锁定部分条件：

```text
使用 $shot-photo，主体为短发中国女性，广州雨后街头，35mm，都市疏离感，生成 5 组，其余由摄影导演决定。
```

或只给一个模糊意图：

```text
使用 $shot-photo，把“一个人在盛夏午后短暂发呆”拍成 6 组真实摄影提示词。
```

## v0.1 设计原则

1. **Anchor Budget**：硬锚点原则上不超过 4 个，软锚点不超过 5 个，至少保留 3 个自由变量。
2. **Conditional Selection**：变量不是独立随机；焦段、景别、机位、光线、前景和场景之间必须兼容。
3. **Style First**：先确定摄影风格人格，再从相应变量分布中选择，而不是所有元素放进同一个大池。
4. **Moment First**：优先拍动作正在发生的瞬间，而不是动作完成后的标准摆拍。
5. **Controlled Imperfection**：允许自然遮挡、轻微失焦、运动模糊、过曝、反射和颗粒，但不能为了“瑕疵感”破坏主体。
6. **GPT Image Native**：使用完整自然语言和明确视觉关系，不堆砌模型参数，不把 Prompt 写成标签垃圾桶。

## 当前版本

v0.1：建立摄影导演核心框架、10 个摄影风格人格、基础变量库、兼容性规则、GPT Image 专用 Prompt 规范与质量门。

后续计划包括：个人审美反馈权重、参考图反推摄影语言、系列拍摄连续性、人物身份一致性与照片评分回灌。