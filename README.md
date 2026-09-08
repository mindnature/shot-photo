# Shot Photo

面向 GPT Image 的个人 AI 摄影导演 Skill。

Shot Photo 不是简单的“摄影 Prompt 随机生成器”。它把摄影创作拆成：意图理解 → 风格人格 → 硬/软锚点 → 摄影变量选择 → 兼容性检查 → 批次差异控制 → GPT Image 提示词合成 → 质量门检查。

v0.2 开始加入 Reference Photo DNA：参考图不再只是“描述后改写”，而是先提取摄影结构，再迁移到新主体、新场景或新的系列作品。

## 核心目标

- 主要服务 GPT Image，而不是同时兼容所有生图模型
- 用少量关键锚点控制画面，把细枝末节留给模型发挥
- 生成“有边界的随机”，避免机械抽签式变量堆砌
- 同一批作品保持统一摄影审美，但镜头、动作、构图、场景有明显差异
- 强调真实摄影逻辑、生活瞬间、空间层次、自然光线与克制后期
- 从参考照片中提取可迁移的摄影 DNA，而不是机械复制画面内容
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
│   ├── quality_gate.md
│   ├── reference_dna.md
│   └── reference_dna_schema.json
├── scripts/
│   └── generate.py
└── examples/
    ├── USAGE.md
    └── REFERENCE_DNA.md
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

## 参考图模式

上传一张参考图后，可以直接说：

```text
使用 $shot-photo，参考这张图的拍法，不复制人物和服装。换成广州盛夏街头的一位短发中国女生，9:16，给我 4 组。
```

Shot Photo 会优先提取：

- 主体占比
- 摄影距离
- 可能焦段区间
- 机位高度
- 摄影师与主体的观察关系
- 构图重心
- 前景 / 中景 / 背景层次
- 光线方向、软硬和光比
- 主要色块
- 动作处于哪个瞬间
- 真实感来自哪里
- 情绪是如何被摄影关系制造出来的

然后选择三种迁移模式之一：

1. `structure_transfer`：学拍法，换内容。默认推荐。
2. `mood_transfer`：只迁移情绪机制、光线、距离和色块，不照搬构图。
3. `close_rebuild`：用户明确要求时，尽量保留构图、机位、光线和主要画面关系。

详细规则见 `references/reference_dna.md`。

## v0.1 设计原则

1. **Anchor Budget**：硬锚点原则上不超过 4 个，软锚点不超过 5 个，至少保留 3 个自由变量。
2. **Conditional Selection**：变量不是独立随机；焦段、景别、机位、光线、前景和场景之间必须兼容。
3. **Style First**：先确定摄影风格人格，再从相应变量分布中选择，而不是所有元素放进同一个大池。
4. **Moment First**：优先拍动作正在发生的瞬间，而不是动作完成后的标准摆拍。
5. **Controlled Imperfection**：允许自然遮挡、轻微失焦、运动模糊、过曝、反射和颗粒，但不能为了“瑕疵感”破坏主体。
6. **GPT Image Native**：使用完整自然语言和明确视觉关系，不堆砌模型参数，不把 Prompt 写成标签垃圾桶。

## v0.2 Reference DNA

v0.2 新增四个原则：

1. **Structure Before Content**：先判断参考图为什么成立，再看人物穿了什么、站在哪里。
2. **No Fake EXIF**：没有真实 EXIF 时，只估计焦段区间与摄影距离，不伪造光圈、快门、ISO。
3. **Transfer, Not Collage**：迁移摄影关系，而不是把参考图的服装、动作、场景、光线全部堆到新图里。
4. **Reference Anchor Budget**：参考图只锁定最重要的 3–5 个结构锚点，保留新画面的自由度。

## 当前版本

v0.2：在 v0.1 的摄影导演核心框架之上，加入 Reference Photo DNA、三种参考图迁移模式、多参考图共同 DNA 提取与参考图质量门。

下一阶段计划：个人审美反馈权重、系列拍摄连续性、人物身份一致性，以及“喜欢 / 不喜欢”结果回灌形成个人 Photographer Profile。
