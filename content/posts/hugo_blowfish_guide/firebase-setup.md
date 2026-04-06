+++
title = 'Firebase 集成指南'
subtitle = '添加页面浏览和点赞功能'
date = 2025-04-06T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'Firebase']
series = ['Hugo Blowfish 指南']
+++

# Firebase 配置指南

本指南帮助你配置 Firebase 以启用文章浏览数和点赞功能。Blowfish 主题已内置 Firebase 支持，使用 Firebase v9 ES modules 实现。

## 前置条件

- Blowfish 主题版本：2026-02-06 或更高（包含 Firebase v9 支持）
- 已有 Firebase 项目
- Firebase 配置将填写在 `config/production/params.toml` 中

## 步骤 1：创建 Firebase 项目

1. 访问 [Firebase Console](https://console.firebase.google.com/)
2. 点击 **添加项目**，创建新项目或选择现有项目
3. 按照向导完成项目创建

## 步骤 2：启用 Firestore Database

1. 在 Firebase Console 中，选择你的项目
2. 在左侧菜单点击 **Firestore Database**
3. 点击 **创建数据库**
4. 选择生产模式或测试模式（推荐先选测试模式，配置好规则后再切换）
5. 选择数据库位置（建议选择离用户最近的位置）

## 步骤 3：配置 Firestore 安全规则

1. 在 Firestore Database 页面，点击 **规则** 标签
2. 将规则替换为以下内容：

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /views/{documentId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    match /likes/{documentId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

3. 点击 **发布** 按钮

## 步骤 4：启用匿名认证

1. 在左侧菜单点击 **Authentication**
2. 点击 **开始使用** 或 **Sign-in method** 标签
3. 找到 **匿名** 选项
4. 点击启用开关
5. 点击 **保存**

## 步骤 5：获取 Firebase 配置

1. 在 Firebase Console 中，点击项目设置（齿轮图标）
2. 滚动到 **您的应用** 部分
3. 点击 **Web** 图标（或 `</>`）
4. 输入应用名称，点击 **注册应用**
5. 在 **Firebase SDK snippet** 部分，选择 **Config** 选项
6. 复制配置对象中的值

## 步骤 6：配置 Hugo

### 创建生产环境配置

创建 `config/production/params.toml` 文件（已在 `.gitignore` 中保护）：

```toml
# Production configuration
# This file overrides config/_default/params.toml
# It is NOT committed to git (.gitignore protects sensitive data)

[firebase]
  apiKey = "YOUR_API_KEY"
  authDomain = "YOUR_PROJECT_ID.firebaseapp.com"
  projectId = "YOUR_PROJECT_ID"
  storageBucket = "YOUR_PROJECT_ID.appspot.com"
  messagingSenderId = "YOUR_SENDER_ID"
  appId = "YOUR_APP_ID"
  measurementId = "YOUR_MEASUREMENT_ID"  # Optional
```

将步骤 5 中获取的配置值填入对应字段。

### 启用浏览数和点赞显示

在 `config/_default/params.toml` 中添加：

```toml
[article]
  showViews = true
  showLikes = true

[list]
  showViews = true
  showLikes = true
```

## 步骤 7：本地测试

### 使用生产环境启动

由于 Firebase 配置在 `config/production/` 目录，需要使用生产环境启动：

```bash
hugo server -D --disableFastRender --environment production
```

服务器运行在 `http://localhost:1313/`

### 功能测试

1. 打开浏览器访问 `http://localhost:1313/`
2. 进入任意一篇文章
3. 打开浏览器开发者工具（F12），切换到 **控制台（Console）** 标签
4. 检查：
   - 是否有 Firebase 相关错误
   - 文章下方是否显示浏览数和点赞按钮

### 浏览数测试

1. 清除浏览器 localStorage（在控制台执行）：
   ```javascript
   localStorage.clear()
   ```

2. 刷新页面，浏览数应该显示为 1
3. 再次刷新页面，浏览数应该保持为 1（localStorage 防止重复计数）
4. 在 Firestore Console 中检查 `views` 集合，应该能看到文档

### 点赞测试

1. 点击文章底部的 **Like** 按钮
2. 点赞数应该增加 1
3. 爱心图标应该从空心变为实心
4. 再次点击 Like 按钮，点赞数应该减少 1
5. 爱心图标应该变回空心
6. 在 Firestore Console 中检查 `likes` 集合，应该能看到文档

## 步骤 8：部署

配置完成后，部署到 GitHub Pages：

```bash
git add .
git commit -m "feat: enable Firebase views and likes"
git push
```

GitHub Actions 会自动构建并部署，Firebase 功能将在生产环境生效。

**注意**：CI/CD 已配置为使用生产环境（`HUGO_ENVIRONMENT: production`），Firebase 配置会自动加载。

## 常见问题

### 控制台报错 "Cannot use import statement outside a module"

**原因**：浏览器缓存了旧版本的 JavaScript 文件

**解决方法**：强制刷新浏览器（`Ctrl + Shift + R` 或 `Ctrl + F5`）

### 点赞按钮没反应

**可能原因**：
1. Firebase 未初始化 - 检查控制台是否有错误
2. 安全规则未正确配置 - 确保步骤 3 已完成
3. 匿名认证未启用 - 确保步骤 4 已完成

**解决方法**：
打开浏览器控制台，查看是否有类似以下的错误：
- `Missing or insufficient permissions` - 安全规则问题
- `auth/operation-not-allowed` - 匿名认证未启用

### 阅读数不增加

**可能原因**：
1. localStorage 已记录访问 - 正常行为，防止重复计数
2. Firebase 写入权限问题 - 检查安全规则

**解决方法**：
在控制台执行 `localStorage.clear()` 后刷新页面测试

### API key 显示为 "YOUR_API_KEY"

**原因**：没有使用生产环境启动服务器

**解决方法**：
```bash
hugo server -D --disableFastRender --environment production
```

## 技术说明

### Firebase 版本

- **Blowfish 主题** 使用 Firebase v9 ES modules
- 通过 `type="module"` 异步加载 Firebase SDK
- 无需在 HTML 中手动加载 Firebase 脚本

### 数据结构

Firestore 中的数据结构：

```
your-project-id (数据库)
├── views (集合)
│   ├── views_posts-some-post-index.md (文档)
│   │   └── { views: 10 }
│   └── views_posts-another-post.md (文档)
│       └── { views: 5 }
└── likes (集合)
    ├── likes_posts-some-post-index.md (文档)
    │   └── { likes: 3 }
    └── likes_posts-another-post.md (文档)
        └── { likes: 1 }
```

### 文档 ID 格式

- 文章页面：`views_posts/path/to/article.md`
- 分类页面：`views_taxonomy_category`
- 标签页面：`views_term_tag-name`
- 首页：`views_home`

## 成本估算

Firebase Spark 免费计划足够个人博客使用：

- Firestore 每天 50,000 次读取
- 每天 20,000 次写入
- 每月 1 GB 网络流量

对于中小型个人博客完全免费。

## 参考资料

- [Firebase Firestore 文档](https://firebase.google.com/docs/firestore)
- [Firebase Authentication 文档](https://firebase.google.com/docs/auth)
- [Blowfish 主题文档](https://blowfish.page/)
- [Firebase 定价](https://firebase.google.com/pricing)
