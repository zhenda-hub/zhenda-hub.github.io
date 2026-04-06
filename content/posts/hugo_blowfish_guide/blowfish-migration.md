# Blowfish 迁移特性对比

| 特性 | puppet_zd | Blowfish | 迁移注意 |
|------|-----------|----------|----------|
| 数学公式 | ✅ | ✅ | 需配置 |
| 代码高亮 | ✅ | ✅ | 需配置 |
| Giscus 评论 | ✅ | ✅ | 需迁移 |
| 社交链接 | ✅ | ✅ | 需迁移 |
| 侧边栏 | ✅ | ❌ | 无此功能 |
| 朋友链接 | ✅ | ⚠️ | 需自定义页面 |
| RSS | ✅ | ✅ | 自动 |
| 搜索 | ❓ | ✅ | 需启用 |
| 深色模式 | ❓ | ✅ | 需配置 |
| 代码复制 | ❓ | ✅ | enableCodeCopy |
| 阅读时间 | ❓ | ✅ | showReadingTime |
| 目录 TOC | ❓ | ✅ | showTableOfContents |
| 分享按钮 | ❓ | ✅ | sharingLinks |
| 作者信息 | ✅ | ✅ | Author 配置 |
| 自定义 CSS/JS | ✅ | ✅ | 需迁移 |

## 当前关键配置

### Giscus
```
repo: zhenda-hub/zhenda-hub.github.io
repo_id: R_kgDOKvQVww
category: Announcements
category_id: DIC_kwDOKvQVw84CfdFG
input_position: top
theme: light
lang: en
```

### 社交
```
github: zhenda-hub
rss: true
```

### 朋友链接
```
- John Doe (https://gohugo.io)
- 梅塔沃克 (https://iweec.com/)
```

## Blowfish 配置文件结构
```
config/_default/
├── hugo.toml       # baseURL, theme, outputs, taxonomies
├── params.toml     # 主题参数
├── languages.en.toml  # 语言、作者信息
└── menus.en.toml   # 导航菜单
```

## 必须配置的参数

### hugo.toml
```toml
theme = "blowfish"
baseURL = "https://zhenda-hub.github.io/"
outputs.home = ["HTML", "RSS", "JSON"]  # 搜索必需
```

### params.toml
```toml
enableSearch = true
enableCodeCopy = true
defaultAppearance = "light"
autoSwitchAppearance = true

[homepage]
layout = "profile"
showRecent = true
showRecentItems = 999
cardView = true
```

### languages.en.toml
```toml
title = "Zhenda's Blog"

[params.author]
name = "Zhenda"
image = "img/avatar.jpg"
headline = "Stay hungry, stay humble, and keep shipping value."
bio = "A personal website"
links = [
  { github = "https://github.com/zhenda-hub" },
  { rss = "/index.xml" },
]
```

## 缩略图方案
- 方案 A: Page Bundle - 放 `feature*` 图片在文章目录
- 方案 B: 暂时不处理

## 参考
- [Getting Started](https://blowfish.page/docs/getting-started/)
- [Configuration](https://blowfish.page/docs/configuration/)
- [Homepage Layout](https://blowfish.page/docs/homepage-layout/)
