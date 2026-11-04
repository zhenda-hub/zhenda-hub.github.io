+++
title = '本来只想让风扇安静点：一台家用 NAS 的一夜整改'
description = "从风扇噪音开始的完整排障：一个满核跑 7 小时的索引器、413 GB 备份迁移、Duplicati 与 smartd 告警配置、光猫下发的公网 IPv6 暴露、Samba 家庭共享，以及两个我判断错了的地方。"
subtitle = ""
date = 2026-11-01T02:40:00+08:00
draft = false
toc = true
series = ['life']
tags = ['NAS', 'Linux', 'Docker', '备份', '网络', '排障']
+++

[toc]

## 起因

晚上十点，书房里那台 GMKtec NucBox G3 Plus 的风扇一直在高速转。

这台机器平时很安静——N100 四核、16 GB 内存、一块 4 TB NVMe，跑着二十来个 Docker 容器：immich 存全家照片、Jellyfin 放电影、Navidrome 听歌，还有一堆下载和管理工具。它应该是个安静的背景存在，而不该让人注意到它。

结果这一晚从"为什么这么吵"开始，一路挖出了备份策略的漏洞、一个公网暴露的安全问题，以及七八个配置不当的地方。

下面是完整的排查和整改记录。

---

## 一、噪音：一个索引器吃满了一个核心

第一步永远是看谁在吃 CPU。

```bash
ps -eo pid,pcpu,etime,comm --sort=-pcpu | head -5
```

结果一目了然：

```
  PID   %CPU     ELAPSED  COMMAND
32788  127.3    07:24:03  tracker-miner-fs-3
```

**GNOME 的文件索引器，已经连续满核跑了 7 小时 24 分。**

温度能说明问题有多严重：

| | 索引器运行中 | 停掉之后 |
|---|---|---|
| CPU 四核温度 | 76 / 76 / 76 / 75 ℃ | 59 / 59 / 59 / 60 ℃ |
| load average | 1.85 | 0.99 |

差了 17 度。风扇当然会叫。

### 为什么它跑不完

`tracker3 status` 显示 "Data is still being indexed, Estimated 55s left"——这句话它已经说了七个小时。往下翻，是刷屏的失败记录：

```
Could not get any metadata for uri:'file:///home/zhenda/Documents/ds_ws/
immich-app/library/upload/.../e010306c-....JPG' and mime:'image/jpeg'
```

一共 **1554 条**。

原因很清楚：`~/Documents/ds_ws/immich-app/library` 里躺着 **233 GB、21.6 万个文件**的照片库。索引器在提取图片元数据，但很多文件提取失败，它就会反复重试——永远出不来。

**更根本的问题是：服务数据放在 `~/Documents` 下。** GNOME 把 `Documents` 当作"用户文档目录"，索引器、云同步工具、"备份我的文档"这类程序默认都会去啃它。815 GB 的服务数据放在这里，等于给自己埋了个定时炸弹。

### 处理

不只是 `systemctl stop`。真要让这个问题不再复发，要堵四个地方：

```bash
# 1. 停掉并屏蔽服务
systemctl --user stop tracker-miner-fs-3.service tracker-extract-3.service \
  tracker-miner-fs-control-3.service tracker-miner-rss-3.service
systemctl --user mask tracker-miner-fs-3.service tracker-extract-3.service \
  tracker-miner-fs-control-3.service tracker-miner-rss-3.service
```

两个坑：

**坑一：只 mask 主服务不够。** 还有一个 `tracker-miner-fs-control-3.service` 是 D-Bus 控制代理，任何程序请求索引都会通过它把 miner 拉起来。

**坑二：`/etc/xdg/autostart/tracker-miner-fs-3.desktop` 里是直接调二进制的。**

```ini
Exec=/usr/libexec/tracker-miner-fs-3   ← 绕过 systemd，mask 管不住
```

必须用用户级同名文件压掉：

```
~/.config/autostart/tracker-miner-fs-3.desktop → Hidden=true
```

验证方式不能只看一眼，要连续观察：

```bash
for i in 1 2 3 4 5 6; do sleep 10; pgrep -a tracker >/dev/null \
  && echo "[${i}0s] 复活了" || echo "[${i}0s] clean"; done
```

六次全部 clean 才算成功。

---

## 二、顺带清掉的垃圾

排查过程中在家目录根下发现了三个文件：

```
fstab~72U7BJ   fstab~7CiP0Z   fstab~HFDwde
```

三个 595 字节的文件，md5 完全相同，全是 `/etc/fstab` 的旧内容。

