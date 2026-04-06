+++
title = '如何自定义文章标题'
subtitle = '设置文章大标题而非使用文件名'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish']
series = ['Hugo Blowfish 指南']
+++

## 概述

在 Hugo 中，文章显示的标题由 frontmatter 中的 `title` 字段控制，与文件名无关。这意味着你可以自由命名文件，而页面显示的标题完全由 frontmatter 决定。

## Frontmatter 格式

Blowfish 主题使用 TOML 格式的 frontmatter：

```toml
+++
title = '这里写文章标题'      # 控制页面显示的大标题
subtitle = "这里是副标题（可选）"
date = 2024-11-13T21:08:52+08:00
draft = false
toc = true
tags = ['标签1', '标签2']
series = []
+++
```

## 关键字段说明

| 字段 | 说明 | 示例 |
|------|------|------|
| `title` | **文章大标题**（必填） | `title = '我的文章'` |
| `subtitle` | 副标题（可选） | `subtitle = "这是一篇关于 Hugo 的文章"` |
| `date` | 发布日期 | `date = 2024-11-13T21:08:52+08:00` |
| `draft` | 是否为草稿 | `draft = false` |
| `toc` | 是否显示目录 | `toc = true` |

## 示例

**文件名**: `my-post-file.md`

**Frontmatter**:
```toml
+++
title = '这是一个完全自定义的标题'
subtitle = "副标题可以写得更详细一些"
date = 2024-11-13T21:08:52+08:00
draft = false
+++
```

页面将显示"这是一个完全自定义的标题"，而不是"my-post-file"。

## 注意事项

1. `title` 字段使用单引号包裹
2. 标题中可以使用中文、英文、emoji 等
3. 文件名建议使用英文或拼音，方便管理
4. 修改 `title` 后需要重启 Hugo 服务器才能看到效果（如果使用了 `--disableFastRender` 则不需要）
