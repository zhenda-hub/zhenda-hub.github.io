# Hugo 缓存清理

## 禁用缓存重新运行

```bash
rm -rf resources public && hugo server -D --disableFastRender --noHTTPCache
```

## 参数说明

| 参数/命令 | 作用 |
|-----------|------|
| `rm -rf resources public` | 删除缓存目录 |
| `--disableFastRender` | 禁用快速渲染，每次修改都完整重新构建 |
| `--noHTTPCache` | 禁用 HTTP 缓存 |
