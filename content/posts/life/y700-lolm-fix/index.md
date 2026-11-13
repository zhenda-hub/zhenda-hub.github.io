+++
title = 'Y700 四代玩英雄联盟手游卡顿：Unity 把线程绑死在 2 颗核上'
subtitle = "一条「难度档位」的线索锁定到 Unity 绑核，taskset 从 5.4% 异常帧恢复到 90 帧"
date = 2026-10-25T23:55:00+08:00
draft = false
toc = true
tags = ['性能排查', '线程调度', 'Android']
series = ['life']
featureimage = "featured.webp"
+++

联想拯救者 Y700 四代（TB322FC，骁龙 8 至尊版 / SM8750，16G 内存）玩英雄联盟手游「一卡一卡」。游戏内帧率显示 `56 / 57 / 58`，不是掉到 20 帧那种崩，而是持续的微抖。

决定性的线索来自机主：

> 人机难度设「不屈白银」及以下不卡，设「不屈白银」以上就卡。别的设备没有这个问题，只有 Y700 四代有。

这句话的价值有两层：

- **可精确复现的二值实验**——同一台机器、同一个游戏、同一个设置界面，只动一个难度档位，卡与不卡可任意切换。有开关才能做干净的 A/B。
- **「别的设备没有」**——范围被锁死在 Y700 四代的机型特性上，可以先排除游戏本身的优化问题、网络问题、服务器问题。

顺这条线查下去，根因一句话：**Unity 把游戏的 10 条关键线程绑死在 cpu6 / cpu7 两颗核上。**

这台机器 8 颗核中只有这 2 颗能跑到 4.32 GHz，另外 6 颗是 3.53 GHz。高难度局的主线程负载一上来，2 颗核塞不下，渲染线程被饿到一次睡 216 毫秒——这才是机主说的「一卡一卡」。

一条 `taskset` 之后：**48–58 fps → 90.8 fps，200ms 级冻结 5 次 → 0 次。**

## 先给修复

```bash
PID=$(pidof com.tencent.lolm)
taskset -a -p ff $PID
```

- `-a` 表示应用到该进程的所有线程，`ff` 是掩码（bit0 ~ bit7 全开）
- 实测 30 秒内零反弹，系统不会改回去

| 指标 | 修复前 | 修复后 |
| --- | --- | --- |
| 帧率 | 48–58 fps | **90.8 fps** |
| 异常帧 | 5.4% | 0.11%（2 / 1806） |
| 200ms 级冻结 | 5 次 | 0 次 |

注意：不同 SoC 的核心数不同，`ff` 只对应 8 核全开，核数不同的机型要改掩码。这个改动只影响线程调度范围，不改变频率策略，属于可逆操作。

## 三条命令确认是不是同一个问题

```bash
# 1. 看游戏的线程被限制在哪些核上
PID=$(pidof com.tencent.lolm)
for t in /proc/$PID/task/*; do
  echo "$(cat $t/comm) $(grep Cpus_allowed_list $t/status)"
done | sort | uniq -c

# 2. 如果大量线程是 6-7 这种窄范围，手动放开
taskset -a -p ff $PID

# 3. 再打一局，对比手感
```

如果大量线程的允许核心是 `6-7` 这种窄范围，即为同一问题。

## 为什么只有高难度局才卡

难度档位提供了精确的开关，就能做干净的 A/B：同一台机器，只动难度。

| 场景 | 结果 |
| --- | --- |
| 高难度 + 绑 2 核 | 48–58 fps，5.4% 异常帧 |
| **白银 + 绑 2 核** | **60 fps，0 异常帧** |

同一台机器、同样的绑核、同样的两颗核，白银局就是不卡。

白银局场上单位少、AI 逻辑轻，2 颗核塞得下；高难度局主线程负载上升后，2 颗核不够，10 条线程开始互相抢占，渲染线程被饿到睡 200 毫秒。

**这个 bug 一直存在，只是没超载时看不出来。**

同一台机器只动难度，两组数据的差异：