`fstab~XXXXXX` 这种命名是 `mktemp` 的模板特征。加上属主是普通用户、位置在家目录，可以还原出当时发生的事：**有人用普通用户身份跑了某个改 fstab 的脚本，草稿生成在家目录，最终没清理。** 系统盘上的真实 `/etc/fstab` 已经是对的（`/swapfile 16G`），这三个纯属垃圾。

顺手还把 `/swap.img` 清了——那是个 **4 GB 的孤儿文件**。当初从 4 GB 的 `swap.img` 升级到 16 GB 的 `swapfile`，旧文件没人删，白白占着空间。

```bash
sudo swapoff /swap.img 2>/dev/null
sudo rm -f /swap.img
sudo sed -i '/^#\/swap\.img/d' /etc/fstab   # 顺手删掉注释掉的死配置
```

---

## 三、备份：413 GB 从一个盘搬到另一个盘

这是今天最有价值的一件事。

### 发现的问题

Duplicati 的备份目标原本在 `~/Documents/ds_ws/duplicati-app/backups`——**和它要保护的源数据在同一块物理盘上**。

整台机器只有一块 3.6 TB 的 NVMe，根目录、服务数据、备份全在这上面。也就是说：

> 硬盘挂了，数据和"备份"一起消失。

这个"备份"唯一的作用是"误删了能找回来"，完全没有容灾价值。

先弄清 Duplicati 到底在备什么。目标是加密存储的（`enc-v1:`），但可以查数据库：

```bash
python3 -c "
import sqlite3
con = sqlite3.connect('file:Duplicati-server.sqlite?immutable=1', uri=True)
for r in con.execute('SELECT BackupID, Path FROM Source ORDER BY BackupID'):
    print(r)
"
```

结果发现**不存在"自己备份自己"**——每个任务只备份特定子目录（`immich-app/library`、`jellyfin-app/media`），和备份目标目录是平行关系，没有嵌套。之前我根据 compose 里的 `~/Documents/ds_ws:/source` 这个宽挂载推断"源包含目标"，属于误判：**挂载范围不等于备份源范围。**

### 迁移

买了一块 2 TB 的 M.2 2242 SATA SSD 插进机器空着的 SATA 位。这块盘后面还有个故事，先按下不表。

```bash
# 1. 格式化（整盘 ext4，保留块降到 1%）
mkfs.ext4 -L backup -m 1 /dev/sda

# 2. 挂载（注意 nofail：盘没插也能正常开机）
UUID=d475ad8a-...  /mnt/backup  ext4  defaults,nofail,x-systemd.device-timeout=10  0  2

# 3. 挂载点先设 root:root 700 —— 盘没挂上时容器写不进去，备份会明确报错
#    而不是静默写进系统盘把根分区填满
```

拷贝本身 20 分钟，平均 360 MB/s：

```
Number of files: 17,344 (reg: 17,337, dir: 7)
Total file size: 442,452,408,555 bytes
```

**验证才是重点**，不能只看"rsync 没报错"。做了三层：

1. 文件数和字节数与源完全一致
2. 把 Duplicati 各任务数据库里 `Remotevolume` 表的卷文件名和磁盘实际文件做集合比对——**零缺失、零多余**
3. 随机抽 6 个文件做 md5 内容比对

最后一步最关键：改 compose 里的一行，容器内路径保持不变。

```yaml
volumes:
  - ./config:/config
  - /mnt/backup/duplicati:/backups     # 原来写的是 ./backups:/backups
  - ~/Documents/ds_ws:/source
```

因为容器内还是 `/backups`，Duplicati 数据库里记录的六个任务目标不需要任何改动。

当晚 22:00 的定时任务就在新盘上跑成功了，写入了 8 个新卷。这比任何人工验证都有说服力——它证明整条链路是通的。

### 一个值得记下的坑

迁移完做"校验文件"（Verify）时，日志显示：

```json
{"VerificationsActualLength": 3, "BytesDownloaded": 79912408}
```

**244 GB 的备份，只校验了 76 MB。**

这是 Duplicati 的默认抽样策略——只验最新的 dlist、对应 dindex、再加一个随机的 dblock。它足以发现"文件损坏/丢失"，但不等于全量审计。知道这一点很重要，否则会误以为"校验通过 = 全部数据没问题"。

---

## 四、告警：让问题主动来找你

备份迁移完了，但"备份坏了半年没人知道"是另一个问题。接了两层告警。

