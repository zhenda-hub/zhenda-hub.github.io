+++
title = 'Blowfish 搜索功能'
subtitle = '搜索原理与常见问题'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', '搜索']
series = ['Hugo Blowfish 指南']
+++

# Blowfish 搜索功能说明

Blowfish 主题内置了基于 Fuse.js 的客户端搜索功能。

## 工作原理

### 1. 索引生成

Hugo 通过配置生成搜索索引文件 `index.json`：

```toml
# config/_default/hugo.toml
[outputs]
  home = ["HTML", "RSS", "JSON"]
```

索引文件包含：
- 页面标题
- 页面内容
- 标签和分类
- 永久链接
- 发布日期

### 2. 客户端搜索

- 使用 **Fuse.js** 库在浏览器中进行实时搜索
- 无需服务器端处理
- 搜索速度快，支持模糊匹配

### 3. 异步加载

- 打开搜索框时才加载 `index.json`
- 减少初始页面加载时间

## 配置

启用搜索功能：

```toml
# config/_default/params.toml
enableSearch = true
```

## 使用方法

1. 按下 `/` 键打开搜索框
2. 或点击页面右上角的搜索图标
3. 输入关键词进行搜索
4. 使用 `↑` `↓` 键选择结果，`Enter` 打开

## 常见问题

### 搜索找不到新文章

**原因**：索引未更新

**解决方法**：
```bash
# 重启 Hugo 服务器
hugo server -D --disableFastRender
```

### 搜索结果为空

**原因**：
1. 浏览器缓存了旧的索引文件
2. 多个 Hugo 进程冲突

**解决方法**：
1. 强制刷新浏览器：`Ctrl + Shift + R` 或 `Ctrl + F5`
2. 检查是否有多个 Hugo 进程：
   ```bash
   # Windows
   tasklist | findstr hugo

   # Linux/Mac
   ps aux | grep hugo
   ```
3. 关闭所有 Hugo 进程后重启

### 搜索框打不开

**原因**：`index.json` 加载失败

**解决方法**：
1. 打开浏览器开发者工具（F12）
2. 查看 Console 是否有错误
3. 检查 Network 标签，确认 `index.json` 是否成功加载
4. 检查 `index.json` 文件大小（正常情况下几十 KB 到几百 KB）

## 搜索不稳定的根本原因

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| 多进程冲突 | 启动了多个 Hugo 服务器 | 关闭所有进程后重启 |
| 缓存问题 | 浏览器缓存了旧索引 | 强制刷新浏览器 |
| 索引过期 | 修改文章后未重建 | 重启 Hugo 服务器 |
| 端口冲突 | 默认端口被占用 | Hugo 会自动使用其他端口 |

## 验证搜索功能

### 检查索引文件

访问 `http://localhost:1313/index.json`，确认文件存在且包含内容。

### 检查搜索配置

```bash
# 确认搜索已启用
grep "enableSearch" config/_default/params.toml

# 确认 JSON 输出已配置
grep -A5 "outputs" config/_default/hugo.toml
```

## 清理缓存

如果遇到问题，可以清理缓存后重启：

```bash
# 停止所有 Hugo 进程
pkill hugo

# 清理缓存
rm -rf resources public

# 重新启动
hugo server -D --disableFastRender --noHTTPCache
```

## 注意事项

1. **单实例运行**：确保只运行一个 Hugo 服务器
2. **及时重启**：修改文章或配置后重启服务器
3. **清除缓存**：遇到问题时先清除浏览器缓存
4. **检查日志**：查看 Hugo 控制台输出，确认没有错误