| 指标 | 白银（稳 60） | 高难度（56–58） |
| --- | --- | --- |
| Unity 线程调度总次数 | 15,933 | **30,055（2 倍）** |
| 渲染线程切出次数 | 5,532 | **13,725（2.5 倍）** |
| 主线程切出次数 | 2,814 | **12,815（4.6 倍）** |
| >20 ms 长睡眠 | **0 次** | **19 次，最长 216 ms** |
| 渲染线程所在 CPU | 集中在 cpu7 | **cpu6 / cpu7 均匀劈开互抢** |

白银局一次长睡眠都没有。

## 证据：不是联想的软件干的

读线程亲和性，结论直接：

```
24275 UnityMain        → 允许的核：6-7
24320 UnityGfxDeviceW  → 允许的核：6-7
24339 UnityGfxDeviceW  → 允许的核：6-7
...（共 7 条 UnityMain + 3 条渲染线程）
整个游戏进程           → 允许的核：0-7
```

进程有全部 8 核的权限，但这 10 条关键线程被单独限制成 `6-7`。查全部 195 条线程：

```
Unity 线程   ：全部 6-7
其他线程     ：80 条也被绑 6-7
   含 tgpa_MainHandler / tgpa_SubHandler   ← 腾讯 TGPA（大小核绑定）
      Shark-Looper / APM-* / kcsdk_core    ← 腾讯网络与性能 SDK
      TCP-SendHandler / CodecLooper        ← 网络与解码
```

排除联想的软件的三条证据：

1. 联想的性能配置表 `/data/data/com.zui.tassistent/files/gameperfconfig.xml`（160 KB）中搜不到任何 `core` / `cpus` / `affinity` 字段，全是频率档位和帧率调整
2. 禁用联想两个游戏服务后，卡顿反而更严重：禁用 `com.zui.game.service` 后长睡眠从 19 次升到 36 次、最长 301 ms；禁用 `com.zui.tassistent` 后 GPU 被钉死在 389 MHz
3. 社区已有同款记录。GitHub 上的 `UnityFix` 模块说明写得很直接：

> Unity app incorrectly sets cpu affinity to max capacity cores.

该模块的改善游戏清单里明确列着 League of Legends: Wild Rift。

机制是：Unity 读各核的 `cpuinfo_max_freq`，只认最高那一档，把所有线程绑过去。Y700 四代的频率分布：

```
cpu6 / cpu7  →  4.32 GHz   ← 只有 2 颗
cpu0 ~ cpu5  →  3.53 GHz   ← 差 22%
```

于是 Unity 判定「高性能核 = 2 颗」，10 条线程全挤上去。腾讯 TGPA 再补一刀，把网络、解码、APM 那些线程也钉住。

### 根因的两个条件

这里需要说准确：不是这台机器的 CPU 设计有缺陷，也不是联想的软件在捣乱。问题是**两个条件同时成立**：

1. **Unity 的绑核启发式有缺陷**——只按 `cpuinfo_max_freq` 选核，认定最高频的核心就是唯一最优选择，把线程全部绑过去
2. **这台的频率分档让缺陷致命**——最高频档只有 2 颗核

| | 典型 big.LITTLE（如 1+3+4） | Y700 四代（SM8750，2+6 全大核） |
| --- | --- | --- |
| 最高频档核数 | 1 颗超大核 + 3 颗大核 | **只有 2 颗**（4.32 GHz） |
| 次档核 | 4 颗 3.53 GHz（较弱） | 6 颗 3.53 GHz（**只差 22%**） |
| Unity 绑过去后剩下 | 挤 1 颗，但同簇还有 3 颗可用 | **只剩 2 颗可用** |

在典型的 big.LITTLE 机器上，同样的启发式错误不会致命——线程挤到 1 颗超大核后，同簇的大核仍然可用。而这台是 2+6 全大核设计，最高频档只有 2 颗、次档只差 22%，Unity 把 10 条关键线程全绑到这 2 颗上，剩下的 6 颗哪怕只差 22% 也用不上。

**换句话说：Unity 的缺陷一直存在，但这台的频率分档把它从「不痛不痒」放成了「直接卡死」。**

> 这也是为什么这个 bug 不限于 Y700 四代：凡是最高频核只有 2 颗的机型，都可能触发同样的行为。

## 反直觉之处：性能富余到荒谬

前面所有指标都在看「够不够快」，直到读到这一个字段：

```
averageFrameDuration = 0.077 ms
```

