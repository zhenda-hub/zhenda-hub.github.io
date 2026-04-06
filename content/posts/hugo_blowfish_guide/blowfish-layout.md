+++
title = 'Blowfish 布局说明'
subtitle = '页面布局与组件介绍'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish']
series = ['Hugo Blowfish 指南']
+++

# Blowfish 布局配置

## Homepage Layout（主页布局）

| 布局 | 特点 | 适用场景 |
|------|------|----------|
| **profile** | 头像+简介+社交链接，居中显示 | 个人博客 |
| **page** | 纯 Markdown 内容 | 静态网站 |
| **hero** | profile + Markdown 内容 | 综合型 |
| **background** | 类似 hero，更平滑，需背景图 | 视觉型 |
| **card** | Markdown + 图片卡片 | 作品展示 |
| **custom** | 完全自定义 | 高级用户 |

**配置示例**：
```toml
[homepage]
  layout = "profile"  # 或 page, hero, background, card, custom
  showRecent = true
  showRecentItems = 9
  cardView = true
  showMoreLink = true
```

## Header Layout（头部布局）

| 布局 | 特点 |
|------|------|
| **basic** | 普通流动布局，随页面滚动 |
| **fixed** | 固定在顶部，始终可见 |
| **fixed-fill** | 固定 + 背景填充色 |
| **fixed-fill-blur** | 固定 + 填充 + 背景模糊效果（毛玻璃） |

**推荐**：`fixed` 或 `fixed-fill`

**配置示例**：
```toml
[header]
  layout = "fixed"  # 或 basic, fixed-fill, fixed-fill-blur
```
