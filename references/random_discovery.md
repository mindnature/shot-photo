# Random Discovery — Images 2.5

Random Discovery 是 Shot Photo 的探索模式。目标不是让每一张都服从同一个摄影人格，而是在摄影物理合理的前提下，主动制造大幅差异和意外组合。

核心原则：

> 不用规则替代随机，而是让随机也懂摄影。

> Random 的差异必须发生在“拍法世界”层，而不是只换动作、表情或背景。

---

## 1. 自动触发

用户出现以下表达时默认进入 `strong`：

- 随机拍几张
- 随便来几张
- 自由发挥
- 差异大一点
- 多试几种
- 给我惊喜
- 不知道拍什么，你决定
- 多来点不同的

以下表达进入 `wild`：

- 放飞一点
- 越随机越好
- 完全随机
- 脑洞大一点
- 不要收敛
- 什么风格都试试

用户说“随机一点”但仍希望整体气质稳定时，内部可使用 `balanced`。

前台不要要求小白学习 balanced / strong / wild 名称。

---

## 2. 三种强度

### balanced

- 保留一个主 Photographer Profile；
- 大幅随机场景、动作、景别、焦段、机位、构图、前景、光线；
- 可正常参考 Personal Taste；
- 适合“同一种感觉，多试几个镜头”。

### strong

- 每张允许切换 Photographer Profile；
- 优先使用不同 Scene Cluster；
- Observation Relationship 必须明显变化；
- 景别、焦段、机位、构图、光线均强随机；
- 不启用 Series Continuity；
- 不自动继承上一张人物身份、发型、服装、色调；
- Personal Taste 默认关闭；若用户明确要求参考偏好，则最多弱加载。

推荐概念比例：

```text
User Intent 40%
Random Exploration 45%
Personal Taste ≤ 15%
```

### wild

- 整批尽可能广覆盖 Photographer Profiles；
- 优先未使用过的场景、景别、焦段、机位、构图和光线；
- 人物造型也可变化，除非用户锁定；
- 不继承上一张身份；
- 允许更不常见但合理的观察距离、主体比例和构图；
- Personal Taste 基本去耦。

推荐概念比例：

```text
User Intent 35%
Random Exploration 60%
Personal Taste ≤ 5%
```

---

## 3. 随机层级上移

Random Discovery 至少作用于四层。

### Layer 1 — Photographer Profile

例如：

- 日常观察
- 建筑人像
- CCD 青春
- 纪实街拍
- 自然诗意
- 都市疏离
- 雨夜电影
- 旅行日记
- 东方盛夏
- 安静室内

Strong / Wild 不要求整批像同一个摄影师。

### Layer 2 — Scene Cluster

宽泛场景必须自动展开。

例如用户说：

```text
大学生，素颜，校园，随机 8 张
```

“校园”应展开为多个子场景：

```text
图书馆入口
教学楼走廊
操场看台
食堂窗口
自行车棚
楼梯转角
空教室窗边
校园便利店
树荫主路
宿舍楼下
篮球场边
草坪
```

不要把“校园”理解成“同一条树荫路”。

### Layer 3 — Observation Relationship

随机摄影师与主体的关系：

- 同学顺手拍到；
- 中远距离观察；
- 路过时偶然记录；
- 跟拍中回头；
- 从人群边缘拍；
- 从门框后拍；
- 隔着玻璃观察；
- 坐着时被记录；
- 人物经过镜头时被抓到；
- 从台阶下方或楼上栏杆处观察。

这比单纯换焦段更能改变照片。

### Layer 4 — Camera Language

主动打散：

- 近距离广角；
- 中距离自然透视；
- 远距离压缩；
- 小人物大环境；
- 近景 / 半身 / 全身 / 环境人像；
- 高 / 平 / 低机位；
- 静态停顿 / 行进中 / 动作被打断。

---

## 4. Random Anchor Budget

随机模式只锁用户真正指定的内容。

例如：

```text
一个大学生，素颜，校园，随机 8 张。
```

应锁定：

- 大学生；
- 素颜；
- 校园。

不应自动锁定：

- 同一张脸；
- 同一件白 T；
- 同一条牛仔裙；
- 同一时间；
- 同一色彩；
- 同一焦段；
- 同一摄影人格。

### Strong

- Hard Anchors ≤ 3
- Soft Anchors ≤ 3
- Free Variables ≥ 6

