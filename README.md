# Shot Photo

不会摄影，也能让 AI 像摄影师一样拍。

Shot Photo 是一个面向 GPT Image / Images 2.5 的 AI 摄影 Skill。你不需要懂焦段、机位、构图、布光，也不需要自己拼一长串 Prompt。

你只需要说清楚：**想拍谁、在哪里、什么感觉。**

剩下的场景、动作、观察距离、机位、构图、光线和随机探索，由 Shot Photo 自动完成。

> 核心原则：不用规则替代随机，而是让随机也懂摄影。

> v0.8 新原则：同一个人、同一次拍摄，但每一张都要有新的摄影发现。

当前摄影引擎：`v0.8 Series Entropy / Controlled Chaos`。

---

## 30 秒开始

安装后，在支持 Skills 的环境里直接输入：

```text
$shot-photo
中国大学生，校园。
随机生成 8 张照片，差异尽量大，给我惊喜。
```

或者拍同一个人的九宫格：

```text
$shot-photo
一个女生，广州夏天街头。
做一套 9 宫格，同一个人、同一套衣服，像同一次真实拍摄。
但每张照片的机位、动作和构图要有变化，增加随机性，给我惊喜。
```

第一次使用：看 [`QUICKSTART.md`](./QUICKSTART.md)

更多可直接复制的例子：看 [`examples/BEGINNER_EXAMPLES.md`](./examples/BEGINNER_EXAMPLES.md)

---

## 为什么做 Shot Photo

很多 AI 写真已经能把人画得很好看，但连续看几张，经常会发现：

- 同一个正面机位；
- 同一种人物距离；
- 同一种“看向侧面 + 轻微微笑”；
- 同一种“手抓包带”；
- 背景换了，照片却还是像同一张；
- 旅行写真每张都像旅游宣传片；
- 招牌文字太完整，反而暴露 AI 味。

Shot Photo 解决的不是“再加几个摄影词”，而是让 AI 在生成前先做摄影决策。

它会考虑：

```text
为什么在这一秒按快门？
摄影师站在哪里？
人物是否意识到镜头？
这个空间适合什么距离和机位？
这一张和上一张为什么必须不一样？
哪些东西应该连续，哪些东西应该主动变化？
```

---

## 四种最常用玩法

### 1. 随机拍｜Random Discovery

适合找灵感、开盲盒、一次看很多不同拍法。

```text
$shot-photo
校园学生。
生成 10 张，越随机越好，什么拍法都试。
```

随机的不只是动作，还包括：

```text
摄影风格
场景子区域
观察关系
人物距离
景别
焦段
机位
构图
前景
光线
色彩
```

比如“校园”会自动展开成图书馆、教学楼、食堂、操场、自行车棚、空教室、便利店、宿舍楼下等不同子场景，而不是 8 张都站在同一条树荫路上。

### 2. 普通拍｜Standard Director

已经知道大概想拍什么，只让 Shot Photo 帮你把摄影细节补完整。

```text
$shot-photo
一个短发中国女生，广州盛夏街头。
自然、克制、有生活感，生成 6 张。
```

### 3. 参考图拍｜Reference DNA

上传一张你喜欢的照片后，可以直接说：

```text
$shot-photo
学这张图的感觉。
不要照搬人物和具体场景，随机生成 6 张。
```

Shot Photo 会优先学习人物占比、摄影距离、观察关系、空间层次、光线和瞬间状态，而不是机械照抄画面物件。

### 4. 拍一整套｜Series Director + Series Entropy

适合九宫格、旅行写真、人物组图。

```text
$shot-photo
参考图里的女生，丽江古城。
同一个人、同一套衣服，做一套 9 张。
像同一次真实拍摄，但每张机位、动作、人物占比和构图都要不同。
主打真实，不要旅游宣传片感，不要满屏清晰招牌。
```

v0.8 会锁住：

```text
人物身份
核心发型
服装
地点世界
时间窗口
主色彩世界
```

但主动改变：

```text
景别
机位
动作状态
Observation Relationship
人物占比
构图
前景遮挡
反射
轻微摄影缺陷
```

这就是 `Series Entropy`。

---

## v0.8：为什么系列照片不再“九张像一张”

以前连续组照容易为了稳定而过度收敛。人物确实统一了，但动作、角度和构图也一起被锁住。

v0.8 给九宫格增加了最低差异配额。默认至少包含：

- 3 种不同景别；
- 4 种不同机位；
- 4 种不同动作状态；
- 4 种不同构图；
- 5 种不同摄影师—人物观察关系；
- 2 张前景遮挡 / 玻璃反射 / 人群干扰；
- 1 张人物小比例大环境；
- 1 张背影 / 半背影；
- 1 张轻微真实摄影不完美。

一套照片可以同时出现：

```text
朋友边走边拍
远处观察
低机位动态
从背后跟拍
隔玻璃拍
人群缝隙抓拍
近距离情绪
人物很小的环境照
离场背影
```

身份连续，但摄影关系不重复。

---

## v0.8：压低“AI 旅游宣传片感”

古城、老街、旅行类生成最容易出现一个问题：每张都同时塞入“地点名 + 鲜花 + 灯笼 + 水渠 + 山景 + 完整招牌 + 完美阳光”。

看起来漂亮，但不像朋友真实拍的一套照片。

