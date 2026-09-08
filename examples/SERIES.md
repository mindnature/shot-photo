# Series Director Examples

## 1. 六张单地点组照

```text
使用 $shot-photo。
同一个短发中国女生，广州盛夏，生活感，9:16。
不要做 6 张互不相关的照片，要做成一套连续组照：同一人物、同一服装、同一地点、同一时间段，远中近有节奏，最后一张有离场感。
```

CLI：

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州盛夏生活感" \
  --series-mode single-location \
  --time-arc static \
  --seed 42
```

## 2. 九张小旅程

```text
使用 $shot-photo。
做一组 9 张雨后城市写真。
同一个人、同一套衣服，从便利店门口到公交站再到街口，空间必须能自然连续；不要每张换地点。
前面先交代环境，中间靠近人物，后面重新拉开并以离场结束。
```

CLI：

```bash
python scripts/generate_series.py "一位中国女性" \
  --count 9 \
  --profile 雨夜电影 \
  --intent "雨后城市短途步行" \
  --series-mode micro-journey \
  --time-arc progressive \
  --seed 42
```

## 3. 带 Personal Taste 的系列

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州夏日街头" \
  --taste-profile taste_profile.json \
  --series-mode single-location \
  --seed 42
```

Personal Taste 会影响每张镜头的摄影选择，但 Series Director 会防止偏好把整组压成相同焦段、相同构图。

## 4. 锁定服装世界

```bash
python scripts/generate_series.py "一位中国女性" \
  --count 6 \
  --scene "南方老宅窗边" \
  --wardrobe "米白色宽松衬衫与低饱和长裙，整组保持同一套" \
  --series-mode single-location
```

## 5. 有人物参考图时

在 ChatGPT / GPT Image 中上传人物参考图后：

```text
使用 $shot-photo 做一套 6 张组照。
人物身份严格参考我上传的照片，保持同一张脸、同一发型和年龄感。
摄影 DNA 参考第二张参考图的拍法，但不要复制它的衣服和背景。
整组在广州老城区完成，同一套衣服，同一时间段。
```

此时优先级：

```text
人物参考身份
> 当前用户 Hard Anchor
> Reference DNA
> Series Director
> Personal Taste
```

## 6. 推荐六张节奏

```text
01 建立空间：人物小、环境大
02 进入人物：中远景建立关系
03 动作发生：走、推门、回头、整理等进行中动作
04 靠近情绪：中近景或近景
05 重新拉开：恢复环境与呼吸
06 离场收束：背影、离开、停顿或即将走出画面
```

这六张不必讲完整故事，但必须让人感觉摄影师和人物在同一个真实时间里共同移动。
