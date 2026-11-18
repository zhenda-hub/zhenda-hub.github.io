+++
title = 'Samba 传输速度只有 2 MB/s：真凶是 Ubuntu 出厂默认开着的 WiFi 省电'
description = "客户端 ping 网关 1 ms、ping 服务器 90 ms。从这一个 RTT 反推带宽，挖到 /etc/NetworkManager/conf.d 里一个没人改过的默认值。"
subtitle = "从 2 MB/s 到 30 MB/s"
date = 2026-11-18T15:40:00+08:00
draft = false
toc = false
series = ['nas']
tags = ['性能排查', 'Wi-Fi', '文件传输']
featureimage = "featured.webp"
+++

客户端 ping 网关 1 ms，ping 这台服务器 90 ms。同一个 Wi-Fi，多出来的 89 毫秒就是答案。

## 根因

`/etc/NetworkManager/conf.d/default-wifi-powersave-on.conf` 里写着 `wifi.powersave = 3`（强制省电）。

这文件属于 `network-manager` 包，mtime 还是 `2024-04-05 02:48:03`——Ubuntu 24.04 打包那一刻的时间。它从装机起就没被人改过，日志里一句抱怨都没有。

## 为什么慢在这 2 MB/s

单流 TCP 吞吐有个硬天花板：

```
吞吐 ≤ 窗口 / RTT
```

250 KB 窗口 ÷ 90 ms ≈ **2.8 MB/s**，和实测的 2 MB/s 严丝合缝。

而证据不在平均值，在波形：`min 1.7 ms / avg 25 ms`。网卡醒着 2 ms，睡着就白等 25 ms——**这是省电的指纹，带宽问题不会长这样。**

## 修

```bash
# 1. 改出厂默认值（先备份）
cp -a /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf{,.bak}
sed -i 's/powersave = 3/powersave = 2/' \
  /etc/NetworkManager/conf.d/default-wifi-powersave-on.conf

# 2. 字典序靠后的兜底（必须 zz-，不能是 99-）
printf '[connection]\nwifi.powersave = 2\n' \
  > /etc/NetworkManager/conf.d/zz-wifi-powersave-off.conf

# 3. 立即生效
iw dev wlp1s0 set power_save off
```

第 2 步的坑值得单说：`conf.d` 按文件名**字典序**读，后读的覆盖先读的。`'9'(0x39) < 'd'(0x64)`，所以 `99-xxx.conf` 排在 `default-` 前面，写了等于没写，还没有任何报错。

驱动层再补一刀防 ASPM 延迟尖峰：

```bash
echo 'options rtw89_pci disable_aspm_l1=1 disable_aspm_l1ss=1' \
  > /etc/modprobe.d/rtw89-latency.conf
```

## 结果

| 指标 | 修前 | 修后 |
| --- | --- | --- |
| 服务端 → 网关 | avg 25.4 ms | **1.11 ms** |
| 抖动 mdev | 10.4 ms | **0.19 ms** |
| 大文件上传 | **2 MB/s** | **30 MB/s** |

延迟一降到 1 ms，那条天花板自己消失了。

## 附：12 MB/s 不是没修好

客户端接着传了几十张照片，只有 12 MB/s。50 张 × 5 MB = 250 MB，按带宽算该 7 秒传完，实际 21 秒——**差的 14 秒是每张 280 ms 的元数据往返**（create/open/close 各要一趟）。同一个客户端传 1 GB 大文件是 30 MB/s。

**小文件慢和大文件快同时为真，它们量的不是一回事。** 想让照片传快点，最有效的不是改配置，是多选几个文件夹同时拖。

## 一句话

**慢的从来不是带宽，是那个没人动过的默认值。** 而"这是谁改的"，`dpkg -S` 加 `ls --time-style=full-iso` 就能问出来。
