# 星图与尘埃 · 站点维护与写作规范

Hugo + blowfish，部署 GitHub Pages。定制全在项目根的 `layouts/` / `assets/` / `config/`，**不改 `themes/blowfish/`**。

## 命令

```bash
hugo server -D                          # 本地预览（含草稿），localhost:1313
hugo --minify                           # 生产构建 → public/
bash hugo-config-check.sh               # 配置自检
git submodule update --init --recursive # 新克隆后必须
```

## 结构

```
content/posts/<分类>/<slug>/
├── index.md        正文（page bundle，文件名固定）
├── featured.webp   封面，必须有
└── imgs/           正文图
```

- 正文图走相对路径，单图 `{{< figure src="imgs/x.jpg" caption="图注" >}}`，多图 `gallery` / `carousel`；不用裸 `![]()`
- 文章图放 bundle 内，**不**放 `assets/` 或 `static/`；全站图放 `assets/img/`
- 表格用普通 markdown（自动圆角 + 金色表头 + 斑马纹），强调用 `>`，正文标题从 `##` 起手

## frontmatter

```toml
+++
title = '...'
description = "一句话说结论，别复述标题"
date = 2026-11-18T23:40:00+08:00
draft = false
toc = true
series = ['system']
tags = ['SMB', '文件共享']
+++
```

## 封面（缺失 = 构建失败）

- 判定：`featureimage` 有值，或 bundle 内有名字含 `feature` / `cover` / `thumbnail` 的图
- `layouts/partials/check-covers.html` 首页渲染时遍历全部文章，缺封面直接 `errorf`，CI 不部署
- 生成：`python scripts/gen-covers.py --only <分类>/<slug> [--force]`
- 同一张图兼作列表缩略图、文章顶部横幅、分享卡；封面左上角分类取 `tags` 的第一个

## 写作

篇幅：默认 ≤2000 字（正文中文字符）；单一故障 / 操作 ≤500 字（现象、根因、修法、结果）。不为凑篇幅加背景铺垫、教学式科普、与正文重复的总结。

- **标题**：一句话说清功能，或「对象 + 问题」。禁 `记录` / `复盘` / `踩坑记` / `折腾记`；禁罗列系统、禁讲定义区别
- **钩子**：症状（可验证的一句）→ 反常识根因（加粗）→ 数字结果；先排除 2–3 个常见误判；禁「起因 / 背景 / 缘起」小节
- **抓核心**：一篇一个论点，前两段出现；每节第一句是结论，不是过渡句；删「换句话说 / 值得注意的是 / 其实 / 教训 / 小结」；判断标准是「删掉这句，读者损失什么」
- **定结构**：按读者要解决的问题排，不按「我查了什么」排；结论、清单在前；排查过程降级附录
- **名词**：混用概念（SMB / Samba）单独一节对齐关系；顺序是 是什么 → 什么关系 → 怎么用

## 标签

每篇 2–3 个，按「解决什么问题」命名，不按产品名。三条硬规则：

1. 与 series / 目录重名 → 不建
2. 模糊泛化 → 删（单独拎出来答不上「具体指什么」）
3. 已有更准的标签 → 删掉这个

准确性优先于数量，接受孤标签。不自动打标（试过两次，产出全是垃圾）。

## 坑

1. **`date` 写未来时间**：Hugo 默认跳过，构建成功但页面不出现，无任何报错
2. **改标题或 tags 后不重生成封面**：封面是图片，不会跟着 frontmatter 变
3. **dev server 缓存不自动重建**：新增文章、新建 series、加 tag 后列表页可能显示旧数据，日志干净无警告。先 `hugo --minify -d $TEMP/hugo-check` 静态构建对比；静态正常就是缓存，重启 server，别在内容上找问题
4. 中文标签在 HTML 里是 URL 编码，grep 中文会误判「没显示」；`hugo --minify` 输出属性不带引号

## 部署

push 到 `main` / `premium-design` 触发 `.github/workflows/hugo.yml`，Hugo 0.165.0 构建后发布 GitHub Pages；CI 里先 `git submodule update --init`。taxonomy：categories / tags / series；另有 Giscus 评论、搜索、Mermaid。
