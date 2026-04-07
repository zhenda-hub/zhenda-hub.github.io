+++
title = 'Umami 统计部署指南'
subtitle = '自建隐私友好的网站分析'
date = 2025-04-07T00:00:00+08:00
draft = false
toc = true
tags = ['Hugo', 'Blowfish', 'Umami', 'Analytics', 'Railway']
series = ['Hugo Blowfish 指南']
+++

# Umami 统计部署指南

本指南帮助你在 Railway 上部署 Umami 统计，为博客添加隐私友好的网站分析功能。Umami 是 Google Analytics 的开源替代方案，数据完全掌控在自己手中。

## 为什么选择 Umami？

| 特性 | Umami | Google Analytics |
|------|-------|------------------|
| **隐私** | ✅ GDPR 合规，无需 Cookie | ❌ 收集大量用户数据 |
| **数据掌控** | ✅ 完全自建，数据库在你手中 | ❌ 数据在 Google 服务器 |
| **界面** | ✅ 简洁现代 | ⚠️ 功能复杂但专业 |
| **成本** | ✅ 完全免费（Railway） | ✅ 免费但有配额 |
| **国内访问** | ⚠️ Railway 海外服务器 | ⚠️ Google 可能被墙 |

**推荐方案：** Firebase（前端展示） + Umami（后台分析）

## 部署方式对比

| 方式 | 优势 | 劣势 | 推荐度 |
|------|------|------|--------|
| **Railway** | 完全免费，零维护 | 数据在 Railway 平台 | ⭐⭐⭐⭐⭐ |
| **自己的 VPS** | 完全掌控，可选国内服务器 | 需付费，需维护 | ⭐⭐⭐ |
| **云服务版** | 无需部署 | 付费，数据不在自己手中 | ⭐⭐ |

**本指南采用 Railway 部署** - 完全免费且零维护。

## 部署步骤

### 步骤 1：注册 Railway

