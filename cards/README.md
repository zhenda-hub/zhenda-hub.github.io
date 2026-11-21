# cards —— 小红书画卡片图

每篇文章一个目录，存该文导出的 3:4 卡片图（1080×1440）+ 文案。

```
cards/<分类-slug>/
├── 01.png        封面
├── 02.png …      正文卡片
└── caption.txt   小红书标题 + 正文 + 话题标签
```

生成：

```bash
# 台词类（解析 {{< quotecard >}}）：一篇 = 封面 + 每句一张
python scripts/export-cards.py --post games/lol-cn-lines

# 散文类（按 ## 分节 + figure 出图卡）
python scripts/export-cards.py --post life/pc-rebuild --mode prose     --kicker "装机 · 散热与风道" --cover-title "买的整机太吵<br>最后<em>换掉</em>了散热和机箱"
```

- `--mode quote`（默认）：数据源是 `{{< quotecard >}}` 块（编号 / 英雄名 / 称号 / 中英台词 / 判词）
- `--mode prose`：按 `##` 分节，有列表出「要点卡」（每张最多 4 条，超出自动续卡），没有列表出「观点卡」；每个 `{{< figure >}}` 单独出一张图卡
- `--cover-title` 支持 `<br>` 与 `<em>`（金色强调）
- 图片：自动取 bundle 内 `imgs-chars/loading-<slug>.jpg`
- 依赖：本机 Chrome、`requests`、`websocket-client`
- 输出不写进 `public/`（那里被 .gitignore 忽略），直接落在本目录以便版本化

当前局限：prose 模式只吃裸 markdown（表格已禁用）；短代码除 `figure` 外会被忽略。
