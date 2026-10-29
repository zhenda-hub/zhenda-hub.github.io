+++
title = 'Blowfish 自定义规范与本博客的轻量做法'
subtitle = '官方要求是什么，我们为什么不重编译 Tailwind'
description = "记录 Blowfish 主题自定义的官方规范（custom.css 入口、配色方案格式、Tailwind 重编译、扩展点、覆盖即接管），以及本站为何选择更轻量的方案，附覆盖文件清单与 5 个实际踩过的坑。 | Blowfish customisation rules and our lightweight approach: the custom.css entry point, colour scheme format, Tailwind recompilation, extension points and override responsibilities."
date = 2026-10-30T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'CSS']
series = ['hugo-blowfish']
+++

给一个 Hugo 主题做自定义，最怕的不是写不出来，而是**写法不符合主题的设计意图** —— 升级主题时全崩，或者改了半天发现配置项被自己的模板吞掉了。

这篇把 Blowfish 官方文档（`/docs/advanced-customisation/`）的硬性规定和本站的实际做法放在一起，方便以后照着改。

## 一、官方规定（7 条）

| # | 规定 | 要点 |
|---|---|---|
| 1 | **永远不要改主题文件** | 官方原话：*you should never manually adjust any of the theme files directly*。一律靠 Hugo 的 lookup order 用项目同名文件覆盖 |
| 2 | **自定义样式只写 `assets/css/custom.css`** | Hugo 会自动 minify，并**加载在所有主题样式之后**，所以优先级最高 |
| 3 | **配色方案放 `assets/css/schemes/<name>.css`** | 颜色必须写成 **RGB 三元组**：`--color-primary-500: 139, 92, 246;`（Tailwind 靠它算透明度），再用 `colorScheme` 引用 |
| 4 | **字体放 `static/fonts/` + 在 custom.css 里 `@font-face`** | 官方推荐自托管，不依赖 CDN |
| 5 | **要用新的 Tailwind 工具类 → 必须重新编译主题 CSS** | 主题自带的 `compiled/main.css` 是**预编译产物**，Hugo 不会为你的模板重新跑 Tailwind |
| 6 | **只能用官方扩展点插脚本/样式** | `extend-head.html`（缓存）、`extend-head-uncached.html`（按页面条件）、`extend-footer.html`、`favicons.html` |
| 7 | **覆盖 = 完全接管** | 官方没说但必须知道：你覆盖了一个模板，主题原本读的配置就没人读了，要自己补回去 |

### CSS 打包顺序（决定谁能覆盖谁）

`themes/blowfish/layouts/partials/head.html` 里是按这个顺序 `resources.Concat` 的：

```
css/schemes/<scheme>.css   ← 配色变量
css/compiled/main.css      ← 预编译的 Tailwind（主题自带）
css/custom.css             ← 你的自定义样式（最后加载 → 优先级最高）
lib/zoom/style.css
```

所以「改样式写 custom.css」不只是官方建议，它在机制上就是最后一个生效的。

### 官方给的 Tailwind 重编译命令

```bash
node ./themes/blowfish/node_modules/@tailwindcss/cli/dist/index.mjs \
  -c ./themes/blowfish/tailwind.config.js \
  -i ./themes/blowfish/assets/css/main.css \
  -o ./assets/css/compiled/main.css --jit
```

产物放**项目的** `assets/css/compiled/main.css`，Hugo 会优先用它、覆盖主题那份。

## 二、我们为什么不重编译 Tailwind

| 对比项 | 方案 A：手写语义类（本站采用） | 方案 B：重编译 Tailwind（官方版） |
|---|---|---|
| 构建依赖 | 只需 `hugo` | 需要 node + 主题 `node_modules` |
| CI | 不用改，Actions 只跑 `hugo` | 每次都要多跑一步编译 |
| 改模板时要做什么 | 无（类名是自定义语义类） | 用了新工具类就得**重新编译并提交生成物** |
| 仓库体积 | 不变 | 多一份 ~150 KB 生成文件 |
| 风险 | 无 | 忘记重编译 → 样式静默失效 |

结论：本站样式集中在 `custom.css`，模板里**尽量不引入主题没用过的 Tailwind 工具类**；个别确有必要，就在 custom.css 里补等价定义（兼容层），把方案 A 走到底。

## 三、本站的做法（4 条原则）

**1. 样式只进 `assets/css/custom.css`**