### 第一层：Duplicati 邮件（QQ 邮箱）

Duplicati 的 send-mail 模块配置本身不复杂，卡住的是 QQ 邮箱。

配置写进数据库后，我先直接测试 SMTP 凭据：

```
535 Login fail. Account is abnormal, service is not open,
    password is incorrect, login frequency limited
```

有意思的是排查过程：用 Python 的 `smtplib` 自动协商认证方式时，QQ **直接断开连接**；改成手工走 `AUTH LOGIN`，才拿到这个明确的 535 错误。

**这是个通用经验：服务器"主动断连"时，往往不是网络问题，而是它不想跟你多说话；换一种握手方式能逼出真实错误码。**

授权码格式全对（16 位小写字母、无空格、From 与账号一致），所以问题在账号侧——最终是重新生成授权码解决的。

配置项（全局默认，一次管所有任务）：

```ini
--send-mail-to=xxx@qq.com
--send-mail-from=xxx@qq.com
--send-mail-url=smtps://smtp.qq.com:465
--send-mail-username=xxx@qq.com
--send-mail-password=<16位授权码>
--send-mail-level=Warning,Error
--send-mail-subject=[家庭NAS] Duplicati %OPERATIONNAME% - %PARSEDRESULT%
```

**验证方法**：临时把 level 改成 `All`，跑一个最快的小任务（音乐库 0.27 秒跑完），确认能收到邮件，再改回 `Warning,Error`。不做这一步等于赌它能用。

### 第二层：smartd 硬盘监控

硬件故障是备份救不回来的场景，所以单独接一条。

smartmontools 已经装了，但缺 `/usr/sbin/sendmail`——smartd 靠它发信。装 `msmtp-mta` 提供兼容层，SMTP 配置直接从 Duplicati 数据库里读（避免密码落进脚本）。

监控配置：

```
# 系统盘 NVMe
/dev/nvme0 -d nvme -a -s (S/../.././03|L/../../6/04) -W 5,70,80 -m root -M daily

# 备份盘 SATA SSD
/dev/sda -a -o on -S on -s (S/../.././02|L/../../6/03) -W 5,60,70 -m root -M daily
```

`-M daily` 保证每天最多一封，不会刷屏。`-W 5,...` 里的 `5` 表示"温度变化超过 5℃ 才记日志"——设成 0 会每 30 分钟刷两行温度日志，把 journal 淹掉。

**这里有个 systemd 的坑**：

```
Failed to enable unit: Refusing to operate on alias name or linked unit file: smartd.service
```

Ubuntu 里 `smartd.service` 是 `smartmontools.service` 的别名（`Alias=smartd.service`），**对别名执行 enable 会被拒绝**。必须用真实单元名。

### 读出来的数据

| | NVMe 4 TB（系统盘） | SATA SSD 2 TB（备份盘） |
|---|---|---|
| 总体健康 | PASSED | PASSED |
| 重分配扇区 | — | 0 |
| 待定扇区 | — | 0 |
| 介质完整性错误 | 0 | — |
| 备用块 | 100% | — |
| 已用寿命 | **2%** | — |
| 总写入量 | 17.09 TB | 读不到 |
| 通电时间 | 13,982 小时（1.6 年） | **3 小时** |
| **异常关机次数** | **76** | — |

两个结论：

**① 系统盘还很年轻。** 1.6 年、17 TB 写入、2% 磨损——按这个速率能用几十年。

**② 76 次异常关机是个信号。** 这不是硬盘的问题，是供电/使用方式的问题。NVMe 有掉电保护，但 76 次反复经历"写入过程中突然断电"是累积风险，对 SQLite 和 PostgreSQL 更危险（这台机器上有 Duplicati 的任务库和 immich 的 PostgreSQL）。

**一台 7×24 跑的 NAS 应该配 UPS。** 300 块的小 UPS 能让这个数字停止增长，优先级高于再加一块硬盘。

---

## 五、网络：从手机热点回到光猫

查 IPv6 的时候发现了一件意外的事：

```
当前使用的 WiFi：OnePlus Ace 6T 822A
网关 10.23.62.23，MAC 是本地管理地址
```

**这台"NAS"连的不是家里的光猫，是一台手机的热点。**

这意味着：家人连家里 WiFi 时根本访问不到它；手机一息屏热点关了，NAS 就掉线。IP 也是手机分配的 `10.23.62.100`，随时会变。

### 固定 IP 的曲折

