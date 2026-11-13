+++
title = '一个索引器啃 21 万张照片 7 小时，根因是目录规划'
subtitle = "风扇高速转、四核 76℃ 的背后：GNOME 索引器在反复重试大量提取失败的图片"
date = 2026-11-01T03:00:00+08:00
draft = false
toc = true
tags = ['性能排查', '文件索引']
series = ['nas']
featureimage = "featured.webp"
+++

一台本来很安静的 N100 小机器（四核、16 GB 内存、4 TB NVMe、二十来个 Docker 容器），风扇开始持续高速转。

`ps` 一查就看到原因：**GNOME 的文件索引器已经连续满核跑了 7 小时 24 分。**

```
  PID   %CPU     ELAPSED  COMMAND
32788  127.3    07:24:03  tracker-miner-fs-3
```

温度能说明问题有多严重：

| | 索引器运行中 | 停掉之后 |
| --- | --- | --- |
| CPU 四核温度 | 76 / 76 / 76 / 75 ℃ | 59 / 59 / 59 / 60 ℃ |
| load average | 1.85 | 0.99 |

差了 17 度。风扇当然会叫。

## 为什么它跑不完

`tracker3 status` 显示 "Data is still being indexed, Estimated 55s left"——这句话它已经说了七个小时。

往下翻，是刷屏的失败记录：

```
Could not get any metadata for uri:'file:///home/zhenda/Documents/ds_ws/
immich-app/library/upload/.../e010306c-....JPG' and mime:'image/jpeg'
```

一共 **一千五百余条**。

原因很清楚：`~/Documents/ds_ws/immich-app/library` 里是二十余万张照片。索引器在提取图片元数据，大量文件提取失败，它就会反复重试，永远出不来。

## 根因：服务数据放在 ~/Documents 下

索引器本身没有 bug。真正的问题是**数据放错了地方**。

GNOME 把 `~/Documents` 当作「用户文档目录」，索引器、云同步工具、「备份我的文档」这类程序默认都会去啃它。几百 GB 的服务数据放在这里，等于给自己埋了个定时炸弹。

**症状在风扇和温度，根因在目录规划。** 如果只盯着「温度高」去清灰、换硅脂，永远找不到真正的原因。

## 处理：要堵四个地方

只 `systemctl stop` 不够，服务会被重新拉起。四个地方一起堵：

```bash
# 1. 停掉并屏蔽服务
systemctl --user stop tracker-miner-fs-3.service tracker-extract-3.service \
  tracker-miner-fs-control-3.service tracker-miner-rss-3.service
systemctl --user mask tracker-miner-fs-3.service tracker-extract-3.service \
  tracker-miner-fs-control-3.service tracker-miner-rss-3.service
```

**坑一：只 mask 主服务不够。** 还有一个 `tracker-miner-fs-control-3.service` 是 D-Bus 控制代理，任何程序请求索引都会通过它把 miner 拉起来。

**坑二：autostart 里的条目绕过 systemd。**

```ini
# /etc/xdg/autostart/tracker-miner-fs-3.desktop
Exec=/usr/libexec/tracker-miner-fs-3   ← 直接调二进制，mask 管不住
```

必须用用户级同名文件压掉：

```
~/.config/autostart/tracker-miner-fs-3.desktop → Hidden=true
```

**验证不能只看一眼**，要连续观察：

```bash
for i in 1 2 3 4 5 6; do sleep 10; pgrep -a tracker >/dev/null \
  && echo "[${i}0s] 复活了" || echo "[${i}0s] clean"; done
```

六次全部 clean 才算成功。

## 小结

1. **先看谁在吃 CPU，再谈温度。** 风扇响是结果，不是原因。
2. **服务数据不要放 `~/Documents`。** 这是 GNOME 语义上的「用户文档目录」，所有默认会啃文档的工具都会啃到它。
3. **禁用 systemd 服务要连 D-Bus 控制代理和 autostart 一起堵**，否则会被重新拉起。
4. **验证要连续多次观察**，单次 `pgrep` 说明不了问题。

这个系列的另外两篇分别处理备份与告警。