SurfaceFlinger 统计的应用帧生成耗时是 **0.077 毫秒**。77 微秒。

这台机器渲染一帧毫无压力。CPU 占用只有 24%，另外 6 颗核全程闲着。那么 200 ms 的冻结只可能是**在等什么东西**。

抓线程调度后，问题立刻现形：

```
UnityGfxDeviceW（渲染线程）在 12 秒里
  睡眠超过 20ms 的次数：19 次
  最长一次：216 毫秒
```

最长那次的线程状态是 `S`（可中断睡眠）——不是被抢占，是主动睡下去等人。

同时有一个极反常的数字：`UnityGfxDeviceW` 和 `UnityMain` 在同一颗 CPU 上**每秒互相切出 / 切入约 1000 次**。

**瓶颈从来不是「算力不够」，是「路被人为堵死了」。**

## 固化成 Magisk 模块

`taskset` 是运行时内存操作，游戏一重启就会失效——新线程又被绑回 `6-7`。需要常驻守护。

最终脚本 15 行：

```bash
#!/system/bin/sh
PKG=com.tencent.lolm
MASK=ff                 # cpu0-7
SLEEP=5                 # 轮询间隔

echo $$ > /data/local/tmp/lolm_affinity.pid

while true; do
  pid=$(pidof "$PKG" 2>/dev/null | awk '{print $1}')
  if [ -n "$pid" ]; then
    taskset -a -p "$MASK" "$pid" >/dev/null 2>&1
  fi
  sleep $SLEEP
done
```

设计上刻意做了减法：

- **不做状态判断**，游戏在跑就无条件刷一次，宁可多刷几次也不漏
- 刷成**相同的掩码**在内核里会直接返回，几乎零成本
- **不碰**联想任何服务、系统分区、游戏文件、频率策略

实测开销：

| 场景 | 单核占用 |
| --- | --- |
| 待机（游戏未运行） | 0.05%（一小时耗 1.8 秒 CPU） |
| 游戏进行中 | < 0.3% |

模块结构：

```
/data/adb/modules/lolm_affinity_fix/
├── module.prop
├── service.sh                    # 开机启动守护
└── tools/lolm_affinity.sh        # 上面那 15 行
```

验证：手动把一条线程改回 `6-7`，守护 5 秒内自动修回。

## 野兽模式还要不要开

要，两者解决的是不同问题：

| | 绑核修复 | 野兽模式 |
| --- | --- | --- |
| 解决什么 | 线程挤在 2 核上互抢 | CPU / GPU 频率上限 |
| 均衡模式 | — | cpu7 上限 1.96~2.84 GHz，GPU 389~607 MHz |
| 野兽模式 | — | cpu7 **4.32 GHz**，GPU **1100 MHz** |

Unity 主线程是单线程的——8 个核再多，主线程也只用一颗。所以：

- 绑核修复给它腾地方（不挤在 2 个核上）
- 野兽模式决定那颗核跑多快（2.84 GHz 还是 4.32 GHz，差 34%）

## 附录一：两支被证伪的误判

### 一个每 5 秒崩溃一次的服务

日志中 `vendor.qti.qvirt-service_rs` **精确每 5.00 秒崩溃一次**，2 分钟崩 25 次，累计 296 次，间隔稳定在 4.999~5.007 秒。根因也挖到了：

```
/product/bin/vendor.qti.qvirt-service_rs   ← 64 位 Rust 程序，在 product 分区
    需要 liblogger.dylib.so
    product 命名空间是隔离的，只能看 /product/lib64
    而这个库只在 /system/lib64 和 configinfrastructure APEX 里
    → 链接失败 → 崩溃 → init 5 秒后重新拉起 → 无限循环
```

缺的不止一个库：整套 Rust 依赖 13 个库，`/product/lib64` 里只有 2 个文件，其中 `libserde_json.dylib.so` 全系统不存在。这是永远修不好的固件打包 bug。

**但它不是卡顿元凶**：

- 每次崩溃是「拉起进程 → 链接器失败 → 毫秒级退出」，CPU 占用约 0.2%
- 卡顿是单帧冻结 200 ms
- 时间窗口密度检验：崩溃时刻前后 1 秒内，游戏日志密度只有随机期望的 **1.2 倍**，等于无相关性

