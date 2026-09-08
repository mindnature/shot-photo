# Shot Photo

面向 GPT Image 的 AI 摄影导演 Skill。

当前版本：`v0.5 Random Discovery`。

Shot Photo 不是摄影 Prompt 词库。它同时做两件事：

1. 帮不会摄影的人自动完成焦段、机位、构图、光线和瞬间设计；
2. 保留并强化随机探索能力，让同一个简单需求产生真正不同的摄影方案。

核心原则：

> 不用规则替代随机，而是让随机也懂摄影。

## 小白最快上手

安装后直接说：

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异大一点。
```

你不需要指定 35mm、低机位、构图、光线或 Photographer Profile。

Shot Photo 会自动决定这些摄影变量。

## 四种常用方式

### 1. 普通拍

```text
使用 $shot-photo。
一个短发中国女生，广州盛夏，生活感，生成 6 张。
```

系统会保持相对统一的摄影方向，同时拉开镜头差异。

### 2. 随机拍

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异尽量大。
```

Random Discovery 会主动随机：

- Photographer Profile
- 场景子区域
- 动作
- 表情
- 服装
- 景别
- 焦段
- 机位
- 构图
- 前景
- 光线
- 色彩
- 摄影缺陷

“校园”这种宽泛场景还会自动展开成图书馆、教学楼、操场、食堂、自行车棚、楼梯、空教室、便利店、树荫路等不同子场景。

如果想更随机：

```text
越随机越好，什么摄影风格都试，给我惊喜。
```

### 3. 参考图拍

上传参考图后说：

```text
使用 $shot-photo。
学这张图的拍法，不复制人物和衣服。
换成广州夏天，生成 6 张。
```

系统会提取 Reference DNA，而不是只描述图片内容。

小白只需要理解三句话：

```text
学拍法
学感觉
尽量复刻
```

### 4. 拍一整套

```text
使用 $shot-photo。
做一套 9 张校园写真。
同一个人物、同一套衣服、同一个下午，像一次真实拍摄。
```

这时进入 Series Director，而不是 Random Discovery。

## Random Discovery 为什么和原来的随机不同

Random Discovery 不是把所有变量独立抽签。

正确流程：

```text
随机场景
→ 随机一个与场景兼容的焦段
→ 随机兼容景别
→ 随机合理机位
→ 随机构图
→ 随机真实前景
→ 随机可解释光线
```

所以它保留“下一张不知道会是什么”的惊喜，同时避免明显不合理的摄影组合。

Random 模式还会检查整个批次，而不是只检查相邻两张，减少“8 张看起来其实是一张图换动作”的问题。

详细规则：`references/random_discovery.md`

实际示例：`examples/RANDOM.md`

## 随机强度

普通用户不用记内部参数，直接用自然语言即可：

```text
随机一点
```

整体气质相对稳定，但镜头变化更大。

```text
随机拍几张 / 差异大一点 / 给我惊喜
```

默认强随机，每张可以切换 Photographer Profile。

```text
放飞一点 / 越随机越好 / 什么风格都试
```

进入高随机探索，尽量减少历史偏好带来的收敛。

## Random 与 Personal Taste

Personal Taste 不应该变成审美信息茧房。

因此：

```text
普通生成：Taste 正常参与
Random strong：探索优先，Taste 默认关闭或弱参与
Random wild：Taste 基本退出
```

只有用户明确说“随机，但参考我的偏好”时，随机模式才弱加载 Personal Taste。

## Random 与 Series 的区别

```text
随机拍几张
→ 每张可以完全不同
→ Random Discovery
```

```text
拍一套 / 九宫格 / 同一次写真
→ 人物、服装、时间、地点连续
→ Series Director
```

如果用户说“拍一套，但镜头随机一点”，Series Continuity 仍然保留，只随机镜头层。

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
│   ├── random_discovery.md
│   ├── random_scene_expansions.json
│   ├── reference_dna.md
│   ├── reference_dna_schema.json
│   ├── personal_taste.md
│   ├── taste_profile.schema.json
│   ├── series_director.md
│   └── series_recipes.json
├── scripts/
│   ├── generate.py
│   ├── generate_random.py
│   ├── generate_series.py
│   └── update_taste.py
└── examples/
    ├── USAGE.md
    ├── RANDOM.md
    ├── REFERENCE_DNA.md
    ├── SERIES.md
    └── siran_taste.json
```

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/
```

## CLI：强随机

```bash
python scripts/generate_random.py "一个大学生，素颜" \
  --scene 校园 \
  --count 8 \
  --strength strong \
  --seed 42
```

## CLI：放飞随机

```bash
python scripts/generate_random.py "一个年轻女生" \
  --scene 城市街头 \
  --count 10 \
  --strength wild \
  --seed 42
```

## CLI：固定一部分再随机

```bash
python scripts/generate_random.py "一个短发中国女生" \
  --scene 广州 \
  --lens 35mm \
  --count 8 \
  --strength strong \
  --seed 42
```

## Reference DNA

参考图分析规则：`references/reference_dna.md`

三种内部模式：

1. `structure_transfer`
2. `mood_transfer`
3. `close_rebuild`

## Personal Taste

初始档案：

```bash
cp examples/siran_taste.json taste_profile.json
```

反馈更新：

```bash
python scripts/update_taste.py taste_profile.json \
  --like lenses=35mm \
  --strong-like compositions=人物放在极侧边 \
  --dislike imperfections=轻微数码噪点
```

详细规则：`references/personal_taste.md`

## Series Director

6 张默认节奏：

```text
建立空间
→ 进入人物
→ 动作发生
→ 靠近情绪
→ 重新拉开
→ 离场收束
```

可复现规划：

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州盛夏生活感" \
  --series-mode single-location \
  --seed 42
```

详细规则：`references/series_director.md`

## 版本演进

### v0.1 Photography Director

建立 Anchor Budget、Conditional Photography、Moment First、Batch Diversity 和 GPT Image Prompt。

### v0.2 Reference DNA

加入参考图摄影 DNA、三种迁移模式、No Fake EXIF。

### v0.3 Personal Taste

加入喜欢 / 不喜欢反馈和个人审美概率权重。

### v0.4 Series Director

加入 6 / 9 张连续组照、地点与时间连续性、镜头节奏。

### v0.5 Random Discovery

恢复并强化最初 VibeShot 式随机探索：跨 Photographer Profile、宽泛场景自动展开、全批次强去重、Taste 去收敛，以及 strong / wild 两级高随机。

当前目标：

> 普通模式像摄影师，系列模式像一次真实拍摄，随机模式像一台懂摄影的创意老虎机。