# 星图与尘埃 · 站点维护与写作规范

Hugo + blowfish，部署 GitHub Pages。定制全在项目根的 `layouts/` / `assets/` / `config/`，**不改 `themes/blowfish/`**。

## 命令

```bash
hugo server -D --port 8080              # 本地预览（含草稿）→ http://localhost:8080
hugo --minify                           # 生产构建 → public/
bash hugo-config-check.sh               # 配置自检
git submodule update --init --recursive # 新克隆后必须
```

**预览一律用 `hugo server`。**禁止用 `python -m http.server` / `npx serve` 之类静态目录服务预览：

- 它只读 `public/`，改了 CSS/模板/正文不会重建，看到的可能是旧页面
- 它不认草稿与未来日期，调试时容易误判
- 多开一个服务还会和 hugo server 互抢端口、造成“改了没生效”的错觉

**端口别用 1313。**Windows 的 `winnat`（Hyper-V / WSL / Docker）会把 1064–1563 整段列入端口排除范围，`bind` 直接报 `errno 13`。固定用 **8080**；如果哪天也占用失败，用 `netsh interface ipv4 show excludedportrange protocol=tcp` 查一下当前排除段再换。

## 结构

```
content/posts/<分类>/<slug>/
├── index.md        正文（page bundle，文件名固定）
├── featured.webp   封面，必须有
└── imgs/           正文图
```

- 正文图走相对路径，单图 `{{< figure src="imgs/x.jpg" caption="图注" >}}`，多图 `gallery` / `carousel`；不用裸 `![]()`
- 文章图放 bundle 内，**不**放 `assets/` 或 `static/`；全站图放 `assets/img/`
- **不用表格**（小红书不支持，公众号里也容易溢出）。对比/参数/清单一律用列表：`1. **机箱**：旧 XX → 新 YY`，或用「**标签**：说明」的短行。需要并排时用短代码卡片（table 由短代码自己输出，不在正文里写）
- 强调用 `>`，正文标题从 `##` 起手

## frontmatter

```toml
+++
title = '...'
description = "一句话说结论，别复述标题"
date = 2026-11-18T23:40:00+08:00
draft = false
toc = true
series = ['system']
tags = ['SMB', '文件共享']
+++
```

## 封面（缺失 = 构建失败）

- 判定：`featureimage` 有值，或 bundle 内有名字含 `feature` / `cover` / `thumbnail` 的图
- `layouts/partials/check-covers.html` 首页渲染时遍历全部文章，缺封面直接 `errorf`，CI 不部署
- 生成：`python scripts/gen-covers.py --only <分类>/<slug> [--force]`
- 同一张图兼作列表缩略图、文章顶部横幅、分享卡；封面左上角分类取 `tags` 的第一个

## 写作

篇幅：默认 ≤2000 字（正文中文字符）；单一故障 / 操作 ≤500 字（现象、根因、修法、结果）。不为凑篇幅加背景铺垫、教学式科普、与正文重复的总结。

- **标题**：一句话说清功能，或「对象 + 问题」。禁 `记录` / `复盘` / `踩坑记` / `折腾记`；禁罗列系统、禁讲定义区别
- **钩子**：症状（可验证的一句）→ 反常识根因（加粗）→ 数字结果；先排除 2–3 个常见误判；禁「起因 / 背景 / 缘起」小节
- **抓核心**：一篇一个论点，前两段出现；每节第一句是结论，不是过渡句；删「换句话说 / 值得注意的是 / 其实 / 教训 / 小结」；判断标准是「删掉这句，读者损失什么」
- **定结构**：按读者要解决的问题排，不按「我查了什么」排；结论、清单在前；排查过程降级附录
- **名词**：混用概念（SMB / Samba）单独一节对齐关系；顺序是 是什么 → 什么关系 → 怎么用

## 标签

每篇 2–3 个，按「解决什么问题」命名，不按产品名。三条硬规则：

1. 与 series / 目录重名 → 不建
2. 模糊泛化 → 删（单独拎出来答不上「具体指什么」）
3. 已有更准的标签 → 删掉这个

准确性优先于数量，接受孤标签。不自动打标（试过两次，产出全是垃圾）。

## 坑

