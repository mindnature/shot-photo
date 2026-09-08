# Random Discovery Examples

## 1. 小白最简单用法

```text
使用 $shot-photo。
大学生，素颜，校园。
随机给我 8 张，差异大一点。
```

系统应该主动变化：校园子场景、动作、景别、焦段、机位、构图、前景、光线、服装与摄影人格。

不应该把 8 张全部做成同一套白 T、同一条树荫路、同一人物距离。

## 2. 放飞一点

```text
使用 $shot-photo。
一个女生，城市里。
给我 10 张，越随机越好，什么摄影风格都试。
```

这类请求应进入 wild 探索，尽可能覆盖不同 Photographer Profiles。

## 3. 固定人物与地点，镜头随机

```text
使用 $shot-photo。
一个短发中国女生，广州老城区。
人物和广州固定，其余都随机，给我 8 张。
```

广州作为宽泛地点可展开成骑楼、榕树居民街、西关老巷、凉茶铺、社区便利店、珠江步道等子场景。

## 4. 固定焦段再随机

```text
使用 $shot-photo。
荷塘，28mm 固定。
其他全部随机，生成 8 张。
```

此时 28mm 是 Hard Anchor，但动作、景别、机位、构图、前景、光线、服装仍应大幅变化。

## 5. 参考图 + 随机

```text
使用 $shot-photo。
参考这张图的摄影关系，不复制人物和具体背景。
保留最重要的拍法，其余随机给我 8 种。
```

只锁定 2–4 个最高置信 Reference DNA，避免参考图把随机空间全部锁死。

## 6. 随机但参考个人偏好

```text
使用 $shot-photo。
随机给我 8 张，但可以稍微参考我的 Personal Taste，不要太收敛。
```

Personal Taste 只能弱参与，探索优先。

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
