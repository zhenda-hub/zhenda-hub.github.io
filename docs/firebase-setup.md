# Firebase 配置指南

本指南帮助你配置 Firebase 以启用文章浏览数和点赞功能。

## 前置条件

- 已有 Firebase 项目：`myblogpj-5d138`
- 项目配置已填写在 `config/production/params.toml` 中

## 步骤 1：启用 Firestore Database

1. 访问 [Firebase Console](https://console.firebase.google.com/)
2. 选择项目 `myblogpj-5d138`
3. 在左侧菜单点击 **Firestore Database**
4. 点击 **创建数据库**
5. 选择生产模式或测试模式（推荐先选测试模式，配置好规则后再切换）
6. 选择数据库位置（建议选择离用户最近的位置）

## 步骤 2：配置 Firestore 安全规则

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

## 步骤 3：启用匿名认证

1. 在左侧菜单点击 **Authentication**
2. 点击 **开始使用** 或 **Sign-in method** 标签
3. 找到 **匿名** 选项
4. 点击启用开关
5. 点击 **保存**

## 步骤 4：验证配置

### 检查项目配置

确认 `config/production/params.toml` 包含以下配置：

```toml
[firebase]
  apiKey = "AIzaSyDIGc5dZeqsAJX33M6po3xYIogEjugbifs"
  authDomain = "myblogpj-5d138.firebaseapp.com"
  projectId = "myblogpj-5d138"
  storageBucket = "myblogpj-5d138.firebasestorage.app"
  messagingSenderId = "448658936520"
  appId = "1:448658936520:web:a7e69e8248fc892ffdcbfd"
  measurementId = "G-MFGMB6H85S"
```

### 本地测试

1. 启动 Hugo 开发服务器：
   ```bash
   hugo server -D
   ```

2. 打开浏览器访问 `http://localhost:1313/`

3. 打开浏览器开发者工具（F12），切换到 **控制台（Console）** 标签

4. 访问任意一篇文章，检查：
   - 控制台是否有错误信息
   - 文章下方是否显示浏览数和点赞按钮
   - 点击 Like 按钮是否有反应

## 步骤 5：功能测试

### 浏览数测试

1. 清除浏览器 localStorage（在控制台执行）：
   ```javascript
   localStorage.clear()
   ```

2. 刷新页面，浏览数应该显示为 1

3. 再次刷新页面，浏览数应该保持为 1（不会重复计数）

4. 在 Firestore Console 中检查 `views` 集合，应该能看到文档

### 点赞测试

1. 点击文章底部的 **Like** 按钮
2. 点赞数应该增加 1
3. 爱心图标应该从空心变为实心
4. 再次点击 Like 按钮，点赞数应该减少 1
5. 爱心图标应该变回空心

6. 在 Firestore Console 中检查 `likes` 集合，应该能看到文档

## 常见问题

### 点赞按钮没反应

**可能原因**：
1. Firebase 未初始化 - 检查控制台是否有错误
2. 安全规则未正确配置 - 确保步骤 2 已完成
3. 匿名认证未启用 - 确保步骤 3 已完成

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

### 找不到 firebase-config 元素

**可能原因**：
1. Firebase 配置未填写
2. 页面类型不支持（首页、分类页等）

**解决方法**：
检查 `config/production/params.toml` 中的 Firebase 配置是否完整

## Firestore 数据结构

配置完成后，Firestore 中应该有以下数据结构：

```
myblogpj-5d138 (数据库)
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

## 生产环境部署

配置完成后，部署到 GitHub Pages：

```bash
git add .
git commit -m "docs: add Firebase setup guide"
git push
```

GitHub Actions 会自动构建并部署，Firebase 功能将在生产环境生效。

## 参考资料

- [Firebase Firestore 文档](https://firebase.google.com/docs/firestore)
- [Firebase Authentication 文档](https://firebase.google.com/docs/auth)
- [Blowfish 主题文档](https://blowfish.page/)
