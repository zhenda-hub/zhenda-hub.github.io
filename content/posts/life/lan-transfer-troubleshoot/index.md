+++
title = '局域网传大文件：从 1 MB/s 爬回 3.7 MB/s 的完整排障记录'
subtitle = ""
date = 2026-10-20T21:30:00+08:00
draft = false
toc = true
series = ['life']
tags = ['网络', 'Wi-Fi', 'Windows', '排障', '文件传输']
+++

[toc]

## 起因

两台 Windows 电脑在同一个局域网，要传一批 4K 视频，单个文件 12 GB 起。

打开浏览器下载，进度条稳稳地爬在 **600 KB/s**。算了一下：12 GB 要 **3 个半小时**。

这不是能不能等的问题——**同样两台机器，手机连同一个 Wi-Fi 下这个文件能跑 8 MB/s**。差 8 倍，说明某个环节坏了，只是不知道是哪个。

于是开始排障。整个过程花了大概两小时，最后爬回 **3.7 MB/s**（12 GB 约 55 分钟）。下面把方法、数据和踩过的坑都记下来。

## 先说结论

**瓶颈是"客户端的 USB 无线网卡 + 信道干扰 + 服务器摆放位置"三件事叠在一起，跟传文件的软件一点关系都没有。**

但一开始我不知道这些，所以走了不少弯路。真正有价值的不是最后的答案，而是**怎么一层层把嫌疑对象排除掉**的方法。

## 第一层：先排除软件

一开始想的是"用什么工具传最快",试了三条路：

| 方案 | 命令 | 断点续传 |
| --- | --- | --- |
| Python 标准库 | `python -m http.server 8000` | ❌ 不支持 Range |
| Python + 补丁包 | `pip install rangehttpserver` → `py -m RangeHTTPServer 8000` | ✅ |
| Node | `npx http-server . -p 8001 -a 0.0.0.0` | ✅ |

**`python -m http.server` 不支持断点续传**——它返回 `HTTP/1.0 200`，无视 `Range` 请求头，也不会发 `Accept-Ranges`。12 GB 下到 90% 断了，只能从头再来。这是标准库二十年没修的老毛病。

所以换成了 `rangehttpserver`，实测正常：

```
HTTP/1.0 206 Partial Content
Content-Range: bytes 100000-199999/300000
Accept-Ranges: bytes
```

结果两个服务**一样慢，都卡在 600 KB/s 左右**。这就有点意思了——两套完全独立的代码（Python 标准库 vs Node）、不同语言、不同 I/O 模型，怎么可能恰好卡在同一个数字上？

**两个独立实现给出同一个上限，说明上限在它们之外。**

## 第二层：把应用层整个摘掉

光"怀疑"不够，得测。写了个 40 行的裸 TCP 测速脚本，不解析 HTTP、不发响应头、不读文件，就是纯 socket 灌数据：

```python
#!/usr/bin/env python
# 8009 = 收（客户端发给我），8010 = 发（我发给客户端）
import socket, threading, time

CHUNK = 256 * 1024

def sink(conn, addr):
    total, t0 = 0, time.time()
    while time.time() - t0 < 15:
        d = conn.recv(CHUNK)
        if not d: break
        total += len(d)
    print(f'[上行] {addr[0]}: {total/1048576:.1f} MB = {total/(time.time()-t0)/1048576:.2f} MB/s')

def src(conn, addr):
    buf = bytes(CHUNK)
    total, t0 = 0, time.time()
    while time.time() - t0 < 15:
        conn.sendall(buf)
        total += len(buf)
    print(f'[下行] {addr[0]}: {total/1048576:.1f} MB = {total/(time.time()-t0)/1048576:.2f} MB/s')

def serve(port, handler):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port)); s.listen(8)
    while True:
        c, a = s.accept()
        threading.Thread(target=handler, args=(c, a), daemon=True).start()

threading.Thread(target=serve, args=(8009, sink), daemon=True).start()
serve(8010, src)
```

客户端那一侧只要一行 PowerShell（`iex(irm ...)` 拉下来直接跑，省得敲长命令）：

```powershell
iex(irm 192.168.10.7:8000/t.ps1)
```

结果：

```
[下行] 192.168.10.9: 4.8 MB / 5.2s = 0.93 MB/s
[上行] 192.168.10.9: 5.0 MB / 6.4s = 0.79 MB/s
```

**把两个软件全摘掉，还是 1 MB/s。** 到这里可以百分百确定：跟 HTTP、跟 Python、跟 Node、跟浏览器、跟代理都没关系。

