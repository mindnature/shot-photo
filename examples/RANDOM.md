# Random Discovery Examples — v0.6 Images 2.5

## 1. 小白最简单用法

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异大一点。
```

系统应该主动变化：

- Photographer Profile
- 校园子场景
- Observation Relationship
- 动作
- 景别
- 焦段
- 机位
- 构图
- 前景
- 光线
- 服装

不应该把 8 张全部做成同一套白 T、同一条树荫路、同一人物距离。

Random Strong 默认不要求人物身份连续；如果用户没有说“同一个人”，每张可以是不同学生。

---

## 2. 放飞一点

```text
使用 $shot-photo。
一个女生，城市里。
给我 10 张，越随机越好，什么摄影风格都试。
```

进入 wild 探索：

- 尽可能覆盖不同 Photographer Profiles；
- 不继承上一张人物脸、服装和色调；
- 优先没有出现过的 Scene / Lens / Shot / Camera Position / Composition；
- Prompt 进一步压缩，给 Images 2.5 更多发明空间。

---

## 3. 固定人物条件与大地点，其他随机

```text
使用 $shot-photo。
短发中国女生，广州老城区。
人物条件和广州固定，其余都随机，给我 8 张。
```

这里固定的是“短发中国女生”这个人物条件，不代表必须是同一张脸。

广州作为宽泛地点可展开成骑楼、榕树居民街、西关老巷、凉茶铺、社区便利店、珠江步道等子场景。

如果确实要同一张脸，应明确说：

```text
同一个人，其他都随机。
```

---

## 4. 固定焦段再随机

```text
使用 $shot-photo。
荷塘，28mm 固定。
其他全部随机，生成 8 张。
```

28mm 是 Hard Anchor，但动作、景别、机位、观察关系、构图、前景、光线、人物造型仍应大幅变化。

---

## 5. 参考图 + 随机

```text
使用 $shot-photo。
参考这张图的摄影关系，不复制人物和具体背景。
保留最重要的拍法，其余随机给我 8 种。
```

只锁 2–4 个最高置信 Reference DNA，避免参考图把随机空间全部锁死。

---

## 6. 随机但参考个人偏好

```text
使用 $shot-photo。
随机给我 8 张，但可以稍微参考我的 Personal Taste，不要太收敛。
```

Personal Taste 只能弱参与：

```text
strong ≤ 15%
wild ≤ 5%
```

探索优先。

---

## 7. Images 2.5 的 Prompt 应该更短

Random Strong 示例：

```text
9:16 真实手机感生活摄影。一位素颜大学生在校园食堂端着餐盘刚转过身，似乎有人在旁边叫她。摄影师从排队人群边缘近距离记录，让餐盘和周围学生形成自然空间层次。食堂冷白灯混合窗外日光，保持普通校园生活的颜色和质感。像朋友随手拍到，不要精修摆拍感。
```

Random Wild 示例：

```text
9:16 真实生活摄影。为一位大学生在校园创造一张意外但可信的照片：她坐在空教学楼楼梯转角，刚把背包放到脚边准备起身。摄影师从楼上栏杆后略高处偶然看到这一瞬间，只使用走廊窗光。保持日常可信，不要商业写真感。
```

不要再把所有后台变量机械写成一长串。

---

## CLI

### strong

```bash
python scripts/generate_random.py "一个大学生，素颜" \
  --scene 校园 \
  --count 8 \
  --strength strong \
  --seed 42
```

### wild

```bash
python scripts/generate_random.py "一个年轻女生" \
  --scene 城市街头 \
  --count 10 \
  --strength wild \
  --seed 42
```

### 锁焦段

```bash
python scripts/generate_random.py "一个短发中国女生" \
  --scene 广州 \
  --lens 35mm \
  --count 8 \
  --strength strong \
  --seed 42
```

### JSON 输出

```bash
python scripts/generate_random.py "一个大学生" \
  --scene 校园 \
  --count 8 \
  --format json \
  --seed 42
```

JSON 输出会包含 `coverage.observation_relationships`，用于验证随机不仅换场景，也换摄影师与主体的观察关系。