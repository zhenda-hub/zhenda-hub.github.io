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

## 首页布局

```toml
[homepage]
  layout = "page"        # profile, page, hero, background, card
  cardView = true
  showRecentItems = 9
```

| 布局 | 说明 |
|------|------|
| profile | 头像+简介+社交链接 |
| page | 纯 Markdown 内容 |
| hero | 大标题 + Markdown |
| background | 背景图 + 内容 |
| card | 卡片式文章列表 |

## 列表页布局

```toml
[list]
  cardView = true        # 卡片视图（true）或列表视图（false）
  showSummary = true     # 显示摘要
  groupByYear = true     # 按年份分组
```

## 导航栏布局

```toml
[header]
  layout = "fixed"      # basic, fixed, fixed-fill, fixed-fill-blur
```

| 布局 | 说明 |
|------|------|
| basic | 普通流动 |
| fixed | 固定顶部 |
| fixed-fill | 固定+填充色 |
| fixed-fill-blur | 固定+毛玻璃 |

## 文章 Hero

```toml
[article]
  showHero = true
  heroStyle = "big"     # basic, big, background, thumbAndBackground
```

## 切换方法

**全局配置**: 修改 `config/_default/params.toml`

**文章级别**: 在 frontmatter 中覆盖
```toml
+++
[params]
  cardView = false
+++
```
