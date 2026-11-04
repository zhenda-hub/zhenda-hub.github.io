+++
title = '搜「海边」搜出一堆无关照片：immich 调优记录'
description = "4 核 N100 跑 immich：并发打满 CPU、硬件转码没开、CLIP 模型不懂中文。附官方基准和实测数据。"
subtitle = ""
date = 2026-11-01T23:10:00+08:00
draft = false
toc = true
series = ['life']
tags = ['immich', 'CLIP', 'OCR', '调优']
+++

[toc]

## 起因

手机传照片慢，搜「海边」出来一堆无关照片。查完发现两件事是同一个背景：4 核小机器被塞了太多活。

## 一、并发：默认值是为大机器准备的

`load average 30.51`，4 核，CPU 空闲 0%。数据库里的并发：

| 队列 | 原值 | immich 默认 | 改成 |
|---|---|---|---|
| faceDetection | 5 | 2 | 1 |
| smartSearch | 5 | 2 | 1 |
| **metadataExtraction** | 5 | 5 | **2** |
| ocr | 4 | 1 | 1 |

隐蔽的一层：ML 容器只有 1 个 gunicorn worker，但内部开了 **24 个线程**（ONNX 每个模型各一套线程池）。加 `OMP_NUM_THREADS=3` 后降到 18。

效果：缩略图 **5 张/分钟 → 54 张/分钟**，postgres 占用 65% → 1.2%。真正起作用的是 `metadataExtraction 5→2`。

## 二、硬件转码：设备给了，阀门没开

宿主机有 `/dev/dri/renderD128`，但容器没传。补上：

```yaml
    devices: ["/dev/dri:/dev/dri"]
    group_add: ["44", "992"]     # 写组名会报错，必须用数字 GID
```

验证通路：

```bash
ffmpeg -f lavfi -i testsrc -c:v h264_qsv -f null -
# libva: va_openDriver() returns 0；退出码 0
```

但 `ffmpeg.accel` 默认是 `Disabled`，还要在 **管理 → 设置 → 视频转码 → 硬件加速** 里打开。

> 我一开始以为这个 key 在 `transcode` 下面，挖了源码才发现 `transcode` 是 `ffmpeg` 内部的字段。

## 三、搜索不准：CLIP 模型不懂中文

日志显示加载 `ViT-B-32__openai`——2021 年的原始 CLIP，纯英文训练。

**自证方法**：英文搜 "beach" 准确、中文搜「海边」乱 → 100% 是模型语言问题，不用查索引。

中文 Recall（官方基准）与实测：

| 模型 | Recall | 耗时 | 维度 | 重建速度 |
|---|---|---|---|---|
| nllb-clip-large-siglip | 79.7% | 75ms | 768 | — |
| XLM-Roberta-Large-ViT-H-14 | 75.22% | 39ms | 1024 | — |
| nllb-clip-base-siglip | 74.8% | 15ms | 768 | 6.4 张/分 |
| **XLM-Roberta-Base-ViT-B-32** | 65.7% | 3.2ms | 512 | **43.7 张/分** |

两个坑：

1. **维度**：表是 `vector(512)`，nllb 是 768 维。但 immich 会自动 `ALTER`（日志有 `Updating database CLIP dimension size`），不用手工改。
2. **速度**：nllb 慢 6.8 倍。原因 384px vs 224px（像素 2.9 倍）+ 768 维索引（1.5 倍），理论 4.4 倍，实测 4.7 倍，对得上。

最终选 65.7% 那个：质量差 9 点，但重建 30 小时 vs 207 小时。

## 四、OCR：能搜图里的字

已处理 59,946 张（75%）。搜索用 pg_trgm 模糊匹配：

```sql
f_unaccent(ocr_search.text) %>> f_unaccent(query)
```

实测命中：订阅 651 / Shorts 249 / 梦露 82 / 海边 60 / 5G 16,129（高频词等于没有）。中文可用，但识别错误会传下去（抽样有 `RUEICGE`、`③@Lii-31` 这种乱码）。这版只有 `PP-OCRv5_mobile`，更好的 v6 要 immich 3.3.0+。

## 教训

1. **默认并发是为服务器定的**，4 核上会把 CPU 打满，症状却表现为"上传慢"。
2. **降并发反而快 10 倍**——省下的不是算力，是 postgres 写冲突。
3. **「英文准中文乱」是模型语言问题的标准指纹**，换个语言搜一次就能定位。
4. **三处靠读源码才查对**：`accel` 的位置、队列默认值、OCR 匹配方式。印象会骗人。
