# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static blog site deployed to GitHub Pages. The blog supports multiple Hugo themes as submodules, with `puppet_zd` (a fork of hugo-theme-puppet) as the active theme.

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
The project uses git submodules for multiple Hugo themes. The active theme is set in `config.toml`:
```toml
theme = "puppet_zd"  # Current active theme
```

Available themes (in `themes/`):
- `puppet_zd` - Active theme (custom fork)
- `PaperMod`, `blowfish`, `hextra`, `beautifulhugo`, `hugo-coder`, `LoveIt`

To switch themes, change the `theme` value in `config.toml` and restart the server.

### Content Structure
```
content/
├── _index.md          # Homepage
├── about/             # About page
├── archive/           # Archive page
├── link/              # Link page
├── posts/             # Blog posts (organized by subdirectories)
└── series/            # Series/collection pages
```

### Theme Customization
Custom theme modifications are in `themes/puppet_zd/` (the forked version). Key files:
- `layouts/_default/` - Main templates (single.html, list.html, li.html, summary.html)
- `layouts/partials/` - Reusable components
- `assets/sass/` - SCSS styles
- `static/` - Static assets (images, CSS, JS)

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
header_img = "img/image.jpg"  # Background image for article header
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
- 单图：用 `figure` 短代码 + 中文图注（自动居中、圆角边框阴影、点击放大）
  ```md
  {{< figure src="image1.jpg" alt="多肉植物养护" caption="多肉植物养护实拍" >}}
  ```
- 多图/图集：用 `gallery` 短代码
- 正文不要用裸 `![](img.jpg)`（无图注、无法利用优化）
- 文章横幅图：页面资源命名为 `featured.jpg` / `cover.jpg`（自动匹配），或 frontmatter 用 `featureimage`

**表格**：普通 markdown 表格即可，自动获得圆角 + 金色表头 + 斑马纹

**引用/强调**：口诀、名言用 `> 引用`，自动金色衬线样式

**标题层级**：正文用 `##` 起手（h2 带金色左边线），章节内用 `###`

### Key Configuration
- `config.toml` - Main Hugo configuration
- Theme uses `header_img` param for article header backgrounds (displays as page banner, not list thumbnail)
- Supports Giscus comments, search, math rendering (Mermaid), syntax highlighting
- Taxonomies: categories, tags, series

## Important Notes

### Article Cover Images
The `header_img` parameter sets the article page header background (banner style), NOT a thumbnail in article lists. The theme does not natively support list-view thumbnails. Adding this would require modifying `li.html` and `summary.html` templates.

### Submodule Handling
Always ensure submodules are initialized before building or deploying. The GitHub workflow handles this automatically with `submodules: recursive`.