1. **`date` 写未来时间**：Hugo 默认跳过，构建成功但页面不出现，无任何报错
2. **改标题或 tags 后不重生成封面**：封面是图片，不会跟着 frontmatter 变
3. **dev server 缓存不自动重建**：新增文章、新建 series、加 tag 后列表页可能显示旧数据，日志干净无警告。先 `hugo --minify -d $TEMP/hugo-check` 静态构建对比；静态正常就是缓存，重启 server，别在内容上找问题
4. 中文标签在 HTML 里是 URL 编码，grep 中文会误判「没显示」；`hugo --minify` 输出属性不带引号
5. **英文撇号后面看着多一个空格**：Hugo 的 typographer 会把 `'` 转成弯撇号 `’`（U+2019），而中文字体（Noto Serif SC）把它按**全角标点**排版，多出约一个字宽（实测 40px 字号下 `isn’t` 113px vs `isn't` 81px）。已在 `config/_default/markup.toml` 里设 `[goldmark.extensions.typographer] apostrophe = "'"` 保持直引号。注意 `…`（U+2026）也是全角，但行尾无害

## 公众号转载

正文复制 → 微信公众号编辑器是可以直接用的，但有两条硬约束：

1. **正文元素禁用渐变背景**。Chrome 复制网页时会把**计算后的样式内联**进剪贴板，微信对渐变背景报「文字背景尽量不要使用渐变」，粘贴直接中断。
   - `blockquote` / `th` / `hr` 已从 `linear-gradient` 改成纯色 rgba（`assets/css/custom.css`），要层次就调透明度，不要用渐变。
   - 新增自定义组件、卡片、强调块时同样遵守。
   - 自检：`grep -o "\.[a-z-]*{[^}]*linear-gradient[^}]*}" public/css/main.bundle.min.*.css`，正文相关选择器应为空。
2. **正文别依赖 flex 布局**。微信会吃掉 `display:flex`，卡片塌成上下堆叠；需要左右结构用 `<table>` + `width` 属性。

另外：正文图片不用先上传——绝对 URL 的图粘进公众号编辑器时微信会自动抓取转存（图源需可公开访问、无防盗链、单张别太大）。

### 代码与表格：微信没有横向滚动

> 注意：正文已禁用 markdown 表格（小红书不支持），以下 `.article-content table` 的规则只服务于短代码内部的 table 布局。

公众号正文里 `overflow-x:auto` 是无效的，长行会被直接截掉。所以正文一律**折行**，不靠滚动：

```css
.article-content pre, .article-content pre * {
  white-space: pre-wrap !important;   /* Chroma 的行 span 设了 pre，只改 pre 不够 */
  overflow-wrap: anywhere;
  min-width: 0 !important;            /* prose 给 code 的 min-width:max-content 必须归零 */
}
.article-content table { table-layout: fixed; }  /* 均分列宽，否则文字列被压成 1~2 字 */
.article-content td :not(pre) > code { overflow-wrap: anywhere; font-size: .76em; }
```

两个坑：`min-width:max-content` 不归零，`pre-wrap` 也永远不会折行；`table-layout:auto` + `anywhere` 会把普通文字列压成竖排。

### 正文配色（方案 A，已落地）

公众号深色模式**不会改你写的颜色**，所以只能选一套「两种底色下都还看得过去」的值。单一色不可能两边都到 4.5:1（最优 `#7d7d7d` 也只有 4.1），最终选**亮色优先**的 A：

| 用途 | 值 | 白底 | 深底 #1a1a1a |
|---|---|---|---|
| 正文 | `#5f5f5f` | 6.39 | 2.75 |
| 标题 / strong | `#4a4a4a` | 8.86 | 1.98（深色下确实偏暗，接受） |
| 强调 / 链接 | `#b07d18` | 3.63 | 4.85 |
| 引用块底 | `rgba(176,125,24,.10)` + 左框 `.55` | — | — |
| 表头底 | `rgba(176,125,24,.13)` | — | — |
| 斑马纹 / 代码底 | `rgba(128,128,128,.07)` / `.10` | — | — |
| 表格线 / hr | `rgba(128,128,128,.28)` / `.35` | — | — |

两条铁律：