连回光猫 `CU_4yb9_5G` 后，拿到 `192.168.1.7`。在光猫里做了 DHCP 静态绑定（MAC → `192.168.1.10`），但重连 WiFi 后还是 `.7`。

排查的关键一步是看 DHCP 事务日志：

```
dhcp4 (wlp1s0): activation: beginning transaction (timeout in 45 seconds)
dhcp4 (wlp1s0): state changed new lease, address=192.168.1.7
```

这是**一次真实的 DHCP 事务**（不是本地租约缓存），服务器明确回了 `.7`。而绑定表里写的是 `.10`，MAC 也确认无误。

**结论：不是 MAC 配错，是光猫的 DHCP 服务没有重载绑定表。**

重启光猫（拔电源 30 秒）之后，绑定就生效了。

> 教训：做网络排障时，"我认为我配对了"和"服务端确实读到了"是两件事。日志里那句 `beginning transaction` 分辨出了"客户端没重新申请"和"服务端给了别的地址"，这一步省掉了后面所有的瞎猜。

顺便说一句，过程中我犯过一个错：因为之前建议用户绑有线网卡的 MAC，就当成了事实去做推断，还说成是"证据"。被追问时才意识到——**那是推测，不是观测**。后面改成直接看 DHCP 日志才定位到真因。

---

## 六、一个没预料到的洞：公网 IPv6

查主机名解析时，`getent hosts` 返回了一大串地址，其中两个是：

```
inet6 2408:8206:2660:3360:2d84:e181:4603:b98c/64  scope global dynamic
inet6 2408:8206:2660:3360:9b77:fe7d:86e4:22b2/64  scope global temporary
```

`2408:` 是联通的公网前缀。**两小时前检查时还只有 link-local 地址，是重启光猫之后路由器开始下发 IPv6 前缀（RA 广播）了。**

这就麻烦了：

```
ufw 状态: ENABLED=no          ← 防火墙根本没启用
[::]:445   SMB        [::]:8200  Duplicati
[::]:22    SSH        [::]:9443  Portainer
[::]:2283  immich     
（20 多个服务全部监听在 IPv6 通配地址上）
```

**IPv6 没有 NAT。** 每个设备都是"公网直连"，安不安全完全取决于防火墙和光猫有没有拦入站。

在本机用公网地址访问，返回 200 —— 这是必然的，关键是光猫挡不挡外部。联通家宽的 IPv6 在部分省份是不拦入站的。

### 处置

最直接的办法是关掉 IPv6。两层保险：

```bash
# ① NetworkManager 层：不再请求 IPv6（RA 是根因）
nmcli connection modify "CU_4yb9_5G" ipv6.method disabled

# ② 内核层：持久化禁用
cat > /etc/sysctl.d/99-disable-ipv6.conf <<'EOF'
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv6.conf.lo.disable_ipv6 = 1
EOF
sysctl --system
```

验证要彻底：全局地址、默认路由、连 `fe80::` 在内的所有地址都要消失，同时 IPv4 和网关必须仍然正常（最容易出的错是关 IPv6 时顺手把网络弄断了）。

> 这件事的教训不是"IPv6 不好"，而是**默认配置会变**。同一个 IP 地址，两小时前是"安全的内网设备"，两小时后变成"公网可达的主机"，中间没有人改过 NAS 的任何配置——是上游路由器开始下发前缀了。
>
> **基础设施的安全状态是有时效性的。** 装完系统那天的检查结论，不能当作今天的结论。

---

## 七、给家人用的那一面

技术问题解决完，还剩一个更实际的问题：**让家里人能用起来。**

### 导航页

Homarr 做了个公开看板，只放六个给家人用的服务：

```
家庭常用     家庭相册（immich）  影视（Jellyfin）  音乐（Navidrome）
阅读与听书   漫画（Komga）       有声书（Audiobookshelf）  电子书（Calibre-Web）
```

两个坑：

**① 看板名不能用中文。** 我把看板命名为「家庭」，整页报 `Application error: a server-side exception`。挖出 zod 的校验错误：

```json
{"validation":"regex","code":"invalid_string","path":["name"]}
```

Homarr 的看板名受正则约束（只允许 ASCII slug），中文名会让**服务端渲染直接崩**。改成 `family`，中文放到 `page_title`。

**② 公开看板的分类分区，访客默认是折叠的。** 六个卡片全是 0×0 不可见，查 DOM 才发现祖先节点 `display:none`：

```html
<div style="opacity: 0; height: 0px; overflow: hidden; display: none;">
```

