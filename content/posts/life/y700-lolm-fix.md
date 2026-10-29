+++
title = '拯救者 Y700 四代玩英雄联盟手游一卡一卡：完整排查复盘'
subtitle = "从 5.4% 异常帧到 90 帧，根因是被绑死在两颗核上"
date = 2026-10-25T23:55:00+08:00
draft = false
toc = true
tags = ['Android', '性能排查', 'Y700', 'Magisk']
series = ['life']
+++

## 症状：一个可精确复现的卡顿

联想拯救者 Y700 四代（TB322FC，骁龙 8 至尊版 / SM8750，16G 内存），玩英雄联盟手游「一卡一卡」。

最关键的线索来自机主的一句话：

> 人机难度设「不屈白银」及以下不卡，设「不屈白银」以上就卡。别的设备没有这问题，只有 Y700 四代有。

这句话把排查范围从「玄学卡顿」压缩成了一个**可精确复现的二值实验**：同一台机器、同一个游戏、同一个设置界面，只动一个难度档位，卡和不卡可以任意切换。

游戏内 FPS 显示 `56 / 57 / 58`，不是掉到 20 帧那种崩，而是**稳定的微抖**。

## 先建立测量口径

没有测量就没有结论。全程用 adb + 已 root 的设备，主要三个观测面：

```bash
# 1. 帧时间分布（SurfaceFlinger 的 presentToPresent 直方图）
adb shell dumpsys SurfaceFlinger --timestats -clear
# ...等 20 秒...
adb shell dumpsys SurfaceFlinger --timestats -dump

# 2. 线程调度（ftrace，过滤到游戏的线程）
echo 'prev_comm ~ "Unity*" || next_comm ~ "Unity*"' > \
  /sys/kernel/tracing/events/sched/sched_switch/filter

# 3. 内核阻塞原因（这一项后面救了整场排查）
echo 1 > /sys/kernel/tracing/events/sched/sched_blocked_reason/enable
```

第一次测出来的基线：

```
6672 帧 / 123 秒
超时帧 359 个（5.4%）
其中 200ms 级冻结 5 次
```

**平均帧率不算低，但每 4~5 秒就有一次 200 毫秒的整帧冻结**——这才是机主说的「一卡一卡」。

## 第一轮：把常规嫌疑人全部排除

| 怀疑项 | 实测数据 | 结论 |
|---|---|---|
| CPU 性能不足 | 卡的时候 CPU 上限 2.84GHz，不卡的时候反而只有 1.96GHz | ❌ 反证 |
| 温控降频 | 芯片 49~61°C，电池 26.5~30°C，热状态 = 0 | ❌ |
| 内存不足 | 可用内存 2.7~2.9GB，Swap 空闲 9.9GB | ❌ |
| 后台应用抢资源 | 两次测量的后台进程完全一致，PID 都没变 | ❌ |
| 存储性能 | 136GB 空余 | ❌ |
| 屏幕刷新率 | 60Hz 改 165Hz 后依然卡 | ❌ |

这里有个坑值得记一笔：一开始我看到 `MemFree: 142M` 就差点判定「内存耗尽」，实际上 `MemAvailable` 是 2.9GB。**`MemFree` 和 `MemAvailable` 是两个完全不同的东西**，前者几乎永远很小。

## 第二轮：两次误判，以及怎么证伪

### 误判一：一个每 5 秒崩溃一次的服务

日志里发现 `vendor.qti.qvirt-service_rs` **精确每 5.00 秒崩溃一次**，2 分钟崩了 25 次，累计 296 次。间隔稳定在 4.999~5.007 秒之间。

根因也挖到了：

```
/product/bin/vendor.qti.qvirt-service_rs   ← 64 位 Rust 程序，在 product 分区
    需要 liblogger.dylib.so
    product 命名空间是隔离的，只能看 /product/lib64
    而这个库只在 /system/lib64 和 configinfrastructure APEX 里
    → 链接失败 → 崩溃 → init 5 秒后重新拉起 → 无限循环
```

而且缺的不止一个库，整套 Rust 依赖 13 个库，`/product/lib64` 里只有 2 个文件，其中 `libserde_json.dylib.so` **全系统不存在**。这是个永远修不好的固件打包 bug。

**但它不是卡顿元凶。** 证伪方法很简单：

- 每次崩溃是「拉起进程 → 链接器失败 → 毫秒级退出」，CPU 占用约 0.2%
- 而卡顿是单帧冻结 200 毫秒
- 统计检验：崩溃时刻前后 1 秒内，游戏日志的密度只有随机期望的 **1.2 倍**（等于没有相关性）

> 教训：找到 bug ≠ 找到你正在查的那个 bug。**必须做相关性检验，不能因为两件事都"大约每几秒一次"就下结论。**

### 误判二：CPU/GPU 频率在横跳

采样发现频率在上限之间反复跳：