1. **底色一律半透明**，不写 `#fff` / `#f7f5f0` 实色。实色底在深色模式下就是一块刺眼白板，文字色怎么调都救不回来。
2. **站内深色模式不跟着变淡**：A 的深色表现本来就弱，`html.dark` 下用 `neutral-50/300` 覆盖成高对比（`h2`/`td` 容易漏，改色时必须补）。
3. **纸色不能画在 `body` 上**（已改）：Chrome 复制网页时会把可见底色「传播」给每个复制出来的块级元素，微信深色模式再把这块实色底渲染成浅灰方块（`#cdcdcd`），整篇文章变成一块块灰片。现在纸色放在 `body::before` 固定层：
   ```css
   body { background-color: transparent !important }
   body::before { content:""; position:fixed; inset:0; z-index:-1;
                  background-color: rgb(var(--color-neutral-50)) }
   html.dark body::before { background-color: rgb(var(--color-neutral-800)) }
   ```
   `::before` 不是任何被复制元素的祖先，传播不过去。**以后给页面加底/改主题色，不要再写回 `body` 或 `html`。**
   自检（Chrome 开发者工具控制台）：`html / body / main / article` 的 `background-color` 应全部为 `rgba(0,0,0,0)`。

## 小红书卡片图

`cards/<分类-slug>/` 存各文的 3:4 卡片图（1080×1440）+ `caption.txt` 文案，由
`python scripts/export-cards.py --post <分类/slug>` 生成，参数与依赖见 `cards/README.md`。

- 数据源分两种模式：`--mode quote`（默认）读正文的 `{{< quotecard >}}` 块；`--mode prose` 按 `##` 分节出要点卡/观点卡，每个 `{{< figure >}}` 单独出图卡
- 输出**不要**写进 `public/`（被 .gitignore 忽略），直接落 `cards/`；卡片是产物，不手改
- 改版式就改 `scripts/export-cards.py` 里的 `CSS` 常量，然后重跑一遍
- 文案要卡小红书限制：标题 ≤20 字、正文 ≤1000 字符、图 3:4 竖版、**不支持表格**
- **数字一律等高（lining figures）**：Georgia 默认是老式数字，`0 1 2` 矮、`6 8` 有升部、`3 5 7 9` 有降部，同字号看起来也像大小不一。所有数字元素统一：

  ```css
  .num {
    font-family: "Noto Serif SC Variable", "Songti SC", Georgia, serif;
    font-variant-numeric: lining-nums;
    font-feature-settings: "lnum" 1;
  }
  ```

  同理，数字字号只留两档：单个主角数字 190px、并排对比 132px，禁止 150/110/210 这类临时值。

- 英文撇号必须用直引号 `'`：弯撇号在衬线体里按全角排，会显示成 `It’ s`

### 封面：主次不能颠倒（血泪教训）

封面唯一的任务是在信息流里**让人停下来**，不是把标题排好看。已验证：米白底 + 96px 小字居中的版本好看，点击率打不过一张「丑但对比强」的深底大字。

正确主次（占比从大到小）：

1. **关键词最大**——「英雄联盟」「经典台词」这类主体词单独成行，约 200px，占宽 85%+，其中一行用色块反白（橙块/绿条）
2. **钩子句**放彩色条（约 44px）：带数字和冲突，如「11 句台词，被抄进签名十年」
3. **数字/补充句**降到第三层（约 58px），不许和关键词抢字号
4. **顶部主体图满幅**：3 张方图无缝拼接（每张 360px），在白色 feed 里有明确边界
5. 至少一个高饱和色块（橙 `#ff5a2b` / 绿 `#00c46a`）负责「跳」

**关键词必须是搜索词，不是描述词。**封面标题里要出现读者会去搜的那两个词（如「局域网」「提速」），而不是「传文件慢」这种状态描述——状态描述不产生搜索，也不产生点击欲。

**数字必须能被正文严格支撑。**写「6 倍」就得是 0.6 → 3.7 MB/s 这个换算；不能出现「8 倍」这种从别处借来的数字，点进去对不上会掉完收藏。

反面清单（不要再做）：

- 米白底 + 居中小字（白色 feed 里几乎隐形）
- 纯文字无主体图（上 1/3 空白）
- 把数字或长标题当主视觉，关键词反而小
- 一张封面同时想要「极简」和「抢眼」
- 标题只写状态（「传文件慢」），不写读者会搜的词（「局域网提速」）
- 用撑不住的数字（放大、取整、借用别处的倍数）

## 部署

push 到 `main` / `premium-design` 触发 `.github/workflows/gh-pages.yml`，Hugo 0.165.0 构建后发布 GitHub Pages；CI 里先 `git submodule update --init`。taxonomy：categories / tags / series；另有 Giscus 评论、搜索、Mermaid。
