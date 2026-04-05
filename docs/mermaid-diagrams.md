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