| 采样时刻 | GPU 频率 | cpu7 上限 |
|---|---|---|
| t0 | 607 MHz | 1.96 GHz |
| t1 | **389 MHz** | 1.96 GHz |
| t2 | 607 MHz | **2.84 GHz** |
| t5 | **389 MHz** | 1.96 GHz |

GPU 满血 1100MHz，实际在 389↔607MHz 之间跳；CPU 超大核在 1.96↔2.84GHz 之间跳。定位到写这个策略的进程是 `com.zui.tassistent`（日志里 `TGAME/GameManager: updatePerfPolicy` 每 1.17 秒刷一次）。

于是我把联想这两个游戏相关服务分别禁用测试：

```
禁用 com.zui.game.service  →  长睡眠 19 次 → 36 次，最长 301ms（更差）
禁用 com.zui.tassistent    →  GPU 被钉死在 389MHz（彻底不给升频）
```

**结论：频率振荡是噪音，不是原因。而且禁用联想服务只会更糟。** 这个结论后来非常重要——它说明绑核的不是联想。

## 转折点：换个指标，发现它在「睡」而不是在「算」

前面所有指标都在看「够不够快」。直到读了这一个字段：

```
averageFrameDuration = 0.077 ms
```

SurfaceFlinger 统计的**应用帧生成耗时**是 **0.077 毫秒**。77 微秒。

这台机器渲染一帧毫无压力，性能富余到荒谬。那么 200ms 的冻结只可能是——**它在等什么东西**。

换成抓线程调度，问题立刻现形：

```
UnityGfxDeviceW（渲染线程）在 12 秒里
  睡得超过 20ms 的次数：19 次
  最长一次：216 毫秒
```

而其中最长的那次，线程状态是 `S`（可中断睡眠）——它不是被抢占，是主动睡下去等人。

同时看到一个极其反常的数字：`UnityGfxDeviceW` 和 `UnityMain` 在同一颗 CPU 上**每秒互相切出/切入约 1000 次**。

## 决定性实验：白银 vs 高难度

有了精确的开关，就能做干净的 A/B。同一台机器，只动难度：

| 指标 | 白银（不卡，稳 60） | 高难度（卡，56-58） |
|---|---|---|
| Unity 线程调度总次数 | 15,933 | **30,055（2 倍）** |
| 渲染线程切出次数 | 5,532 | **13,725（2.5 倍）** |
| 主线程切出次数 | 2,814 | **12,815（4.6 倍）** |
| **>20ms 长睡眠** | **0 次** | **19 次，最长 216ms** |
| 渲染线程所在 CPU | 集中在 cpu7 | **cpu6/cpu7 均匀劈开互相抢** |

白银局**一次长睡眠都没有**。

## 根因：所有线程被绑死在两颗核上

读线程亲和性，一句话就说完了：

```
24275 UnityMain        → 允许的核：6-7
24320 UnityGfxDeviceW  → 允许的核：6-7
24339 UnityGfxDeviceW  → 允许的核：6-7
...（共 7 条 UnityMain + 3 条渲染线程）
整个游戏进程           → 允许的核：0-7
```

进程有 8 个核的权限，但这 10 条关键线程被单独限制成 `6-7`——**只有两颗核可用**。

再查全部 195 条线程：

```
Unity 线程   ：全部 6-7
其他线程     ：80 条也被绑 6-7
   含 tgpa_MainHandler / tgpa_SubHandler   ← 腾讯 TGPA（大小核绑定）
      Shark-Looper / APM-* / kcsdk_core    ← 腾讯网络与性能 SDK
      TCP-SendHandler / CodecLooper        ← 网络与解码
```

**谁干的？** 不是联想。证据有三条：

1. 联想的性能配置表 `/data/data/com.zui.tassistent/files/gameperfconfig.xml`（160KB）里，**搜不到任何 `core` / `cpus` / `affinity` 字段**，全是频率档位和帧率调整
2. 禁用联想两个服务后，卡顿反而更严重
3. 社区里早有同款记录：GitHub 上的 `UnityFix` 模块说明写得很直白：

> Unity app incorrectly sets cpu affinity to max capacity cores.
> （Unity 会错误地把 CPU 亲和性设置到「最大容量核心」上）

而这个模块的改善游戏清单里，**明确列着 League of Legends: Wild Rift**。

机制就是：Unity 读各核 `cpuinfo_max_freq`，只认最高那一档，把所有线程绑过去。Y700 四代的频率分布是这样的：

```
cpu6 / cpu7  →  4.32 GHz   ← 只有 2 颗
cpu0 ~ cpu5  →  3.53 GHz   ← 差 22%
```

于是 Unity 判定「高性能核 = 2 颗」，10 条线程全挤上去。腾讯 TGPA 又补了一刀，把网络、解码、APM 那些线程也钉住。

## 为什么只有高难度才卡

这是整件事最关键的一环，也是为什么之前所有排查都走偏：

