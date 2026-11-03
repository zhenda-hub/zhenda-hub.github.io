# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static blog site deployed to GitHub Pages. The blog supports multiple Hugo themes as submodules, with **`blowfish`** as the active theme (`config/_default/hugo.toml`). Site-specific overrides live in the project's own `layouts/`, `assets/` and `config/` — the theme submodule is not edited.

## Common Commands

### Development Server
```bash
# Start development server (includes draft posts)
hugo server -D

# Start with full rebuild on file changes
hugo server -D --disableFastRender

# Server runs at http://localhost:1313/
```

### Building
```bash
# Production build (minified output)
hugo --minify

# Build output goes to `public/` directory
```

### Git Submodules
```bash
# Initialize and update all theme submodules (required after fresh clone)
git submodule update --init --recursive

# Add a new theme as submodule
git submodule add <repo-url> themes/<theme-name>
```

### Testing Changes
```bash
# Run Hugo config check
bash hugo-config-check.sh

# Check build without deploying
hugo --minify
ls -la public/posts  # Verify build output
```

## Architecture

### Multi-Theme Setup
The project uses git submodules for multiple Hugo themes. The active theme is set in `config/_default/hugo.toml`:
```toml
theme = "blowfish"  # Current active theme
```

Available themes (in `themes/`):
- `blowfish` - Active theme
- `puppet_zd`, `PaperMod`, `hextra`, `beautifulhugo`, `hugo-coder`, `LoveIt`

To switch themes, change the `theme` value and restart the server.

### Content Structure
```
content/
├── _index.md          # Homepage (branch bundle)
├── about/             # About page
├── archive/           # Archive page
├── link/              # Link page
├── posts/             # Blog posts — 每篇都是 page bundle（见下）
└── series/            # Series/collection pages
```

### 文章目录结构：page bundle（强制）

`content/posts/` 下**每篇文章都是 page bundle**，正文、封面、正文图全部跟着文章走：

```
content/posts/tech/pyqt5指南/
├── index.md              # 正文
├── featured.webp         # 封面（必须）
└── imgs/                 # 正文图
    ├── css-expression.jpg
    └── VeryCapture_20231125121414.jpg
```

规则：
- 文件名固定为 `index.md`（叶子 bundle），**不再使用** `xxx.md` 这种单文件写法
- 封面文件名以 `feature*` 开头（`featured.webp` / `featured.jpg` 等），blowfish 会自动识别，**不需要**写 `featureimage`；显式写也可以
- 正文图放 `imgs/` 或直接放 bundle 根目录，正文里用**相对 bundle 的路径**引用：`![说明](imgs/xxx.jpg)`
- **禁止** `../imgs/`（bundle 化后目录层级已变）、**禁止**把文章图放进 `assets/` 或 `static/`
- 多图排版优先用主题短代码：`figure`（单图带图注）、`gallery`（网格）、`carousel`（轮播）

迁移工具：`scripts/migrate-to-bundles.py`（叶子 md → bundle，含引用重写与 URL 保留）。
封面生成：`scripts/gen-covers.py`（按标题生成 1600×900 字标封面，输出到各 bundle 的 `featured.webp`）。

### Theme Customization
站点对主题的所有定制都在**项目根目录**，不改 `themes/blowfish/`：
- `layouts/` - 模板覆盖（`index.html` 首页、`partials/article-link/simple.html` 列表项、`partials/check-covers.html` 封面校验）
- `assets/css/custom.css` - 全站样式（报头、列表项、文章排版）
- `assets/img/` - 头像、社交分享卡等全站图片
- `config/_default/` - params / languages / menus

主题自带的图片查找顺序（`figure` 短代码、封面、hero 都一样）：
**page resource（bundle 内） → `assets/` → `static/`**。所以文章图放 bundle，全站图放 `assets/`。

### Article Frontmatter
Posts use TOML frontmatter. Common fields:
```toml
+++
title = "Post Title"
subtitle = "Optional subtitle"
date = 2024-01-01T00:00:00+08:00
draft = false
toc = true
tags = ['tag1', 'tag2']
series = []
featureimage = "featured.webp"  # 可省略：bundle 内有 featured.* 会自动识别
+++
```

### Deployment
- GitHub Actions workflow: `.github/workflows/hugo.yml`
- Triggered on push to `main` / `premium-design` branch
- Builds with Hugo 0.165.0, minifies output
- Deploys to GitHub Pages
- CI/CD requires: `git submodule update --init` before `hugo` command

### 图文文章排版规范 (premium-design)
文章页样式（图片/表格/引用/标题）已全局美化，写作时遵循以下约定即可获得最佳效果：

**图片**
- 图片一律放**文章 bundle 内**，正文用相对路径引用
- 单图：用 `figure` 短代码 + 中文图注（自动居中、圆角边框阴影、点击放大）
  ```md
  {{< figure src="imgs/image1.jpg" alt="多肉植物养护" caption="多肉植物养护实拍" >}}
  ```
- 多图网格：用 `gallery` 短代码；多图轮播：用 `carousel` 短代码
- 正文不要用裸 `![](img.jpg)`（无图注、无法利用 Hugo 图片优化）
- 封面：bundle 内的 `featured.*`（必须，缺失时构建直接失败，见 `layouts/partials/check-covers.html`）

**表格**：普通 markdown 表格即可，自动获得圆角 + 金色表头 + 斑马纹

**引用/强调**：口诀、名言用 `> 引用`，自动金色衬线样式

**标题层级**：正文用 `##` 起手（h2 带金色左边线），章节内用 `###`

### Key Configuration
- `config/_default/` - params / languages / menus（不再使用 `config.toml`）
- 封面字段统一为 `featureimage` 或 bundle 内的 `featured.*`；旧的 `header_img` **已失效**（puppet 时代遗留）
- 列表缩略图：由项目自定义的 `layouts/partials/article-link/simple.html` 渲染封面
- Supports Giscus comments, search, math rendering (Mermaid), syntax highlighting
- Taxonomies: categories, tags, series

## Important Notes

### 封面（必须）

- 判定：frontmatter 的 `featureimage` 有值，**或** bundle 内存在名称含 `feature` / `cover` / `thumbnail` 的图片
- 执行：`layouts/partials/check-covers.html` 在首页渲染时遍历所有 posts，缺封面直接 `errorf`，**构建失败、CI 不部署**
- 栏目页 `_index.md` 豁免
- 封面同时用于：列表缩略图、文章页顶部横幅（`article.showHero`）、社交分享卡

### Article Cover Images
文章页顶部横幅与列表缩略图**都**来自同一张封面，不再有 `header_img` 那套“横幅/缩略图”区分。

### Submodule Handling
Always ensure submodules are initialized before building or deploying. The GitHub workflow handles this automatically with `submodules: recursive`.