Shot Photo 现在默认：

- 不让每张都承担“证明地点”的任务；
- 普通墙、转角、阴影、半截店门、路人、栏杆也可以入镜；
- 只有少数建立空间的镜头需要明显地标；
- 背景招牌优先局部、模糊、被遮挡或裁切；
- 不主动生成大段完整旅游宣传文字。

地点应该由空间关系让人相信，而不是靠九张图都写着“丽江古城”。

---

## 安装

### macOS / Linux

```bash
git clone https://github.com/mindnature/shot-photo.git
mkdir -p ~/.codex/skills
cp -R shot-photo ~/.codex/skills/shot-photo
```

### Windows PowerShell

```powershell
git clone https://github.com/mindnature/shot-photo.git
New-Item -ItemType Directory -Force "$HOME\.codex\skills" | Out-Null
Copy-Item -Recurse -Force ".\shot-photo" "$HOME\.codex\skills\shot-photo"
```

安装完成后，重新打开或刷新支持 Skills 的 Codex / Agent 环境，然后输入：

```text
$shot-photo
```

> `$shot-photo` 不是任意聊天窗口里的通用魔法词。只有当前环境已经安装并支持这个 Skill 时，它才会读取仓库里的规则。

完整安装与排错：[`QUICKSTART.md`](./QUICKSTART.md)

---

## 小白万能公式

```text
$shot-photo
拍谁：...
在哪里：...
什么感觉：...
要几张：...
额外要求：...
```

例如：

```text
$shot-photo
拍谁：一对 30 多岁的夫妻
在哪里：周末菜市场
什么感觉：生活感，不要写真感
要几张：6 张
额外要求：像两个人真的在买菜，不要为了拍照摆动作。
```

或者：

```text
$shot-photo
我完全不会摄影。
一个女生，海边旅行，生成 6 张。
不要一直看镜头，不要摆拍，其他你决定。
```

---

## 不满意，不用重写 Prompt

第一轮出图后直接说人话：

```text
太摆拍了，重来，自然一点。
```

```text
人物太大，环境多一点。
```

```text
保留这个光，但换完全不同的机位。
```

```text
九张还是太像，把 Series Entropy 再提高一级。
```

```text
背景太像旅游宣传片，减少招牌和景点元素。
```

```text
第 3 张最好，保留这种摄影关系，但不要复制构图。
```

---

## 高级用户

内部规则：

- 随机探索：[`references/random_discovery.md`](./references/random_discovery.md)
- Images 2.5 Prompt：[`references/gpt_image_prompting.md`](./references/gpt_image_prompting.md)
- 参考图 DNA：[`references/reference_dna.md`](./references/reference_dna.md)
- Personal Taste：[`references/personal_taste.md`](./references/personal_taste.md)
- Series Director：[`references/series_director.md`](./references/series_director.md)
- Series Entropy：[`references/series_entropy.md`](./references/series_entropy.md)
- Series Entropy 配额：[`references/series_entropy_rules.json`](./references/series_entropy_rules.json)
- 质量门：[`references/quality_gate.md`](./references/quality_gate.md)

随机 CLI：

```bash
python scripts/generate_random.py "一个大学生，素颜" \
  --scene 校园 \
  --count 8 \
  --strength strong \
  --seed 42
```

系列 CLI：

```bash
python scripts/generate_series.py "一个女生" \
  --scene 旧城区市场 \
  --count 9 \
  --entropy-strength strong \
  --series-mode single-location \
  --seed 42 \
  --format json
```

如果用户明确要系列更放飞：

```bash
python scripts/generate_series.py "一个女生" \
  --scene 旧城区市场 \
  --count 9 \
  --entropy-strength wild \
  --seed 42
```

默认会抑制背景可读文字；只有确实需要清晰招牌时才加：

```text
--allow-readable-text
```

---

## 项目结构

```text
shot-photo/
├── SKILL.md
├── README.md
├── QUICKSTART.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── references/
│   ├── series_director.md
│   ├── series_entropy.md
│   ├── series_entropy_rules.json
│   └── ...
├── scripts/
│   ├── generate.py
│   ├── generate_random.py
│   ├── generate_series.py
│   └── update_taste.py
└── examples/
```

---

## 版本演进

- `v0.1` Photography Director：摄影逻辑、Moment First、质量门。
- `v0.2` Reference DNA：参考图摄影关系迁移。
- `v0.3` Personal Taste：喜欢 / 不喜欢的概率偏好。
- `v0.4` Series Director：连续组照与镜头节奏。
- `v0.5` Random Discovery：恢复并强化老虎机式随机探索。
- `v0.6` Images 2.5 Random Director：Prompt 压缩、Observation Relationship、更强随机传递。
- `v0.7` Beginner Frontend：README、Quickstart、小白示例。
- `v0.8` Series Entropy / Controlled Chaos：身份稳定 + 摄影层高熵；增加组照差异配额、Anti-Tourism-Poster 与 Background Text Suppression。

当前产品方向：

> **小白只负责说“想拍什么”，Shot Photo 负责像摄影师一样把剩下的事情做完。**

---

## License

Shot Photo 使用 [MIT License](./LICENSE) 开源。

你可以自由使用、修改、分发和商用本项目；在复制或分发本项目或其主要部分时，请保留原始版权与 MIT License 声明。
