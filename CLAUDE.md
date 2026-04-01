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
- Triggered on push to `main` branch
- Builds with Hugo 0.128.0, minifies output
- Deploys to GitHub Pages
- CI/CD requires: `git submodule update --init` before `hugo` command

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
