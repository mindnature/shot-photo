# Shot Photo

面向 GPT Image / Images 2.5 的 AI 摄影导演 Skill。

当前版本：`v0.6 Images 2.5 Random Director`。

Shot Photo 不是摄影 Prompt 词库。它同时解决四类问题：

1. 小白不会摄影，也能只用自然语言得到可用照片；
2. Random Discovery 保留并强化“下一张不知道会是什么”的探索感；
3. Reference DNA 能学参考图的摄影关系；
4. Series Director 能把多张照片组织成一次真实拍摄。

核心原则：

> 不用规则替代随机，而是让随机也懂摄影。

> Images 2.5 Prompt 要短、准、有空间：内部规划可以复杂，最终提示词不要把所有变量写满。

---

## 小白最快上手

安装后直接说：

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异大一点。
```

你不需要指定 35mm、低机位、构图、光线或 Photographer Profile。

Shot Photo 会自动决定摄影变量。

---

## v0.6 针对 Images 2.5 做了什么

### 1. Prompt 更短

以前随机规划虽然差异很大，但最终仍会把焦段、景别、机位、构图、前景、光线、色彩、缺陷全部写进同一套长模板，容易把随机重新收敛。

v0.6 改成：

```text
主体
+ 子场景
+ 一个进行中瞬间
+ 一个观察关系
+ 一个构图亮点
+ 一个光线亮点
+ 可选一个真实感线索
```

Random Strong / Wild 使用独立的短 Prompt 渲染器。

### 2. 随机层级上移

随机不只随机动作，而是随机整个“拍法世界”：

```text
Photographer Profile
→ Scene Cluster
→ Observation Relationship
→ Camera Language
→ Moment / Light / Composition
```

新增 Observation Relationship，例如：

- 同行同学顺手拍到；
- 中远距离观察；
- 路过者偶然记录；
- 人群边缘抓拍；
- 门框后观察；
- 隔着玻璃观察；
- 台阶下方低位观察；
- 楼梯 / 栏杆上方观察；
- 让人物经过镜头而不是停下来摆拍。

### 3. Random 不再默认人物连续

如果用户说：

```text
校园学生，随机 8 张
```

系统不会自动锁：

- 上一张的脸；
- 上一张的发型；
- 上一套服装；
- 上一个地点；
- 上一种色调。

只有用户明确要求“同一个人 / 同一套写真 / 连续组照”时才锁身份连续性。

### 4. Personal Taste 更弱

```text
Standard：Taste 正常参与
Random balanced：Taste 可参与
Random strong：Taste 默认关闭，明确要求时最多弱加载
Random wild：Taste 基本退出
```

避免用久以后随机模式又收敛到熟悉的 35mm、同一构图和同一种光线。

### 5. Anchor Budget 更开放

```text
Standard
Hard Anchors ≤ 4
Soft Anchors ≤ 4
Free Variables ≥ 4

Random Strong
Hard Anchors ≤ 3
Soft Anchors ≤ 3
Free Variables ≥ 6

Random Wild
Hard Anchors ≤ 2
Soft Anchors ≤ 2
Free Variables ≥ 8
```

---

## 四种最常用方式

### 1. 普通拍

```text
使用 $shot-photo。
一个短发中国女生，广州盛夏，生活感，生成 6 张。
```

系统保持相对统一的摄影方向，同时拉开镜头差异。

### 2. 随机拍

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异尽量大。
```

Random Discovery 会主动随机：

- Photographer Profile
- 场景子区域
- Observation Relationship
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

“校园”这种宽泛场景还会自动展开成图书馆、教学楼、操场、食堂、自行车棚、楼梯、空教室、便利店、树荫路、宿舍楼下、篮球场边、草坪等不同子场景。

更随机：

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

---

## Random Discovery 为什么不是“纯乱抽”

正确流程：

```text
随机场景
→ 在场景内选择兼容焦段
→ 随机兼容景别
→ 随机合理机位
→ 随机观察关系
→ 随机构图
→ 随机真实前景
→ 随机可解释光线
```

所以它保留“开盲盒”的惊喜，同时避免明显不合理的摄影组合。

Random 还会检查整个批次，而不是只检查相邻两张，减少“8 张其实是一张图换动作”的问题。

详细规则：`references/random_discovery.md`

实际示例：`examples/RANDOM.md`

---

## Random 强度

普通用户不用记内部参数。

```text
随机一点
```

对应 balanced：整体气质相对稳定，但镜头变化更大。

```text
随机拍几张 / 差异大一点 / 给我惊喜
```

对应 strong：每张可以切换 Photographer Profile、Scene Cluster 和 Observation Relationship。

```text
放飞一点 / 越随机越好 / 什么风格都试
```

对应 wild：最大化探索，减少历史偏好和连续性约束。

---

## Images 2.5 Prompt 规则

最终 Prompt 不再机械写满后台字段。

### Standard

通常保留：

```text
主体
场景
瞬间
观察关系
1 个构图亮点
1 个光线亮点
0–1 个真实感线索
```

### Random Strong

Prompt 更短，让 Images 2.5 保留更多发明空间。

### Random Wild

只锁用户 Hard Anchor + 一个鲜明子场景 + 一个观察关系 + 一个未完成动作 + 一个真实光线逻辑。

负面约束默认压缩成一句：

```text
避免影楼式精修、塑料皮肤、过度摆拍和无理由杂乱背景，保持真实可信的生活摄影感。
```

详细规则：`references/gpt_image_prompting.md`

---

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

---

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/
```

---

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

---

## Reference DNA

参考图分析规则：`references/reference_dna.md`

内部模式：

1. `structure_transfer`
2. `mood_transfer`
3. `close_rebuild`

---

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

---

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

---

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

恢复并强化 VibeShot 式随机探索：跨 Photographer Profile、宽泛场景自动展开、全批次强去重、Taste 去收敛。

### v0.6 Images 2.5 Random Director

针对 Images 2.5 重构 Prompt：缩短最终指令、减少穷尽式控制、增加 Observation Relationship、进一步弱化 Random Taste、Random Strong / Wild 使用独立 Prompt 渲染器，让随机差异真正传递到最终生图。

当前目标：

> Standard 要稳，Series 要连，Reference 要会学，Random 要敢变；Images 2.5 Prompt 要短、准、有空间。