当前 1262 行、23 个分节，按页面区块归类：设计令牌 / 基础排版 / 中英断行基线 / 导航 / 报头 / 板块标题 / 精选文章 / 卡片 / 列表 / 系列行 / prose / TOC / 页脚 / 404 / 搜索 / 动画 / 打印 / **兼容层** / 列表行宽。

**2. 模板只覆盖需要改的（15 个文件）**

```
layouts/
├── index.html                      首页调度器（按 homepage.layout 分发）
├── 404.html                        404 页
├── _default/list.html              文章列表（编辑感列表）
├── _default/term.html              标签/分类页
├── taxonomy/series.terms.html      系列总览（杂志式大列表）
└── partials/
    ├── header/basic.html           站头字标（保留 Logo / disableTextInHeader）
    ├── author-links.html           作者卡社交图标（受 showAuthorLinks 控制）
    ├── article-link/simple.html    列表条目（纯文字）
    ├── article-link/card.html      卡片（比例/悬停可配）
    ├── recent-articles/main.html   首页最近更新
    ├── home/featured.html          精选文章
    ├── comments.html               评论区
    ├── functions/gradient-index.html 渐变索引
    ├── extend-head.html            字体 + 统计
    └── extend-footer.html          图片放大兜底修复
```

**3. 不新增 Tailwind 工具类；必要时补兼容层**

`custom.css` 第 22 节就是兼容层，把模板里用到、但主题预编译产物里没有的 5 个类补上：

```css
.pb-7 { padding-bottom: 1.75rem; }
.gap-x-3 { column-gap: 0.75rem; }
.gap-y-1 { row-gap: 0.25rem; }
.tracking-widest { letter-spacing: 0.1em; }
.right-2 { right: 0.5rem; }
```

以后再遇到「明明写了类却没效果」，先查它是不是预编译产物里没有，然后加到这里。

**4. 覆盖模板必须保留主题配置**

覆盖即接管，所以每个覆盖文件都要把主题原本的开关读回来。当前保留的：

| 模板 | 保留的可配置项 |
|---|---|
| `index.html` | `homepage.layout`（custom / hero / profile / page / background / card / landing）、`homepage.layoutSwitcher` |
| `header/basic.html` | 顶层 `Logo`、`disableTextInHeader` |
| `author-links.html` | `article.showAuthorLinks` |
| `article-link/simple.html` | `list.constrainItemsWidth`、`article.showDraftLabel` |
| `article-link/card.html` | `list.thumbnailAspectRatio`、`list.featureImageHover`、`hotlinkFeatureImage`、`imagePositionFeature` |

## 四、实际踩过的 5 个坑

**1. 预编译 Tailwind：写了类没样式**

`list.html` 里的 `gap-x-3`、`pb-7`、`tracking-widest` 全部无效，因为主题 CSS 里根本没有这些类。判定方法：在最终 CSS 里 grep 类名。

**2. 覆盖模板把配置吞了**

`layouts/index.html` 曾经直接写死整页，导致 `homepage.layout` 改了毫无反应；`header/basic.html` 导致 `Logo` 失效；`author-links.html` 被清空导致 `Author.links` 完全不可用。**覆盖的代价是接管，配置要自己读。**

**3. Hugo 菜单按 identifier 去重**

页脚做纯图标行时，`name` 留空的多条菜单会在 Hugo 层被合并，只剩最后一条渲染。规则：**`name` 为空时，每条必须写唯一 `identifier`**。

**4. 模板 `style` 属性插值必须 `safeCSS`**

```go-html-template
style="--thumbnail-aspect-ratio: {{ $ratio | safeCSS }};"
```

漏了 `safeCSS`，Go 模板输出 `ZgotmplZ` 占位符，CSS 变量永远拿不到值。

**5. 配置写错层级就静默失效**

`Logo`、`disableTextInHeader`、`thumbnailAspectRatio`、`hotlinkFeatureImage` 这些是**顶层**参数；`featureImageHover`、`constrainItemsWidth`、`showDraftLabel` 在 `[list]` / `[article]` 段里。放错位置不会报错，只是不生效。

## 五、改动后的检查清单

- [ ] 样式改动只写进 `assets/css/custom.css`
- [ ] 文案/开关改 `params.toml`，注意顶层 vs 分段
- [ ] 模板里新用 Tailwind 类 → 先查是否已编译，没有就补进兼容层
- [ ] 覆盖了模板 → 确认对应主题参数仍然生效
- [ ] `hugo --minify` 构建通过
- [ ] 至少看 320 / 360 / 1280 三档宽度，确认无横向溢出
- [ ] 换图标后记得浏览器 favicon 缓存独立于页面缓存，需无痕验证
