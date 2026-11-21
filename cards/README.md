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
python scripts/export-cards.py --post games/lol-cn-lines
```

- 数据来源：文章 `index.md` 里的 `{{< quotecard >}}` 块（编号 / 英雄名 / 称号 / 中英台词 / 判词）
- 图片：自动取 bundle 内 `imgs-chars/loading-<slug>.jpg`
- 依赖：本机 Chrome、`requests`、`websocket-client`
- 输出不写进 `public/`（那里被 .gitignore 忽略），直接落在本目录以便版本化

当前局限：只认 `quotecard` 块，散文类文章（无 quotecard）需要另写分屏逻辑。
