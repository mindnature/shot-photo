# Shot Photo

不会摄影，也能让 AI 像摄影师一样拍。

Shot Photo 是一个面向 GPT Image / Images 2.5 的 AI 摄影 Skill。你不需要懂焦段、机位、构图、布光，也不需要自己拼一长串 Prompt。

你只需要说清楚：**想拍谁、在哪里、什么感觉。**

剩下的场景、动作、观察距离、机位、构图、光线和随机探索，由 Shot Photo 自动完成。

> 核心原则：不用规则替代随机，而是让随机也懂摄影。

当前摄影引擎：`v0.6 Images 2.5 Random Director`。

---

## 30 秒看懂怎么用

安装后，在支持 Skills 的环境中直接输入：

```text
$shot-photo
大学生，校园。
随机生成 8 张照片，差异尽量大，给我惊喜。
```

不会写 Prompt 也没关系。下面三种用法已经覆盖大多数场景。

### 1. 不知道怎么拍：让它随机

```text
$shot-photo
一个女生，海边。
自然、松弛、有生活感。
随机生成 8 张，差异尽量大。
```

### 2. 看到喜欢的图：让它学这种感觉

上传参考图后：

```text
$shot-photo
参考这张照片的感觉。
不要照搬人物和具体场景，
随机生成 6 张类似摄影感的照片。
```

### 3. 想做九宫格：让它拍一整套

```text
$shot-photo
一个女生，广州夏天街头。
做一套 9 张连续写真，
同一个人、同一套衣服，像一次真实拍摄。
```

**第一次使用？直接看：[QUICKSTART.md](./QUICKSTART.md)**

**想复制更多现成指令？看：[examples/BEGINNER_EXAMPLES.md](./examples/BEGINNER_EXAMPLES.md)**

---

## 为什么做 Shot Photo

很多 AI 写真已经能把人物画得很好看，但连续生成几张后，经常出现另一个问题：

- 同一个正面机位；
- 同一种人物距离；
- 同一种“看镜头 + 摆姿势”；
- 换了背景，照片却还是像同一张；
- Prompt 越写越长，画面反而越来越模板化。

Shot Photo 解决的不是“再加几个摄影词”，而是让 AI 在生成前先做摄影决策。

它会考虑：

```text
为什么在这一秒按快门？
摄影师站在哪里？
人物是否意识到镜头？
这个空间适合什么距离和机位？
光从哪里来？
这一张和上一张为什么必须不一样？
```

所以它不是一个摄影 Prompt 词库，而更像一个藏在后台的 AI 摄影导演。

---

## 四种常用玩法

### 随机拍｜Random Discovery

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

### 普通拍｜Standard Director

适合已经知道自己想要什么，只希望 AI 帮你把摄影细节补完整。

```text
$shot-photo
一个短发中国女生，广州盛夏街头。
自然、克制、有生活感，生成 6 张。
```

### 参考图拍｜Reference DNA

适合“我说不清为什么喜欢，但我就想要这种感觉”。

小白只需要记三句话：

```text
学这张图的拍法
学这张图的感觉
尽量按这张图复刻
```

Shot Photo 会优先学习人物占比、摄影距离、观察关系、空间层次、光线和瞬间状态，而不是机械照抄参考图里的衣服和背景。

### 拍一整套｜Series Director

适合小红书九宫格、旅行写真、人物组图。

```text
$shot-photo
做一套 9 张校园写真。
同一个人物、同一套衣服、同一个下午，像一次真实拍摄。
```

这时系统会主动保持人物、服装和视觉世界连续，并设计远景、中景、近景和收尾镜头，而不是生成 9 张互不相关的照片。

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

> `$shot-photo` 不是任意聊天窗口里的通用魔法指令。只有当前环境已经安装并支持这个 Skill 时，它才会读取仓库里的 `SKILL.md` 和配套规则。

完整安装、更新和排错说明见：[QUICKSTART.md](./QUICKSTART.md)

---

## 小白万能公式