Homarr 把「分区折叠状态」按登录用户存在 `section_collapse_state` 表里，**未登录的访客没有记录 → 只能默认折叠**。解法是把卡片移到分区标题下方的空分区里，标题当分组用，卡片常驻显示。

### 文件共享

Samba 之前只配了两个打印机共享，**一个文件共享都没有**——这台 NAS 的"文件共享"功能其实一直没启用。

配了三个：

```ini
[family]  ~/srv/family        可写 + 回收站
[media]   jellyfin 媒体目录    只读
[music]   navidrome 音乐目录   只读
```

两个细节值得记：

**`force user = zhenda`** —— 所有写入都以文件属主的身份进行。不这么设的话，家人写入的文件属于 `family` 用户（uid 不是 1000），Jellyfin 这类容器读不到。

**`vfs objects = recycle`** —— Samba 自带回收站模块。删除的文件先进 `.recycle`，保留目录结构和多版本：

```ini
vfs objects = recycle
recycle:repository = .recycle
recycle:keeptree = yes
recycle:versions = yes
```

配合 Duplicati 的 `keep-versions=3`，"误删恢复"这条链路就完整了——这也补上了原本打算用 Nextcloud 提供的能力。

### 停掉 Nextcloud

原本有一台 Nextcloud，但查了一下：

```
dbtype   = sqlite3        ← 官方不支持生产环境用 SQLite
证书     = 自签 CN=*      ← 浏览器每次都要点"继续前往"
数据库   = 1.8 MB         ← 基本没在用
文件     = 169 个，大部分是官方示例图
```

Nextcloud 用 SQLite 撑不住多人同时操作（单写锁），要修就得迁 PostgreSQL，为一个"没在用"的服务不值得。

**关键判断：它的优势大部分已被抵消。** 照片备份 → immich 更好；版本历史 → Duplicati 已有；远程访问 → 应该用 VPN 而不是把服务暴露出去。剩下唯一不可替代的是"给外部人发下载链接"——这个需求等真出现时再说。

容器停掉、数据保留（84 MB），随时能回来。

---

## 八、清理主机名

最后一件事小但烦人。

```
hostname      = myserver
/etc/hosts    = 127.0.1.1  zhenda-NucBoxG3-Plus    ← 装系统时的旧名字
myserver.local → 172.26.0.1                        ← 这是 Docker 网桥的地址
```

三个问题叠在一起：

1. 主机名和 hosts 不一致 → `sudo` 每次启动都尝试解析失败
2. `avahi-daemon` 没限制网卡，在**所有接口**（包括十几个 Docker 网桥）上发布了 `.local` 记录，解析时随机抢到哪个算哪个
3. `publish-workstation=no`，macOS Finder 和 iOS 根本发现不了它

修法：

```ini
# /etc/avahi/avahi-daemon.conf
[server]
allow-interfaces=wlp1s0     # 只在这个网卡上广播

[publish]
publish-workstation=yes     # 发布 workstation 记录，Finder 才能自动发现
```

修改后 avahi 的日志给出了干净的证据：

```
Joining mDNS multicast group on interface wlp1s0.IPv4 with address 192.168.1.10.
Registering new address record for 192.168.1.10 on wlp1s0.IPv4.
Server startup complete. Host name is NucBoxG3-Plus.local.
Withdrawing workstation service for veth2e471f4.     ← 之前错误广播在 docker 网桥上的记录正在撤销
```

顺带装了 `wsdd` 让 Windows 10/11 的「网络」里能看到这台机器。**这里有个坑：Ubuntu 的 `wsdd` 包不提供 systemd 服务单元**，只装了 `/usr/bin/wsdd`，得自己写一个：

```ini
[Service]
ExecStart=/usr/bin/wsdd --shortlog -4 -i wlp1s0 -w WORKGROUP
```

`-i wlp1s0` 是必须的——不加的话它和 avahi 一样，会在所有 Docker 网桥上广播。

---

## 九、最后一个失败：Tailscale 与 clash 的冲突

想给远程访问找个方案，选了 Tailscale（不需要公网 IP、不需要端口映射、不开任何端口）。

装完之后一直拿不到授权链接。日志说明原因：

```
register request: Post "https://controlplane.tailscale.com/machine/register":
connection attempts aborted by context: context deadline exceeded
```

排查过程很有意思：

```
1. curl 访问控制面         → 0.6 秒成功
2. /dev/tcp 连 443         → 成功
3. 但 tailscaled 的连接    → SYN-SENT，永远不回
```

最后在 `ss` 输出里看到了关键一行：

