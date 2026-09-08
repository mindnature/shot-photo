# Random Discovery

Random Discovery 是 Shot Photo 的“探索模式”。目标不是让每一张都服从同一个摄影人格，而是在摄影物理合理的前提下，主动制造大幅差异和意外组合。

核心原则：

> 不用规则替代随机，而是让随机也懂摄影。

## 什么时候自动进入

用户出现以下表达时，默认进入 `strong` 随机：

- 随机拍几张
- 随便来几张
- 自由发挥
- 差异大一点
- 多试几种
- 给我惊喜
- 不知道拍什么，你决定
- 多来点不同的

用户出现以下表达时进入 `wild`：

- 放飞一点
- 越随机越好
- 完全随机
- 脑洞大一点
- 不要收敛
- 什么风格都试试

## 三种强度

### balanced

保留一个主 Photographer Profile，但大幅随机：场景、动作、景别、焦段、机位、构图、前景和光线。适合用户想保持整体气质但希望镜头差异明显。

### strong（默认随机模式）

- 每张允许切换 Photographer Profile。
- 尽量避免连续重复 Profile。
- 场景、动作、景别、焦段、机位、构图、前景、光线均强随机。
- Personal Taste 只提供很弱的参考，默认不加载 Taste。
- 不启用 Series Director。
- 不要求整批像同一次拍摄。
- 用户没有锁定服装时，服装也允许变化。

### wild

- 摄影人格在整批中尽可能广覆盖。
- 对历史偏好基本去耦，不让 Personal Taste 把探索拉回熟悉区。
- 允许更大胆的景别、观察距离、构图和光线切换。
- 仍必须通过 Lens / Scene / Light compatibility，不生成物理上明显荒谬的组合。

## Random Anchor Budget

随机模式仍尊重用户明确要求。

例如：

```text
一个大学生，素颜，校园，随机 8 张。
```

应锁定：

- 大学生
- 素颜
- 校园

其余尽可能随机：

- 场景子区域：图书馆、教学楼、操场、食堂、自行车棚、楼梯、树荫、走廊等
- 动作
- 景别
- 焦段
- 机位
- 构图
- 前景
- 光线
- 服装细节（若用户未锁定）

不要因为用户说“校园”，就把 8 张全部生成成同一个树荫步道 + 白 T + 牛仔裙。

## 强化差异规则

Random Discovery 不只检查相邻两张，而检查整个批次。

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

- `strong`：任意新方案不得与已有方案在 7 个摄影核心维度中重复 3 项以上。
- `wild`：进一步优先未使用过的 Profile、Lens、Shot Size、Camera Position 和 Composition。
- 6 张以上至少覆盖 3 种景别层级。
- 6 张以上尽量覆盖广角 / 标准 / 长焦至少两类。
- 8 张以上 strong 模式尽量覆盖至少 4 个 Photographer Profiles；wild 尽量覆盖更多。

如果用户锁定场景或焦段，相应维度不计入“随机不足”的惩罚。

## Taste 的探索比例

随机探索不能被 Personal Taste 变成审美信息茧房。

推荐：

```text
普通生成：Personal Taste 正常参与
Random strong：约 70% 探索 / 30% 已知偏好
Random wild：约 90% 探索 / 10% 已知偏好
```

脚本默认 Random Discovery 不加载 Taste；只有用户明确说“随机，但参考我的偏好”时才允许弱加载。

## 与 Series Director 的关系

两者默认互斥：

- “随机拍几张 / 多试几种” → Random Discovery
- “拍一套 / 九宫格 / 同一次写真 / 连续组照” → Series Director

如果用户同时说“拍一套，但每张随机差异很大”，优先保留 Series 的身份与时间连续性，只在镜头层增加随机，不随机人物身份与核心服装。

## 与 Reference DNA 的关系

用户上传参考图后又说“参考这张图，随机多试几种”，锁定 Reference DNA 的 2–4 个最高置信结构锚点，其余进入 Random Discovery。

不要把参考图变成一个把随机空间全部锁死的模板。

## 前台语言

不要向小白展示 `balanced / strong / wild`，除非用户明确问高级设置。

自然语言对应：

- “随机一点” → balanced
- “随机拍几张 / 差异大一点 / 给我惊喜” → strong
- “放飞一点 / 越随机越好 / 什么都试” → wild

用户只需要描述想拍什么，其余由 Shot Photo 完成。