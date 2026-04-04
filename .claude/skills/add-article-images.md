---
name: add-article-images
description: 为文章添加图片（Page Bundle 格式 + Lorem Picsum 图片）
---

# 为文章添加图片（Page Bundle + 图片）

为单篇文章添加 Page Bundle 格式的图片，包括封面图和内容配图。

## 前置条件

- 文章当前是单文件 `.md` 格式
- Hugo 服务正在运行

## 流程步骤

### 1. 转换为 Page Bundle

```bash
# 创建同名目录并移动文件
mv content/posts/category/article.md content/posts/category/article/index.md
```

### 2. 下载图片

```bash
cd content/posts/category/article/

# 封面图（1200x630，JFIF格式需要特殊处理）
curl -L "https://picsum.photos/seed/{keyword}/1200/630" -o featured.jpg

# 内容配图（800x600）
curl -L "https://picsum.photos/seed/{keyword}1/800/600" -o image1.jpg
curl -L "https://picsum.photos/seed/{keyword}2/800/600" -o image2.jpg
```

### 3. 检查并转换图片格式

```bash
# 检查字节头
head -c 10 featured.jpg | xxd
```

- **JFIF 格式** (`FFD8 FFE0`) ✅ 可用
- **Exif 格式** (`FFD8 FFE1`) ❌ 需要转换

**如果 Exif 格式，复制已知的 JFIF 图片**：
```bash
# 从已转换的文章复制
cp /path/to/other/article/featured.jpg featured.jpg
```

### 4. 在文章开头添加封面图

编辑 `index.md`，在 frontmatter 后添加：

```markdown
+++
title = 'Article Title'
...
+++

![封面描述](featured.jpg)

## 原有标题
```

### 5. 内容配图已预先插入

如果文章已有 `![描述](image1.jpg)` 等引用，无需修改。

### 6. 验证 Hugo 构建

```bash
hugo --minify
```

### 7. 提交

```bash
git add content/posts/category/article/
git commit -m "feat: convert article-name to Page Bundle with images"
```

## 关键要点

1. **Lorem Picsum 总是返回 Exif 格式**，Hugo imaging 库可能无法处理
2. **解决方案**：复制已知的 JFIF 格式图片，或使用其他图片源
3. **Page Bundle 命名规则**：`featured.*` 自动作为封面图
4. **一篇一篇处理**：完成后提交，再处理下一篇

## 常见问题

**Q: Hugo 报错 `image: unknown format`**
A: 图片是 Exif 格式，需要转换为 JFIF。

**Q: 如何批量处理多篇文章？**
A: 使用 stash 逐篇处理，一次只处理一篇并提交。