> 找到 bug ≠ 找到正在查的那个 bug。必须做相关性检验，不能因为两件事都「大约每几秒一次」就下结论。

### CPU / GPU 频率在横跳

| 采样时刻 | GPU 频率 | cpu7 上限 |
| --- | --- | --- |
| t0 | 607 MHz | 1.96 GHz |
| t1 | **389 MHz** | 1.96 GHz |
| t2 | 607 MHz | **2.84 GHz** |
| t5 | **389 MHz** | 1.96 GHz |

GPU 满血 1100 MHz，实际在 389 ↔ 607 MHz 之间跳；CPU 超大核在 1.96 ↔ 2.84 GHz 之间跳。写这个策略的进程是 `com.zui.tassistent`（日志中 `TGAME/GameManager: updatePerfPolicy` 每 1.17 秒刷一次）。

分别禁用测试后结论是：**频率振荡是噪音，不是原因。而且禁用联想服务只会更糟。** 这个结论后来很重要——它说明绑核的不是联想的软件。

## 附录二：测量口径

没有测量就没有结论。全程用 adb + 已 root 的设备，三个观测面：

```bash
# 1. 帧时间分布（SurfaceFlinger 的 presentToPresent 直方图）
adb shell dumpsys SurfaceFlinger --timestats -clear
# ...等 20 秒...
adb shell dumpsys SurfaceFlinger --timestats -dump

# 2. 线程调度（ftrace，过滤到游戏的线程）
echo 'prev_comm ~ "Unity*" || next_comm ~ "Unity*"' > \
  /sys/kernel/tracing/events/sched/sched_switch/filter

# 3. 内核阻塞原因
echo 1 > /sys/kernel/tracing/events/sched/sched_blocked_reason/enable
```

基线：

```
6672 帧 / 123 秒
超时帧 359 个（5.4%）
其中 200ms 级冻结 5 次
```

平均帧率不算低，但每 4~5 秒就有一次 200 毫秒的整帧冻结。

已排除的常规原因：

| 怀疑项 | 实测数据 | 结论 |
| --- | --- | --- |
| CPU 性能不足 | 卡的时候 CPU 上限 2.84 GHz，不卡的时候反而只有 1.96 GHz | 反证 |
| 温控降频 | 芯片 49~61°C，电池 26.5~30°C，热状态 = 0 | 排除 |
| 内存不足 | 可用内存 2.7~2.9 GB，Swap 空闲 9.9 GB | 排除 |
| 后台应用抢资源 | 两次测量的后台进程完全一致，PID 都没变 | 排除 |
| 存储性能 | 136 GB 空余 | 排除 |
| 屏幕刷新率 | 60 Hz 改 165 Hz 后依然卡 | 排除 |

## 这次排查踩过的坑

1. **`MemFree` ≠ `MemAvailable`**。前者几乎永远是几百 MB，不能用来判断内存不足。这次看到 `MemFree: 142M` 差点误判，实际 `MemAvailable` 是 2.9 GB。
2. **找到 bug 不等于找到这个 bug**，必须做相关性检验。崩溃循环的时间窗口密度富集只有 1.2 倍。
3. **测量本身会污染测量**。边测边截 3040×1904 的截图，截图本身就吃资源。
4. **禁用厂商服务前先确认它管什么**。这次禁用后 GPU 直接被钉在 389 MHz，比原来更差。
5. **200 ms 这个数字差点带偏方向**。它和 TCP 初始重传超时 RTO 完全一样，一度怀疑是网络，最后靠 `averageFrameDuration = 0.077 ms` 才把方向拽回来。
6. **最反直觉的一点**：CPU 占用只有 24%，6 颗核全程闲置，帧生成只要 77 微秒，却卡得要命。

## 参考

- [LeanxModulostk/UnityFix](https://github.com/LeanxModulostk/UnityFix) —— 同款问题的另一个思路（伪装各核最高频率一致，从源头阻止 Unity 绑核）
- [cinitdev/AppOpt](https://github.com/cinitdev/AppOpt) —— 规则化的按包名 / 线程名配置亲和性
- [Android 官方：分析线程调度](https://developer.android.com/agi/sys-trace/threads-scheduling)
