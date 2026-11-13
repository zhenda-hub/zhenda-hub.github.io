+++
title = '告警本身也会骗人：NAS 的双层告警配置'
subtitle = "LastBackupDate 停在一年前、七十余次异常关机无人知晓，两件事都不是靠「能发邮件」解决的"
date = 2026-11-01T02:50:00+08:00
draft = false
toc = true
tags = ['监控告警', '硬盘健康']
series = ['nas']
featureimage = "featured.webp"
+++

这台 NAS 上有两个「看不见的故障」同时存在了几个月：

- Duplicati 的 `LastBackupDate` 停在一年前，看起来像**一年没备份成功**
- `smartctl` 显示系统盘有 **七十余次异常关机**，没有任何人收到过通知

前者是字段含义被误读，后者是根本没有硬件告警。

**告警的价值不是「能收到邮件」，而是「能识别真实故障」。** 而默认字段和默认配置都会骗人。

## 告警会骗人：LastBackupDate 不是「最后运行时间」

`LastBackupDate` 记录的是**最后一次创建备份版本的时间**，不是最后一次任务运行的时间。

源数据一年没变，就不会产生新版本，这个字段自然停在一年前。备份任务其实每天都在正常跑。

正确的判断方法是看日志里的两个字段：

| 字段 | 含义 |
| --- | --- |
| `ExaminedFiles` | 本次实际扫描了多少文件 |
| `AddedFiles` | 其中有多少是新增或变更 |

只要 `ExaminedFiles` 每天都是全量数字、`AddedFiles` 为 0，就说明「备份在正常跑，只是数据没变」——而不是「备份坏了」。

## 第一层：Duplicati 邮件（QQ 邮箱）

Duplicati 的 `send-mail` 模块本身不复杂，卡住的是 QQ 邮箱的认证。

写入配置后先直接测 SMTP 凭据，得到：

```
535 Login fail. Account is abnormal, service is not open,
    password is incorrect, login frequency limited
```

排查过程有价值：

| 做法 | 结果 |
| --- | --- |
| Python `smtplib` 自动协商认证方式 | QQ **直接断开连接**，没有任何错误码 |
| 手工走 `AUTH LOGIN` | 拿到明确的 535 |

**通用经验：服务器「主动断连」往往不是网络问题，而是它不想跟你多说话。换一种握手方式能逼出真实错误码。**

授权码格式全部正确（16 位小写字母、无空格、`From` 与账号一致），所以问题在账号侧——最终重新生成授权码解决。

配置项写全局默认，一次管所有任务：

```ini
--send-mail-to=xxx@qq.com
--send-mail-from=xxx@qq.com
--send-mail-url=smtps://smtp.qq.com:465
--send-mail-username=xxx@qq.com
--send-mail-password=<16位授权码>
--send-mail-level=Warning,Error
--send-mail-subject=[家庭NAS] Duplicati %OPERATIONNAME% - %PARSEDRESULT%
```

**验证不能省**：临时把 level 改成 `All`，跑一个最快的小任务，确认能收到邮件后，再改回 `Warning,Error`。不做这一步等于赌它能用。

## 第二层：smartd 硬盘监控

硬件故障是备份救不回来的场景，需要单独一条通道。

smartmontools 已经装了，但缺 `/usr/sbin/sendmail`——smartd 靠它发信。装 `msmtp-mta` 提供兼容层，SMTP 配置直接从 Duplicati 数据库里读，避免密码落进脚本或命令行历史。

```
# 系统盘 NVMe
/dev/nvme0 -d nvme -a -s (S/../.././03|L/../../6/04) -W 5,70,80 -m root -M daily

# 备份盘 SATA SSD
/dev/sda -a -o on -S on -s (S/../.././02|L/../../6/03) -W 5,60,70 -m root -M daily
```

| 参数 | 作用 |
| --- | --- |
| `-s (S/../.././03\|L/../../6/04)` | 每天 03 点短自检，每周六 04 点长自检 |
| `-M daily` | 每天最多一封，不会刷屏 |
| `-W 5,70,80` | 温度变化超过 5℃ 才记日志；警告阈值 70℃，临界 80℃ |

`-W` 的第一个参数设成 0 会让 smartd 每 30 分钟刷两行温度日志，把 journal 淹掉。

**一个 systemd 的坑**：

```
Failed to enable unit: Refusing to operate on alias name or linked unit file: smartd.service
```

Ubuntu 里 `smartd.service` 是 `smartmontools.service` 的别名（`Alias=smartd.service`），**对别名执行 enable 会被拒绝**。必须用真实单元名。

## 读出来的数据

| | NVMe 4 TB（系统盘） | SATA SSD 2 TB（备份盘） |
| --- | --- | --- |
| 总体健康 | PASSED | PASSED |
| 重分配扇区 | — | 0 |
| 待定扇区 | — | 0 |
| 介质完整性错误 | 0 | — |
| 备用块 | 100% | — |
| 已用寿命 | **2%** | — |
| 总写入量 | 十几 TB | 读不到 |
| 通电时间 | 约一万四千小时（1.6 年） | **3 小时** |
| **异常关机次数** | **七十余次** | — |

两个结论：

**系统盘还很年轻。** 1.6 年、十几 TB 写入、2% 磨损，按这个速率能用几十年。这块盘不是问题。

**七十余次异常关机是供电或使用方式的问题，不是硬盘的问题。** NVMe 有掉电保护，但这么多次反复经历「写入过程中突然断电」是累积风险，对 SQLite 和 PostgreSQL 危害更大——这台机器上跑着 Duplicati 的任务库和 immich 的 PostgreSQL。

**一台 7×24 运行的 NAS 应该配 UPS。** 300 块的 UPS 能让这个数字停止增长，优先级高于再加一块硬盘。

## 小结

1. `LastBackupDate` 是「最后创建版本时间」，不是「最后运行时间」。判断备份是否正常要看 `ExaminedFiles` 与 `AddedFiles`。
2. 应用层告警和硬件层告警是两条独立通道，缺任何一条都会留下盲区。
3. 告警配完必须实测一条真实消息，否则等于赌它能用。
4. 硬盘本身健康时，异常关机次数指向供电，不指向存储。
