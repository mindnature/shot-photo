# Series Director v0.8 Examples

Shot Photo 的系列模式现在默认启用 `Series Entropy`：身份、服装、地点与时间连续，但摄影关系主动变化。

## 1. 六张单地点组照

```text
$shot-photo
同一个短发中国女生，广州盛夏，生活感，9:16。
做一套 6 张连续组照：同一人物、同一服装、同一地点、同一时间段。
不要 6 张都用同一个角度；机位、动作、人物占比和构图要有明显变化。
像朋友真实拍的一次散步，不要商业写真感。
```

CLI：

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --scene 旧城区市场 \
  --intent "广州盛夏生活感" \
  --series-mode single-location \
  --entropy-strength strong \
  --time-arc static \
  --seed 42
```

## 2. 九宫格：同一个人，但差异要大

```text
$shot-photo
一个女生，广州夏天街头。
做一套 9 宫格。
同一个人、同一套衣服、像同一次真实拍摄。
但每张照片的机位、动作、人物占比和构图要变化，增加随机性，给我惊喜。
不要一直侧看微笑，也不要每张都抓着包带。
```

默认目标至少包含：

```text
3 种景别
4 种机位
4 种动作状态
4 种构图
5 种摄影师—人物观察关系
2 张遮挡 / 反射 / 人群干扰
1 张人物小比例大环境
1 张背影 / 半背影
1 张轻微真实摄影缺陷
```

CLI：

```bash
python scripts/generate_series.py "一个女生" \
  --count 9 \
  --scene 旧城区市场 \
  --entropy-strength strong \
  --series-mode single-location \
  --seed 42 \
  --format json
```

## 3. 参考人物 + 旅行组照

上传人物参考图后：

```text
$shot-photo
参考所给图片里的女生，云南丽江古城。
做一套 9 宫格写真。
同一个人、同一套衣服、像同一次真实拍摄，不要太多滤镜，主打真实。
每张机位、动作和构图要有变化，增加随机性，给我惊喜。
不要每张都做成丽江旅游宣传片，背景招牌不要满屏清晰可读。
```

内部优先级：

```text
人物参考身份
> 用户 Hard Anchor
> Series Continuity
> Reference DNA
> Series Entropy
> Personal Taste
```

## 4. 旅行系列的 Anti-Tourism-Poster

如果你发现结果每张都像景区广告，可以直接说：

```text
背景太像旅游宣传片。
保留地点真实性，但减少地标、灯笼、花墙和完整招牌。
多拍普通转角、阴影、半截店门、路人干扰和过渡空间。
```

Shot Photo v0.8 默认已经抑制大量可读背景文字。只有你确实需要清晰招牌时，CLI 才使用：

```text
--allow-readable-text
```

## 5. 九张小旅程

```text
$shot-photo
做一组 9 张雨后城市写真。
同一个人、同一套衣服，从便利店门口到公交站再到街口。
空间必须自然连续，但摄影关系要变化：有远处观察、跟拍、隔玻璃、人群空隙和低机位。
```

CLI：

```bash
python scripts/generate_series.py "一位中国女性" \
  --count 9 \
  --profile 雨夜电影 \
  --intent "雨后城市短途步行" \
  --series-mode micro-journey \
  --time-arc progressive \
  --entropy-strength strong \
  --seed 42
```

## 6. 更放飞的系列

身份和服装仍然连续，但镜头层进一步放开：

```bash
python scripts/generate_series.py "一个女生" \
  --count 9 \
  --scene 旧城区市场 \
  --entropy-strength wild \
  --seed 7
```

适合用户明确说：

```text
系列也放飞一点
每张都给我惊喜
越随机越好，但必须是同一个人
```

## 7. 带 Personal Taste

```bash
python scripts/generate_series.py "一位短发中国女性" \
  --count 6 \
  --intent "广州夏日街头" \
  --taste-profile taste_profile.json \
  --entropy-strength strong \
  --series-mode single-location \
  --seed 42
```

Personal Taste 可以影响概率，但不得把整组重新压成同一焦段、同一机位和同一种构图。

## 8. 六张推荐节奏

```text
01 建立空间：人物小、环境大
02 人物进入：同行朋友式抓拍
03 动作发生：真实物件或行走事件
04 靠近情绪：改变距离，不复制姿态
05 重新拉开：遮挡 / 反射 / 环境变化
06 离场收束：背影、半背影或即将走出画面
```

角色负责叙事节奏，Series Entropy 负责让每个角色拥有不同的摄影关系。

最终目标：

> 看起来是同一次真实拍摄，而不是九张互不相关的图；同时也不是同一张写真换九个背景。