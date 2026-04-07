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
- ❌ 按年份分组 (`list.groupByYear = false`)
- ✅ 卡片视图 (`list.cardView = true`)
- ⏸️ Giscus 评论（需要自定义 partial）
- ⏸️ 文章缩略图（可选）
- ⏸️ 面包屑导航

## 待配置功能

- ⏸️ 作者头像（需要添加图片）
- ⏸️ 分享按钮
- ⏸️ Hero 图片

## 文章创建配置

修改 `archetypes/default.md` 可设置新文章的默认 front matter：

```toml
+++
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
subtitle = ""
date = {{ .Date }}
draft = false  # 默认发布状态
toc = true
series = []
+++
```

创建新文章时使用：
```bash
hugo new posts/my-new-article.md
```

## 文章摘要配置

Blowfish 主题根据文章开头格式自动生成摘要：

| 开头格式 | 摘要来源 | 示例 |
|---------|---------|------|
| 正文 + `<!--more-->` | `<!--more-->` 前的内容 | `这是摘要...<!--more-->## 正文` |
| `# 一级标题` + 正文 | 一级标题后的正文 | `# 标题\n这是摘要...` |
| `[toc]` / `## 二级标题` | ❌ 无摘要 | `[toc]\n## 正文` |

**添加摘要的方法：**

**方法 1：使用 `<!--more-->` 分隔符**
```markdown
+++
title = "文章标题"
+++

这是文章摘要，会显示在列表页...

<!--more-->

## 正文内容
正文开始...
```

**方法 2：使用 `summary` 参数**
```toml
+++
title = "文章标题"
summary = "这是自定义摘要"
+++
```