```
192.168.1.10:39360 → 198.18.0.200:443   [SYN-SENT]
```

`198.18.0.200` 是 **clash 给 `controlplane.tailscale.com` 分配的 fake-ip**。

### 为什么会有 fake-ip

clash 的 fake-ip 模式：客户端查 DNS 时，返回一个 `198.18.x.x` 的假地址，clash 记下"这个假 IP 对应哪个域名"。等流量发到假 IP 时，clash 就知道真实域名，从而能按**域名**分流——而如果客户端自己解析出真实 IP 再连接，clash 就只看得到 IP，无法精确匹配 `DOMAIN-SUFFIX` 规则。

它换来的是：域名分流精确、抗 DNS 污染、DNS 响应极快。

**代价是：任何"自己管理连接"的软件都会被假 IP 骗到。** tailscaled 拿到假地址后，它的 HTTP/2 Upgrade 握手在这条 TUN 路径上卡死，而普通 curl 的 HTTP 请求却没问题。

试过切 clash 的 direct 模式，不行——TUN 还在，假 IP 还在。要彻底解决得停掉 clash，或者加两条规则：

```yaml
dns:
  fake-ip-filter:
    - "+.tailscale.com"
    - "+.tailscale.io"

prepend-rules:
  - PROCESS-NAME,tailscaled,DIRECT
  - IP-CIDR,192.200.0.0/24,DIRECT,no-resolve
```

**这件事先搁置了。** 远程访问目前不是刚需，而 Tailscale 和 clash TUN 在同一个系统上天然抢路由——能修好，但需要长期维护这个例外。等真需要时再说，可能换个方案更划算（比如 NAS 上关掉 TUN，代理只给需要的容器配环境变量）。

---

## 十、这一天学到的

**1. 症状和根因常常隔得很远。**

风扇叫 → 不是因为灰尘，不是因为 CPU 老，是因为一个文件索引器在啃 21 万张照片，啃了 7 个小时。

如果只盯着"温度高"去清灰、换硅脂，就永远找不到真正的原因。

**2. 默认配置不等于合理配置。**

- ext4 默认给 root 保留 5% 空间——2 TB 的专用备份盘上这是 93 GB
- Samba 默认 `map to guest = bad user`——允许匿名访问
- avahi 默认在所有网卡上广播——在 Docker 宿主机上就是灾难
- 光猫重启后默认下发 IPv6 前缀——于是你的 NAS 悄悄变成了公网可达

这些都不是"配错了"，是"从来没配过"。

**3. 告警本身也会骗人。**

Duplicati 的 `LastBackupDate` 停在一年前，看起来像"一年没备份成功"。实际是：源数据一年没变，所以没有新版本，而这个字段记录的是"最后一次创建版本的时间"，不是"最后一次运行的时间"。

正确的判断方法不是看这个字段，而是看日志里的 `ExaminedFiles` 和 `AddedFiles`。

**4. 两层"接管全局"的工具叠在一起，会产生第三类问题。**

clash 的 TUN 接管路由和 DNS，Tailscale 也要建立自己的虚拟网络并直连自己的控制面。两者单独都没问题，叠在一起就卡在 SYN-SENT。

这类问题没有"谁的错"，只能选边站，或者给其中一方开例外。

**5. 先测量，再动手。**

几乎每一个问题的解决都依赖于一条具体的观测数据：`ps` 里的 127% CPU、`ss` 里的 SYN-SENT、`smartctl` 里的 76 次异常关机、DHCP 日志里的 `beginning transaction`。

如果先猜再改，大概会走很多弯路——这中间我自己也误判过两次（"备份源包含目标"和"绑错了 MAC"），两次都是因为拿推断当证据。

---

## 十一、收尾状态

```
噪音        68℃ → 59℃（索引器已禁用）
备份        442 GB 迁到独立物理盘，逐文件验证通过
邮件告警    Duplicati + smartd，均已实测收到
监控        两块盘，每日短自检 + 每周长自检
IPv6        已禁用（公网暴露面消除）
IP          192.168.1.10，光猫 DHCP 绑定
主机名      NucBoxG3-Plus，avahi 与 wsdd 均正常工作
家庭导航    http://192.168.1.10:7575/boards/family
文件共享    \\192.168.1.10\family
```

从"为什么这么吵"开始，最后的结果是：这台机器跑得更凉、备份在别的地方、出问题会主动发邮件、家里人能用上，而且关掉了一个我原本不知道存在的公网漏洞。

折腾到凌晨两点半，值了。