顺手还做了一组对比——同样的服务，本机自己访问自己：

| 测试路径 | Python 8000 | npx 8001 |
| --- | --- | --- |
| 本机回环 127.0.0.1 | **1,255 MB/s** | **508 MB/s** |
| 从另一台机器进来 | 0.93 MB/s | 0.80 MB/s |

同一份代码，1000 倍的差距。**差异只可能来自中间那段路。**

## 第三层：找一个第三方设备做对照

现在知道问题在网络上，但还有两个嫌疑：服务器这端，还是客户端那端？

方法很土但有效：**拿手机连同一个 Wi-Fi，浏览器直接下同一个文件。**

结果 **8 MB/s**。

一句话定位：**服务器和 AP 都没问题，问题在客户端。**

## 开始修：一共四步，只有三步有效

### ① 换 USB 口（有效，但只翻了一倍）

查出来客户端用的是一块 `Wifi6 802.11ax USB Adapter`——外置 USB 无线网卡。原本插在**黑色口**（USB 2.0，480 Mbps 总线）上。

换到**蓝色口**（USB 3.0，5 Gbps）后：1.09 → 1.13 MB/s。后来又换了一次口，到 1.74 MB/s。

> 顺带纠正一个常见误解：网上说"USB 3.0 会干扰 2.4G Wi-Fi"，这是真的，但你的连接在 5GHz，完全不受影响。

### ② 关网卡省电 + 关闭漫游扫描（无效）

排障时要诚实记录失败尝试。当时观察到速度是**周期性一顿一顿的**，用 0.5 秒采样器看到：

```
下行 每 0.5 秒增量: 0.2, 0.8, 0.2, 0.6, 0.4, 0.6, 0.4, 0.6, 0.4, 0.6
```

如果是路由器限速（令牌桶），增量应该是均匀的 0.5/0.5/0.5。这种"0.2 → 0.8 → 0.2 → 0.6"的交替，典型是**收发端周期性停摆**，最像网卡省电休眠或者漫游扫描。

于是改了服务器网卡（MediaTek MT7921）两个驱动参数：

```powershell
Set-NetAdapterAdvancedProperty -Name 'Wi-Fi' -DisplayName 'Power Saving' -DisplayValue 'Disabled'
Set-NetAdapterAdvancedProperty -Name 'Wi-Fi' -DisplayName 'Roaming Aggressiveness' -DisplayValue '2. Lowest'
Restart-NetAdapter -Name 'Wi-Fi'
```

**结果：没变化**（0.91 → 0.74）。方向错了，记录在此，免得下次再走一遍。

### ③ 改信道：40 → 149（有效，涨 50%）

扫了一圈周围的 AP：

```
你的 AP  : 信道 40
邻居 AP  : 信道 44   信号 51%   ← 就压在你头上
邻居 AP  : 信道 44   信号 21%
```

信道 40 如果用 40MHz 带宽，占的就是 **36–48 一整块**，邻居正好在里面。同频共存 = 抢时隙 = 每帧都要重传。

登录光猫（`http://192.168.10.1`，中兴的移动定制机型），把 5GHz 信道从「自动」改成「手动 → 149」。

服务器侧的协商速率立刻变化：

| 指标 | 信道 40 | 信道 149 |
| --- | --- | --- |
| 接收速率 | 288.2 Mbps | **432.4 Mbps** |
| 传输速率 | 144 Mbps | **216 Mbps** |

实际吞吐 2.85 MB/s。

### ④ 挪服务器位置（效果最猛，涨 5.5 倍）

服务器是一台笔记本，Wi-Fi 信号只有 `-73 dBm`（-50 优秀 / -60 良好 / -70 边缘 / -80 不可用）。把机器往光猫方向挪了挪：

| 指标 | 挪之前 | 挪之后 |
| --- | --- | --- |
| 接收速率 | 432 Mbps | **1201 Mbps** |
| 传输速率 | 216 Mbps | **1201 Mbps** |
| 信号 | 60% | **89%** |
| 网卡链路 | 216 Mbps | **1.2 Gbps** |

1201 Mbps 是 802.11ax 2×2 在 80MHz 带宽下的顶格速率之一——**信号一好，AP 才肯给宽频宽**。

## 最终账本

