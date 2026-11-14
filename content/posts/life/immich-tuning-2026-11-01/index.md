+++
title = 'immich 中文搜不到照片：默认 CLIP 模型只支持英文'
description = "中文搜「海边」全是无关照片，根因是默认加载的 CLIP 模型只有英文语料。换模型解决，附 4 核机器并发配置。"
subtitle = ""
date = 2026-11-01T23:10:00+08:00
draft = false
toc = true
series = ['life']
tags = ['immich', 'CLIP', '中文搜索']
featureimage = "featured.webp"
+++

中文搜「海边」出来一堆无关照片。不是索引没建好，不是中文分词有问题——**immich 默认加载的 CLIP 模型只支持英文**。

`ViT-B-32__openai` 是 2021 年的原始 CLIP，训练语料纯英文。中文查询传进去，输出的向量本身就没有意义，检索结果自然是随机的。

## 三秒自证

同一个词，英文搜 `beach` 准确，中文搜「海边」混乱——即可判定为模型语言问题，与索引、标签、数据库无关。不需要翻日志。

## 换模型

| 模型 | 中文 Recall | 单张耗时 | 维度 | 重建速度 |
| --- | --- | --- | --- | --- |
| nllb-clip-large-siglip | 79.7% | 75 ms | 768 | — |
| XLM-Roberta-Large-ViT-H-14 | 75.22% | 39 ms | 1024 | — |
| nllb-clip-base-siglip | 74.8% | 15 ms | 768 | 6.4 张/分 |
| **XLM-Roberta-Base-ViT-B-32** | 65.7% | 3.2 ms | 512 | **43.7 张/分** |

选最后一行：Recall 比最优模型低 14 个百分点，但全库重建 30 小时，对照组是 207 小时。

两个实施细节：

1. **维度不用手工改**。当前表是 `vector(512)`，nllb 系列是 768 维，immich 会自动执行 `ALTER`（日志中可见 `Updating database CLIP dimension size`）。
2. **慢 6.8 倍是可解释的**。nllb 输入 384px 对 224px（像素 2.9 倍），加 768 维索引（1.5 倍），理论 4.4 倍，实测 4.7 倍。

换完中文搜索可用。

## 顺带：上传慢

同一台机器上还有第二个问题：手机上传慢到每分钟 5 张。`load average 30.51`，4 核，CPU 空闲 0%——瓶颈在缩略图生成任务的并发，不在网络。

| 队列 | 原值 | immich 默认 | 改为 |
| --- | --- | --- | --- |
| `metadataExtraction` | 5 | 5 | **2** |
| `faceDetection` | 5 | 2 | 1 |
| `smartSearch` | 5 | 2 | 1 |
| `ocr` | 4 | 1 | 1 |

ML 容器只有 1 个 gunicorn worker，但内部开了 24 个线程（ONNX 为每个模型各建一套线程池），加 `OMP_NUM_THREADS=3` 后降到 18。

结果：缩略图 **5 张/分钟 → 54 张/分钟**，postgres 占用 **65% → 1.2%**。

**真正起作用的只有 `metadataExtraction` 从 5 降到 2**，其余三项是配合。降并发反而更快，省下的不是算力，是数据库写冲突——`load average 30.51` 而吞吐只有 5 张/分钟，就是线程互相抢占、postgres 卡在锁等待上的直接证据。

## 硬件转码：设备接了，开关没开

宿主机有 `/dev/dri/renderD128`，容器没传入。补齐：

```yaml
    devices: ["/dev/dri:/dev/dri"]
    group_add: ["44", "992"]     # 必须写数字 GID，写组名会报错
```

`ffmpeg.accel` 默认是 `Disabled`，还要在 **管理 → 设置 → 视频转码 → 硬件加速** 手动打开。这个配置项不在 `transcode` 下面，`transcode` 只是 `ffmpeg` 的内部字段。

## 4 核机器配置清单

| 项目 | 默认值 | 4 核建议 |
| --- | --- | --- |
| `metadataExtraction` 并发 | 5 | **2** |
| `faceDetection` 并发 | 2 | 1 |
| `smartSearch` 并发 | 2 | 1 |
| `OMP_NUM_THREADS` | 未设置 | **3** |
| 硬件转码设备 | 未传入 | `/dev/dri` |
| `ffmpeg.accel` | `Disabled` | 开启 |
| CLIP 模型 | `ViT-B-32__openai` | `XLM-Roberta-Base-ViT-B-32` |
