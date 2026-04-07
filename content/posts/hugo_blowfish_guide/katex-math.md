+++
title = 'KaTeX 数学公式'
subtitle = '在 Blowfish 中使用 KaTeX 渲染数学公式'
date = 2025-04-07T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'KaTeX']
series = ['Hugo Blowfish 指南']
+++

{{< katex >}}

# KaTeX 数学公式

Blowfish 主题使用 KaTeX 渲染数学公式。KaTeX 是一个快速的数学排版库。

## 启用方法

在文章中添加 `{{< katex >}}` shortcode（放在任意位置）：

```markdown
+++
title = "文章标题"
+++

{{< katex >}}

文章内容...
```

## 支持的公式格式

### 行内公式

使用 `\(...\)` 包裹：

```markdown
行内公式: \(E = mc^2\)
```

效果：行内公式: \(E = mc^2\)

### 块级公式

使用 `$$...$$` 或 `\[...\]` 包裹：

```markdown
$$
\varphi = \frac{1 + \sqrt{5}}{2} = 1.6180339887…
$$
```

效果：

$$
\varphi = \frac{1 + \sqrt{5}}{2} = 1.6180339887…
$$

## 配置原理

### 两层配置

| 层级 | 文件 | 作用 |
|------|------|------|
| Hugo Goldmark | `config/_default/markup.toml` | 保留 LaTeX 语法，不转换为 HTML 实体 |
| KaTeX auto-render | `themes/blowfish/assets/lib/katex/auto-render.min.js` | 渲染数学公式 |

### Hugo Goldmark 配置

`config/_default/markup.toml`：

```toml
[goldmark.extensions.passthrough.delimiters]
  block = [['\[', '\]'], ['$$', '$$']]
  inline = [['\(', '\)']]
```

这告诉 Hugo：不要转义这些分隔符之间的内容。

### KaTeX delimiters 定义

KaTeX auto-render 的默认分隔符（在 `auto-render.min.js` 中）：

| 分隔符 | 类型 | 说明 |
|--------|------|------|
| `$$...$$` | 块级 | 标准块级公式 |
| `\(...\)` | 行内 | 标准行内公式 |
| `\[...\]` | 块级 | LaTeX 标准块级 |
| `\begin{equation}...\end{equation}` | 块级 | equation 环境 |
| `\begin{align}...\end{align}` | 块级 | align 环境 |

**注意**：默认配置**不支持** `$...$` 作为行内公式分隔符。

## 常见问题

### Q: 为什么 `$E = mc^2$` 不渲染？

A: KaTeX 默认不支持 `$...$` 分隔符。使用 `\(...\)` 代替：

```markdown
❌ $E = mc^2$
✅ \(E = mc^2\)
```

### Q: 如何添加 `$...$` 支持？

A: 需要自定义 KaTeX 配置。创建 `layouts/partials/extend-head.html`：

```html
<script>
  document.addEventListener("DOMContentLoaded", function() {
    renderMathInElement(document.body, {
      delimiters: [
        {left: "$$", right: "$$", display: true},
        {left: "$", right: "$", display: false},
        {left: "\\(", right: "\\)", display: false},
        {left: "\\[", right: "\\]", display: true}
      ]
    });
  });
</script>
```

### Q: 中文文章自动摘要不工作？

A: Hugo 的 `.Summary` 基于空格分词，对中文不适用。使用 `<!--more-->` 手动分隔：

```markdown
+++
title = "文章"
+++

摘要内容...

<!--more-->

正文内容...
```

## 参考资源

- [KaTeX 官方文档](https://katex.org/docs/supported.html)
- [Blowfish 数学公式示例](https://blowfish.page/samples/mathematical-notation/)
- [Hugo Goldmark 配置](https://gohugo.io/getting-started/configuration-markup/#goldmark)