| 阶段 | 下行 | 上行 | 服务器 PHY |
| --- | --- | --- | --- |
| 起点（USB 2.0 口 / 信道 40） | 1.09 | 1.32 | 288 / 144 |
| 换 USB 3.0 口 | 1.13 | 0.71 | 288 / 144 |
| 再换口 | 1.74 | 2.91 | 288 / 144 |
| 信道 40 → 149 | 2.85 | 4.03 | 432 / 216 |
| 挪服务器位置 | **3.70** | **4.58** | **1201 / 1201** |

12 GB 文件：**3.5 小时 → 约 55 分钟**。

## 附带的两个坑

### Python 3.15 的 `http.server` 默认只绑 IPv6

这个坑很隐蔽。跑 `py -m RangeHTTPServer 8000`，日志显示 `Serving HTTP on :: port 8000`，本机 `curl 127.0.0.1:8000` 正常，但**局域网 IPv4 客户端连不上**，返回 000。

加上 `-b 0.0.0.0` 就好了。`python -m http.server` 也一样。

```powershell
py -m RangeHTTPServer 8000 -b 0.0.0.0
```

### 视频点了不播——`moov` 在文件尾部

顺便查了为什么有的 mp4 在浏览器里点了只转圈。读了文件的 atom 结构：

```
off=0            ftyp      28 字节
off=28           mdat      12,994,089,594 字节   ← 视频数据
off=12994089622  moov      28,119,040 字节       ← 索引在最后
```

播放器必须先拿到 `moov`（索引）才能知道每帧位置。Safari/QuickTime 会主动请求文件尾部，**但 Chrome/Edge 从 0 字节开始顺序读**——12 GB 的文件等于要下完才能播。

解法：用 VLC 打开 URL（会自己取尾部，秒开），或者重新封装：

```powershell
ffmpeg -i 原文件.mp4 -c copy -movflags +faststart 新文件.mp4
```

另外 Chrome 不支持 `.mkv` 容器，即使里面是 H.264 也播不了；4K HEVC 还需要系统装 HEVC 视频扩展。

## 踩坑速查

| 现象 | 真实原因 | 解决 |
| --- | --- | --- |
| `ping` 100% 丢包 | Windows 防火墙默认拦 ICMP，不是网络不通 | 放行 `icmpv4:8,any`，或干脆无视 ping |
| 局域网连不上，本机正常 | Python 3.15 默认绑 `::`（纯 IPv6） | 加 `-b 0.0.0.0` |
| 下载断了要重头来 | `python -m http.server` 不支持 Range | 换 `rangehttpserver` 或 `npx http-server` |
| 两个服务都慢 | 说明瓶颈在应用层之外 | 用裸 TCP 测速排除软件 |
| Wi-Fi 速度周期性一顿一顿 | 省电休眠 / 漫游扫描 / 丢包重传 | 0.5 秒采样看增量形态，别猜 |
| 信号 60% 但速率上不去 | AP 不给宽频宽 | 挪位置到 89%，PHY 直接从 216 跳到 1201 |
| 网线口只有 10 Mbps | 网线某对线断了 / 水晶头氧化 | 换根 Cat5e，正常应该 1000 Mbps |
| USB 无线网卡特别慢 | 插在 USB 2.0 口 / 走 hub / 廉价芯片 | 换蓝色口，别用延长线和 hub |

## 总结

这次排障最值钱的不是"改了什么"，而是**怎么确定该改什么**。三条经验：

1. **先证明"是谁的锅"，再动手。** 本机回环 1.2 GB/s + 跨机 0.9 MB/s，一步就把软件排除了。同理，两个不同实现卡在同一个数字，本身就是"瓶颈不在这里"的证据。

2. **用最笨的对照实验。** 手机连同一个 Wi-Fi 下同一个文件，8 MB/s——直接判定服务器无罪。找一个第三方设备当参照物，比分析一百个参数都快。

3. **Wi-Fi 只有三个变量：信道、频宽、位置。** 参数调优（省电、漫游、802.11 模式）大多是心理安慰，真正有效的是**挑一个干净的信道** + **把设备挪到信号好的地方**。这次光"挪一下笔记本"就让协商速率翻了 5.5 倍。

另外一条更硬的结论：**如果经常在两台电脑之间搬大文件，别用 HTTP 服务，用 SMB + robocopy**：

```powershell
robocopy \\192.168.1.5\share D:\dest /E /J /MT:16 /R:2 /W:2
```

`/J` 是无缓冲 I/O，专为大文件准备；中断了重跑同一条命令就是续传。真要快，就插网线——千兆能跑 110 MB/s，比这次的 3.7 MB/s 快 30 倍，而且没有任何玄学。