### Wild

- Hard Anchors ≤ 2
- Soft Anchors ≤ 2
- Free Variables ≥ 8

用户锁定的内容永远优先；系统自己脑补的内容不要升级成 Hard Anchor。

---

## 5. 全批次差异检查

Random Discovery 必须检查整个批次，而不是只看相邻两张。

核心差异维度：

1. Photographer Profile
2. scene
3. moment
4. shot size
5. lens
6. camera position
7. composition
8. foreground
9. lighting
10. wardrobe

默认要求：

- strong：任意新方案不得与已有方案在 7 个核心摄影维度中过度重合；
- wild：进一步优先所有未使用过的 Profile、Lens、Shot Size、Camera Position、Composition；
- 6 张以上至少覆盖 3 种景别层级；
- 6 张以上至少覆盖广角 / 标准 / 长焦中的两类；
- 8 张 strong 尽量覆盖 ≥4 个 Photographer Profiles；
- 8 张 strong 尽量覆盖 ≥6 个 Scene Cluster；
- 8 张 strong 尽量覆盖 ≥4 个 Camera Positions；
- 8 张 strong 尽量覆盖 ≥4 个 Compositions；
- wild 应比 strong 更高覆盖，而不是只换表情。

如果用户锁定某个维度，该维度不计入随机不足。

---

## 6. Random Prompt Compression

Images 2.5 随机模式的 Prompt 不应把所有随机结果全部写成硬约束。

内部完整抽取，外部只挑最能定义这一张照片的关系。

### Strong Prompt 优先保留

- 主体；
- 随机子场景；
- 一个进行中瞬间；
- 一个观察关系；
- 一个构图亮点；
- 一个光线亮点；
- 必要时一个空间层次线索。

### Wild Prompt 优先保留

- 用户 Hard Anchor；
- 一个鲜明子场景；
- 一个非常不同的观察关系；
- 一个未完成动作；
- 一个真实光线逻辑。

Wild 不应把每个内部变量都显式说出来，否则会把随机重新收敛成参数执行。

最终 Prompt 使用 `references/gpt_image_prompting.md` 中的 Images 2.5 Random 模板。

---

## 7. Taste 去收敛

随机探索不能被 Personal Taste 变成审美信息茧房。

默认：

```text
Standard：Taste 正常参与
Random balanced：Taste 可参与
Random strong：Taste 默认关闭；明确要求时弱加载
Random wild：Taste 基本退出
```

如果用户说：

```text
随机，但参考我的偏好
```

则只轻微调整概率，不允许把所有结果拉回熟悉焦段、构图和光线。

---

## 8. Random 与 Series

默认互斥：

```text
随机拍几张 / 多试几种
→ Random Discovery
```

```text
拍一套 / 九宫格 / 同一次写真 / 连续组照
→ Series Director
```

如果用户说：

```text
拍一套，但镜头随机一点
```

锁住人物身份、核心服装、地点和时间，只随机镜头层。

不要随机脸。

---

## 9. Random 与 Reference DNA

用户上传参考图后说：

```text
参考这张图，随机多试几种
```

只锁 Reference DNA 中 2–4 个最高置信结构锚点，例如：

- 人物占比；
- 摄影距离；
- 光线方向；
- 构图重心。

其余继续随机。

不要把参考图变成一个把探索空间全部锁死的模板。

---

## 10. 失败模式

出现以下情况说明 Random 不够随机：

- 只是同一个人换动作；
- 每张都白 T + 牛仔裤；
- 每张都是树荫路；
- 每张都 35mm 平视；
- 每张都人物偏右 + 大留白；
- 每张都是同一色调；
- 每张都像同一个摄影师；
- 所谓 Wild 只是加了更多噪点、眩光或夸张色彩。

正确做法是重抽“拍法世界”，不是叠更多效果。

---

## 11. 最终检查

Random 批次生成前后都要问：

1. 这些照片如果不看人物，拍法是否仍然明显不同？
2. 场景是否真的扩展了，而不是换背景牌？
3. 摄影师与主体的关系是否变化？
4. 景别、焦段和机位是否有跨度？
5. 是否错误继承了上一张身份、服装或色调？
6. Prompt 是否因为写得太满而把随机重新锁死？

如果第 1、3、4 项不成立，继续重组。