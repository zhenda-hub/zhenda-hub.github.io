+++
title = '备份和源数据在同一块盘上，等于没有备份'
subtitle = "数百 GB 搬离同盘、三层验证，以及 Duplicati 校验只抽样的真相"
date = 2026-11-01T02:40:00+08:00
draft = false
toc = true
tags = ['数据备份', '数据验证']
series = ['nas']
featureimage = "featured.webp"
+++

查 Duplicati 配置时发现，备份目标指向 `~/Documents/ds_ws/duplicati-app/backups`——和它要保护的源数据在同一块物理盘上。

整台机器只有一块 3.6 TB NVMe，根目录、服务数据、备份全在上面。

**硬盘挂了，数据和「备份」一起消失。**

这个「备份」唯一的作用是「误删了能找回来」，完全没有容灾价值。

## 先确认备份源到底包含什么

Duplicati 的备份目标是加密存储的（`enc-v1:`），看不到内容，但可以查数据库。

最容易犯的错是先看 compose：

```yaml
volumes:
  - ~/Documents/ds_ws:/source      # 宽挂载，看起来像把整个目录都备了
```

按这个推断「源包含目标」，是错的。实际查 `Duplicati-server.sqlite` 的 `Source` 表：

```bash
python3 -c "
import sqlite3
con = sqlite3.connect('file:Duplicati-server.sqlite?immutable=1', uri=True)
for r in con.execute('SELECT BackupID, Path FROM Source ORDER BY BackupID'):
    print(r)
"
```

结果：每个任务只备份特定子目录（`immich-app/library`、`jellyfin-app/media`），与备份目标目录是平行关系，没有嵌套。

**挂载范围不等于备份源范围。** 这两件事必须分开确认，否则会基于错误前提做判断。

## 迁移

硬件上插了一块 2 TB 的 M.2 2242 SATA SSD 到机器空着的 SATA 位。

```bash
# 1. 格式化：整盘 ext4，保留块比例从默认 5% 降到 1%
mkfs.ext4 -L backup -m 1 /dev/sda

# 2. 挂载（nofail：盘没插也能正常开机）
UUID=d475ad8a-...  /mnt/backup  ext4  defaults,nofail,x-systemd.device-timeout=10  0  2
```

两个参数不是随手写的：

| 参数 | 原因 |
| --- | --- |
| `-m 1` | ext4 默认给 root 保留 5% 空间。2 TB 的专用备份盘上这是 93 GB |
| `nofail` | 没有它，备份盘不在时系统会卡在启动阶段 |

挂载点先设成 `root:root` + `700`：盘没挂上时容器写不进去，备份会明确报错，而不是静默写进系统盘把根分区填满。

拷贝在一个小时内完成，吞吐稳定在 300 MB/s 以上。

## 三层验证

「rsync 没报错」不等于迁移成功。做了三层，从粗到细：

| 层级 | 方法 | 结果 |
| --- | --- | --- |
| 1. 数量 | 文件数与字节数与源完全一致 | 完全一致 |
| 2. 清单 | Duplicati 各任务数据库 `Remotevolume` 表的卷文件名，与磁盘实际文件做集合比对 | 零缺失、零多余 |
| 3. 内容 | 随机抽 6 个文件做 md5 比对 | 全部一致 |

第 2 层最有价值：它验证的不是「文件复制过去了」，而是「备份软件认为应该在的文件，确实都在」。

## 改一行配置

```yaml
volumes:
  - ./config:/config
  - /mnt/backup/duplicati:/backups     # 原来写的是 ./backups:/backups
  - ~/Documents/ds_ws:/source
```

容器内路径保持 `/backups` 不变，所以 Duplicati 数据库里记录的六个任务目标不需要任何改动。

当晚 22:00 的定时任务就在新盘上跑成功了，写入 8 个新卷。**这比任何人工验证都有说服力——它证明整条链路是通的。**

## 校验的真相：抽样不等于全量

迁移完做「校验文件」（Verify），日志里的关键字段：

```json
{"VerificationsActualLength": 3, "BytesDownloaded": 79912408}
```

**几百 GB 的备份，实际只校验了百 MB 量级。**

这是 Duplicati 的默认抽样策略：只验最新的 dlist、对应的 dindex、再加一个随机 dblock。它足以发现「文件损坏或丢失」，但不等于全量审计。

**「校验通过」≠「全部数据没问题」。** 这个区别要在出问题之前就知道。

## 小结

1. 备份能否容灾，第一个判断标准是**物理位置是否隔离**，不是备份软件是否在正常运行。
2. 确认备份范围要查数据库或实际清单，不能从 compose 的挂载范围推断。
3. 迁移验证至少三层：数量、软件视角的清单、内容抽样。
4. 校验结果要看清是抽样还是全量。

同一晚还处理了告警缺失与系统负载异常，见这个系列的另外两篇。