1. 访问 [Railway.app](https://railway.app/)
2. 使用 GitHub 账号登录

### 步骤 2：部署 Umami

**方式 A：一键模板（推荐）**

1. 访问 [Umami Railway 模板](https://railway.app/new/template/umami)
2. Railway 自动创建 Umami + PostgreSQL 服务
3. 等待部署完成

**方式 B：从 GitHub 部署**

1. Fork [umami-software/umami](https://github.com/umami-software/umami) 仓库
2. Railway 控制台 → **New Project**
3. 选择 **Deploy from GitHub repo**
4. 选择你 fork 的 umami 仓库
5. 添加 PostgreSQL 服务

### 步骤 3：配置环境变量

在 Railway 项目设置中，确认以下环境变量：

```bash
DATABASE_URL=postgresql://...  # Railway 自动生成
APP_SECRET=<随机密钥>          # 可选，系统会自动生成
```

生成 APP_SECRET（如需自定义）：
```bash
openssl rand -base64 32
```

### 步骤 4：获取项目 URL

部署完成后，在 Railway 项目页面找到：
```
https://你的项目名.railway.app
```

这是你的 Umami 管理面板地址。

### 步骤 5：初始化 Umami

1. 访问你的 Railway 项目 URL
2. 使用默认账号登录：
   - 用户名：`admin`
   - 密码：`umami`
3. **立即修改默认密码**（Settings → Account → Change Password）
4. 添加网站：
   - 点击 **Settings** → **Websites**
   - 点击 **Add website**
   - 输入博客 URL（如 `https://yourblog.com`）
5. 复制 **Website ID**（后续配置需要）

### 步骤 6：配置 Hugo

#### 配置方案对比

| 方案 | 安全性 | 复杂度 | 推荐度 |
|------|--------|--------|--------|
| **GitHub Secrets** | ✅ 高 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **直接提交配置** | ❌ 低 | ⭐ | ⭐⭐ |

**推荐使用 GitHub Secrets 方案** - 敏感信息不提交到仓库。

---

#### 方案 A：GitHub Secrets（推荐）

**1. 配置 GitHub Actions**

GitHub Actions workflow 已配置为从 Secrets 自动生成配置文件。

**2. 设置 GitHub Secrets**

在 GitHub 仓库中设置以下 Secrets（Settings → Secrets and variables → Actions）：

```bash
# Firebase 配置
FIREBASE_API_KEY=你的API_KEY
FIREBASE_AUTH_DOMAIN=你的PROJECT_ID.firebaseapp.com
FIREBASE_PROJECT_ID=你的PROJECT_ID
FIREBASE_STORAGE_BUCKET=你的PROJECT_ID.appspot.com
FIREBASE_MESSAGING_SENDER_ID=你的SENDER_ID
FIREBASE_APP_ID=你的APP_ID
FIREBASE_MEASUREMENT_ID=你的MEASUREMENT_ID

# Umami 配置
UMAMI_WEBSITE_ID=你的Website-ID
UMAMI_DOMAIN=你的项目.railway.app
```

**3. 本地开发配置**

创建 `config/production/params.toml`（已被 .gitignore 忽略）：

```toml
# config/production/params.toml
# 本地开发使用，不提交到仓库

[firebase]
  apiKey = "AIzaSy..."
  # ... 你的 Firebase 配置

[umamiAnalytics]
  websiteid = "1f7e9b04-..."
  domain = "umami-production-xxx.up.railway.app"
  enableTrackEvent = true
```

**工作流程：**
```
本地开发:
  config/production/params.toml → Hugo 读取

CI/CD 构建:
  GitHub Secrets → 生成 params.toml → Hugo 读取
```

---

#### 方案 B：直接提交配置（简单但不安全）

⚠️ **仅限私有仓库使用**

在 `config/production/params.toml` 中添加：

```toml
# config/production/params.toml

[umamiAnalytics]
  websiteid = "你的Website-ID"
  domain = "你的项目.railway.app"
  enableTrackEvent = true
```

直接提交到仓库（敏感信息会暴露）。

### 步骤 7：本地测试

由于配置在 `production` 目录，需要使用生产环境启动：

```bash
hugo server -D --environment production
```

**验证步骤：**

1. 访问 `http://localhost:1313/`（或显示的端口）
2. 打开浏览器开发者工具（F12）
3. 切换到 **Network** 面板
4. 刷新页面
5. 查找 `你的项目.railway.app/script.js` 的加载请求

**如果看到 script.js 加载成功** → 配置正确 ✓

### 步骤 8：验证数据收集

1. 访问 Umami 管理面板
2. 点击 **Dashboard**
3. 应该能看到你的访问记录
4. 数据包括：页面浏览量、访客数、实时访客等

### 步骤 9：部署到生产

**使用 GitHub Secrets 方案：**

```bash
# 提交代码（不包含敏感配置）
git add .github/workflows/hugo.yml content/posts/hugo_blowfish_guide/umami-analytics.md
git commit -m "feat: 添加 Umami 统计支持（GitHub Secrets）"
git push
```

**重要：**
- 确保 GitHub Secrets 已正确设置
- GitHub Actions 会自动从 Secrets 生成配置
- 首次部署后在 GitHub Actions 页面检查构建日志

---

**使用直接提交方案（不推荐）：**

```bash
git add config/production/params.toml
git commit -m "feat: 添加 Umami 统计分析"
git push
```

⚠️ 警告：敏感信息会被提交到仓库历史中。

### 步骤 10：验证部署

**检查 GitHub Actions：**

1. 访问仓库的 **Actions** 标签
2. 查看最新的构建日志
3. 确认 "Setup production config" 步骤成功
4. 确认 Hugo 构建成功

**检查生产站点：**

1. 访问部署后的博客 URL
2. 打开浏览器开发者工具（F12）
3. 切换到 **Network** 面板
4. 刷新页面
5. 在 Filter 中输入 `umami` 或 `railway.app`
6. 查找 `你的项目.railway.app/script.js` 的加载请求

**验证成功标志：**
```
umami-production-xxx.up.railway.app/script.js  ✅ 200 OK
```

如果看到 `✅ 200 OK`，说明 Umami 脚本加载成功！

**检查 Umami 面板：**

1. 访问 Umami 管理面板
2. 查看 Dashboard 是否有数据
3. 确认实时访客功能正常



## 数据备份

虽然 Railway 稳定可靠，但定期备份是好习惯：

```bash
# 安装 Railway CLI
npm install -g @railway/cli

# 登录
railway login

# 进入项目
railway open

# 导出数据库
pg_dump $DATABASE_URL > umami-backup.sql
```

建议每月备份一次。

## Railway 免费额度

| 资源 | 免费额度 |
|------|---------|
| 执行时间 | $5/月（约 500 小时）|
| 内存 | 512MB RAM |
| PostgreSQL | 1GB 存储 |
| 流量 | 100GB/月 |

**个人博客完全够用！**

## 双统计方案说明

当前博客采用 **Firebase + Umami** 双统计方案：

### Firebase（前端展示）
- ✅ 文章浏览数显示
- ✅ 点赞功能
- ✅ 社交证明，增加互动
- ❌ 数据在 Google 服务器

### Umami（后台分析）
- ✅ 访客来源分析
- ✅ 设备、浏览器统计
- ✅ 地理位置分布
- ✅ 实时访客监控
- ✅ 数据完全掌控
- ❌ 无前端展示功能

**两者互补，功能最全！**

## 常见问题

### Railway 部署后无法访问

**检查步骤：**
1. Railway 项目状态是否为 "Running"
2. 查看部署日志是否有错误
3. 确认 PostgreSQL 服务已启动
4. 尝试重新部署

### 本地测试看不到 script.js

**可能原因：**
- 没有使用 `--environment production` 启动
- 配置文件语法错误

**解决方法：**
```bash
# 检查配置文件语法
hugo config

# 使用正确的环境启动
hugo server -D --environment production
```

### Umami 面板没有数据

**可能原因：**
1. Website ID 配置错误
2. 脚本未正确加载
3. 广告拦截器阻止了脚本

**解决方法：**
1. 检查 `websiteid` 是否正确复制
2. 在 Network 面板确认 script.js 加载状态
3. 暂时禁用广告拦截器测试

### Railway 免费额度用完会怎样？

**Railway 政策：**
- 免费额度每月重置
- 超出后服务暂停，下月自动恢复
- 可以升级付费计划（$5/月起）

**备选方案：**
- 迁移到自己的 VPS（导出数据，重新部署）
- 使用其他免费平台（Render、Fly.io）

## 迁移到自己的服务器

如果将来需要从 Railway 迁移到自己的服务器：

### 数据导出
```bash
# 在 Railway Shell 中
pg_dump $DATABASE_URL > backup.sql
```

### 重新部署（Docker）
```bash
# 拉取 Umami 镜像
docker pull ghcr.io/umami-software/umami:postgresql-latest

# 启动容器
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://... \
  -e APP_SECRET=... \
  ghcr.io/umami-software/umami:postgresql-latest
```

### 数据导入
```bash
# 导入到新数据库
psql $NEW_DATABASE_URL < backup.sql
```

### 更新 Hugo 配置
```toml
[umamiAnalytics]
  websiteid = "..."
  domain = "your-new-domain.com"  # 新域名
```

## 自建统计方案对比

| 方案 | 技术栈 | 资源占用 | 活跃维护 |
|------|--------|---------|---------|
| **Umami** | Node.js + PostgreSQL | ~200MB RAM | ⭐⭐⭐⭐⭐ |
| **GoatCounter** | Go + SQLite | ~20MB RAM | ⭐⭐⭐⭐ |
| **Shynet** | Python + Django + PostgreSQL | ~300MB RAM | ⭐⭐（已归档） |

**推荐：** Umami - 功能完整、社区活跃、Railway 部署简单。

## 参考资料

- [Umami 官方文档](https://umami.is/docs)
- [Railway 文档](https://docs.railway.app/)
- [Blowfish Umami 配置](https://blowfish.page/zh-cn/docs/partials/#umami)
- [Umami GitHub](https://github.com/umami-software/umami)
