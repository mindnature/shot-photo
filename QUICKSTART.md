# Shot Photo 快速上手

这份文档只面向第一次使用 Shot Photo 的人。

如果你不会摄影，也不会写复杂 Prompt，没有关系。你只需要记住一句话：

> **告诉 Shot Photo 你想拍什么，剩下的摄影决策交给它。**

---

## 1. 安装

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

安装后，重新打开或刷新支持 Skills 的 Codex / Agent 环境。

然后输入：

```text
$shot-photo
```

如果环境已经正确安装 Skill，后面的请求就会按 Shot Photo 的规则执行。

> 注意：`$shot-photo` 不是任意 ChatGPT 聊天窗口里的通用指令。当前环境必须支持 Skills，并且已经安装本仓库。

---

## 2. 第一次使用，直接复制这句

```text
$shot-photo
大学生，校园。
随机生成 8 张照片，差异尽量大，给我惊喜。
```

如果当前环境支持图像生成，Shot Photo 会直接把摄影方案用于生图；如果环境只支持文本，它会输出适合 GPT Image / Images 2.5 的摄影 Prompt。

---

## 3. 最常用的 4 种玩法

### A. 随机拍

适合：没想好怎么拍，只想先看到一批真正不同的方案。

```text
$shot-photo
一个女生，海边。
自然、松弛、有生活感。
随机生成 8 张，差异尽量大。
```

想更放飞：

```text
$shot-photo
一个大学生，校园。
生成 10 张，越随机越好，什么拍法都试，给我惊喜。
```

---

### B. 参考图片拍

适合：看到一张喜欢的图，但说不清为什么喜欢。

上传图片后：

```text
$shot-photo
参考这张照片的感觉。
不要照搬人物、衣服和具体背景。
随机生成 6 张类似摄影感的照片。
```

你也可以只说：

```text
$shot-photo
学这张图的拍法。
```

或者：

```text
$shot-photo
学这张图的感觉，换一个完全不同的场景。
```

---

### C. 拍一整套

适合：小红书九宫格、旅行写真、人物系列。

```text
$shot-photo
一个女生，广州夏天街头。
做一套 9 张连续写真。
同一个人、同一套衣服、同一个下午，像一次真实拍摄。
```

这时 Shot Photo 会优先保持人物、服装、时间和视觉世界连续，而不是把每张都随机打散。

---

### D. 第一轮不好，直接说哪里不满意

不用重写 Prompt。

```text
太摆拍了，重来，像朋友顺手拍到的一样。
```

```text
人物太大，让环境多一点。
```

```text
第 2 张最好，保留这种人物靠边的构图，但换个场景。
```

```text
光很好，但机位太普通，给我更大胆的角度。
```

```text
这次不要同一个人，随机性再强一点。
```

---

## 4. 小白万能公式

如果你不知道怎么写，就按下面 4 行：

```text
$shot-photo
[拍谁]
[在哪里]
[什么感觉]
[几张 / 是否随机 / 是否同一个人]
```

例如：

```text
$shot-photo
一个男大学生。
校园。
自然、干净、有少年感。
随机生成 8 张。
```

或者：

```text
$shot-photo
情侣。
海边小城旅行。
不要摆拍，像同行朋友记录的。
做一套 9 张。
```

---

## 5. 你完全不需要懂这些

Shot Photo 会自动处理：

- 焦段；
- 景别；
- 机位；
- 构图；
- 光线；
- 前景；
- 人物与摄影师的距离；
- 抓拍瞬间；
- 同一批照片之间的差异；
- 参考图的摄影关系。

所以不要为了“专业”主动塞很多摄影词。对于 Images 2.5，Shot Photo 更倾向于：

> **内部规划复杂，最终 Prompt 简洁。**

---

## 6. “随机”到底会随机什么

当你说：

```text
随机生成 8 张，差异尽量大。
```

系统不只是换动作，而会尽量变化：

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

例如“校园”可能自动展开成：

- 图书馆；
- 教学楼走廊；
- 食堂；
- 操场看台；
- 自行车棚；
- 空教室；
- 校园便利店；
- 宿舍楼下；
- 树荫主路；
- 楼顶连廊。

随机模式默认不强制沿用上一张的脸、衣服、发型和色调。

如果你想锁同一个人，请明确写：

```text
同一个人，其他都可以随机。
```

---

## 7. 参考图最简单的三句话

### 学拍法

保留摄影距离、机位、构图、空间、光线等关系，但人物和场景可以重做。

```text
$shot-photo
学这张图的拍法，不学具体内容。
```

### 学感觉

只保留情绪、光线、人物和镜头的关系。

```text
$shot-photo
学这张图的感觉，换到海边。
```

### 尽量复刻

更接近原图构图和视觉关系。

```text
$shot-photo
尽量按这张图复刻，但人物换成我指定的人。
```

---

## 8. 如何更新

如果你安装时保留了 Git 仓库，可以：

```bash
cd ~/.codex/skills/shot-photo
git pull
```

Windows PowerShell：

```powershell
Set-Location "$HOME\.codex\skills\shot-photo"
git pull
```

如果是手动复制安装，也可以重新下载仓库后覆盖旧目录。

---

## 9. 常见问题

### Q1：为什么输入 `$shot-photo` 没反应？

先确认：

1. 当前环境支持 Skills；
2. `shot-photo` 已放到 Skills 目录；
3. 文件夹里能看到 `SKILL.md`；
4. 安装后已经重新打开或刷新环境。

### Q2：为什么随机生成的人物不一样？

因为 Random Discovery 默认把“身份连续性”也当成自由度。想固定人物时，请写：

```text
同一个人，其他随机。
```

### Q3：为什么“拍一整套”反而没那么随机？

因为“整套写真”的目标是连续性。Shot Photo 会优先锁人物、服装和视觉世界，只随机镜头层。

### Q4：必须会 Python 吗？

不需要。日常使用只需要 `$shot-photo + 自然语言`。

`scripts/` 目录主要给需要可复现规划、自动化和二次开发的高级用户。

### Q5：一定要写 35mm、85mm 吗？

不需要。除非你本来就明确想锁定某个焦段，否则让 Shot Photo 自己判断通常更适合小白。

---

## 10. 下一步

更多可直接复制的示例：

[examples/BEGINNER_EXAMPLES.md](./examples/BEGINNER_EXAMPLES.md)

高级随机规则：

[references/random_discovery.md](./references/random_discovery.md)

参考图规则：

[references/reference_dna.md](./references/reference_dna.md)

一句话记住：

> **你负责说想拍什么，Shot Photo 负责决定怎么拍。**