| 场景 | 结果 |
|---|---|
| 高难度 + 绑 2 核 | 48~58 帧，5.4% 异常帧 |
| **白银 + 绑 2 核** | **60 帧，0 异常帧** |

**同一台机器、同样的绑核、同样的两颗核——白银局就是不卡。**

因为白银局场上单位少、AI 逻辑轻，2 颗核塞得下；高难度局主线程活一多，2 颗核立刻不够，10 条线程开始互相抢占，渲染线程被饿到睡 200 毫秒。

也就是说这个 bug **一直存在，只是没超载时看不出来**。

## 修复：一条命令

```bash
# 把游戏所有线程的亲和性恢复成全部 8 核
taskset -a -p ff <游戏PID>
```

`-a` 是「应用到该进程的所有线程」，`ff` 是掩码（bit0~bit7 全开）。改完立刻复查，系统不会改回去（实测 30 秒内零反弹）。

效果：

```
修复前：48-58 fps，5.4% 异常帧，5 次 200ms 冻结
修复后：90.8 fps，2/1806 异常帧（0.11%）
```

## 固化成 Magisk 模块

`taskset` 是运行时的内存操作，**游戏一重启就会失效**——新线程又被绑回 `6-7`。所以需要一个常驻守护。

最终版脚本精简到 15 行：

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

- **不做状态判断**，游戏在跑就无条件刷一次。宁可多刷几次也不漏
- 刷成**相同的掩码**在内核里会直接返回，几乎零成本
- **不碰**联想任何服务、系统分区、游戏文件、频率策略

实测开销：

| 场景 | 单核占用 |
|---|---|
| 待机（游戏未运行） | 0.05%（一小时耗 1.8 秒 CPU） |
| 游戏进行中 | < 0.3% |

模块结构：

```
/data/adb/modules/lolm_affinity_fix/
├── module.prop
├── service.sh                    # 开机启动守护
└── tools/lolm_affinity.sh        # 上面那 15 行
```

同时验证过：手动把一条线程改回 `6-7`，守护 **5 秒内自动修回**。

## 野兽模式还要不要开

要，两者解决的是不同问题：

| | 绑核修复 | 野兽模式 |
|---|---|---|
| 解决什么 | 线程挤在 2 核上互抢 | CPU/GPU 频率上限 |
| 均衡模式 | — | cpu7 上限 1.96~2.84GHz，GPU 389~607MHz |
| 野兽模式 | — | cpu7 **4.32GHz**，GPU **1100MHz** |

Unity 主线程是**单线程**的——8 个核再多，主线程也只用一颗。所以：

- 绑核修复给它腾地方（不挤在 2 个核上）
- 野兽模式决定那颗核跑多快（2.84GHz 还是 4.32GHz，差 34%）

## 这次排查踩过的坑

1. **`MemFree` ≠ `MemAvailable`**，前者几乎永远是几百 MB，别拿它判断内存不足
2. **找到 bug 不等于找到这个 bug**，必须做相关性检验（我们对崩溃循环做了时间窗口密度检验，富集只有 1.2 倍）
3. **测量本身会污染测量**——边测边截 3040×1904 的截图，截图本身就吃资源
4. **禁用厂商服务前先想清楚它管什么**，这次禁用后 GPU 直接被钉在 389MHz，比原来更差
5. **200ms 这个数字差点带偏方向**——它和 TCP 初始重传超时 RTO 完全一样，我一度怀疑是网络。后来靠 `averageFrameDuration = 0.077ms` 才把方向拽回来
6. **最反直觉的一点**：CPU 占用只有 24%，另外 6 颗核全程闲着，帧生成只要 77 微秒——**性能富余到荒谬，却卡得要命**。因为瓶颈从来不是"算力不够"，是"路被人为堵死了"

## 如果你也遇到

先确认是不是同一个问题，三条命令：

```bash
# 1. 看游戏的线程被限制在哪些核上
PID=$(pidof com.tencent.lolm)
for t in /proc/$PID/task/*; do
  echo "$(cat $t/comm) $(grep Cpus_allowed_list $t/status)"
done | sort | uniq -c

# 2. 如果大量线程是 6-7 这种窄范围，试着手动放开
taskset -a -p ff $PID

# 3. 再打一局，对比手感
```

如果有效，再考虑固化成模块。

> 注意：不同 SoC 的核心编号和高频核数量不一样，`ff` 对应 8 核全开，核数不同的机型要改掩码。另外这个改动只影响线程调度范围，不改变频率策略，属于可逆操作。

## 参考

- [LeanxModulostk/UnityFix](https://github.com/LeanxModulostk/UnityFix) —— 同款问题的另一个思路（伪装各核最高频率一致，从源头阻止 Unity 绑核）
- [cinitdev/AppOpt](https://github.com/cinitdev/AppOpt) —— 规则化的按包名/线程名配置亲和性
- [Android 官方：分析线程调度](https://developer.android.com/agi/sys-trace/threads-scheduling)
