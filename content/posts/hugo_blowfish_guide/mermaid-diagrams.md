+++
title = 'Mermaid 图表支持'
subtitle = '在文章中使用 Mermaid 绘图'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'Mermaid']
series = ['Hugo Blowfish 指南']
+++

# Mermaid 图表

Blowfish 主题要求 mermaid 使用 shortcode，不用 fenced code block：

```diff
- ```mermaid
+ {{< mermaid >}}
  graph TD
    A --> B
- ```
+ {{< /mermaid >}}
```