你完全可以不写任何摄影术语，只按下面格式说：

```text
$shot-photo
[人物]
[场景]
[感觉]
[数量 / 是否随机 / 是否同一个人]
```

例如：

```text
$shot-photo
一个男大学生，校园。
像朋友顺手拍到的一样。
随机生成 8 张，差异尽量大。
```

或者更短：

```text
$shot-photo
我不会摄影。
帮我拍一组夏天海边的松弛感照片，其他你决定。
```

---

## 不满意，不用重写 Prompt

第一轮出图后直接说人话即可：

```text
第 2 张最好，人物放在画面边上的感觉保留。
```

```text
太摆拍了，重来，自然一点。
```

```text
人物太大，我想让环境更多。
```

```text
保留这个光，但换一个完全不同的机位。
```

```text
这次不要同一个人，随机性再强一点。
```

Shot Photo 会把这些反馈翻译成摄影调整，而不是要求你重新学习专业术语。

---

## Shot Photo 在后台做了什么

小白不需要理解下面这些概念，但它们构成了 Shot Photo 的内部能力：

- `Random Discovery`：强随机摄影探索；
- `Conditional Photography`：避免焦段、场景、机位互相打架；
- `Moment First`：优先未完成动作，而不是标准摆拍；
- `Reference DNA`：学习参考图为什么成立；
- `Personal Taste`：把明确的喜欢 / 不喜欢变成概率偏好；
- `Series Director`：组织 6 / 9 张连续组照；
- `Images 2.5 Prompt Compression`：最终 Prompt 短、准、留有模型发挥空间。

随机模式尤其强调：

```text
随机场景
→ 选择兼容的摄影距离 / 焦段
→ 随机合理机位
→ 随机构图与观察关系
→ 随机真实光线
→ 全批次去重
```

因此它追求的是“强随机，但不乱”。

---

## 给高级用户

如果你希望控制、复现或二次开发，可以继续阅读：

- 随机探索规则：[`references/random_discovery.md`](./references/random_discovery.md)
- GPT Image / Images 2.5 提示规则：[`references/gpt_image_prompting.md`](./references/gpt_image_prompting.md)
- 参考图 DNA：[`references/reference_dna.md`](./references/reference_dna.md)
- Personal Taste：[`references/personal_taste.md`](./references/personal_taste.md)
- Series Director：[`references/series_director.md`](./references/series_director.md)
- 质量门：[`references/quality_gate.md`](./references/quality_gate.md)

CLI 示例：

```bash
python scripts/generate_random.py "一个大学生，素颜" \
  --scene 校园 \
  --count 8 \
  --strength strong \
  --seed 42
```

更激进的随机探索：

```bash
python scripts/generate_random.py "一个年轻女生" \
  --scene 城市街头 \
  --count 10 \
  --strength wild \
  --seed 42
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
├── scripts/
└── examples/
    ├── BEGINNER_EXAMPLES.md
    ├── RANDOM.md
    ├── REFERENCE_DNA.md
    ├── SERIES.md
    └── USAGE.md
```

---

## 版本演进

- `v0.1` Photography Director：建立摄影逻辑、Moment First 与质量门。
- `v0.2` Reference DNA：加入参考图摄影关系迁移。
- `v0.3` Personal Taste：加入喜欢 / 不喜欢的偏好权重。
- `v0.4` Series Director：加入连续组照与镜头节奏。
- `v0.5` Random Discovery：恢复并强化跨场景、跨机位、跨摄影人格的随机探索。
- `v0.6` Images 2.5 Random Director：缩短最终 Prompt、增加 Observation Relationship、强化随机差异传递。

当前产品方向：

> **小白只负责说“想拍什么”，Shot Photo 负责像摄影师一样把剩下的事情做完。**

---

## License

Shot Photo 使用 [MIT License](./LICENSE) 开源。

你可以自由使用、修改、分发和商用本项目；在复制或分发本项目或其主要部分时，请保留原始版权与 MIT License 声明。
