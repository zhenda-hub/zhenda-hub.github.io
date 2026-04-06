+++
title = 'Blowfish 配置指南'
subtitle = '主题配置选项详解'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish']
series = ['Hugo Blowfish 指南']
+++

# Blowfish 配置选项

| 配置项 | 当前值 | 可选值 | 说明 |
|--------|--------|--------|------|
| **外观** | | | |
| `colorScheme` | blowfish | blowfish, avocado, fire, ocean, forest, neon, etc. | 主题配色 |
| `defaultAppearance` | light | light, dark | 默认外观 |
| `autoSwitchAppearance` | true | true, false | 自动切换深浅色 |
| **导航栏** | | | |
| `header.layout` | fixed | basic, fixed, fixed-fill, fixed-fill-blur | 导航栏样式 |
| **首页** | | | |
| `homepage.layout` | profile | profile, page, hero, card, background, custom | 首页布局 |
| `homepage.showRecentItems` | 999 | 数字 | 显示文章数 |
| `homepage.cardView` | true | true, false | 卡片视图 |
| **文章** | | | |
| `article.showHero` | false | true, false | 显示 Hero 图片 |
| `article.heroStyle` | - | basic, big, background, thumbAndBackground | Hero 样式 |
| `article.showBreadcrumbs` | false | true, false | 面包屑导航 |
| `article.sharingLinks` | - | bluesky, email, facebook, linkedin, mastodon, etc. | 分享按钮 |
| **列表页** | | | |
| `list.showHero` | false | true, false | 列表 Hero 图片 |
| `list.showSummary` | false | true, false | 显示摘要 |
| **其他** | | | |
| `footer.showAppearanceSwitcher` | false | true, false | 底部外观切换 |
| `smartTOC` | - | true, false | 智能 TOC 高亮 |

## 当前已启用的功能

- ✅ 搜索 (`enableSearch = true`)
- ✅ 代码复制 (`enableCodeCopy = true`)
- ✅ 固定导航栏 (`header.layout = "fixed"`)
- ✅ 文章目录 (`article.showTableOfContents = true`)
- ✅ 阅读时间 (`article.showReadingTime = true`)
- ✅ 字数统计 (`article.showWordCount = true`)
- ✅ 标题锚点 (`article.showHeadingAnchors = true`)
- ✅ 分类标签 (`article.showTaxonomies = true`)
- ✅ 按年份分组 (`list.groupByYear = true`)
- ✅ 卡片视图 (`list.cardView = true`)

## 待配置功能

- ⏸️ Giscus 评论（需要自定义 partial）
- ⏸️ 作者头像（需要添加图片）
- ⏸️ 文章缩略图（可选）
- ⏸️ 分享按钮
- ⏸️ Hero 图片
- ⏸️ 面包屑导航
