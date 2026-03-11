+++
title = 'Ubuntu使用配置'
subtitle = ""
date = 2024-04-30T13:43:06+08:00
draft = false
toc = true
series = ["system"]
+++

[toc]

## install tool

apt
snap store, snap 各种问题
brew
asdf

```bash
# 罗列所有的snap软件
ll ~/snap
```

## install and remove

sys_update.sh

```bash
#!/bin/bash

# 更新软件包列表
echo "更新软件包列表..."
sudo apt update -y

# 升级已安装的软件包
echo "升级已安装的软件包..."
sudo apt upgrade -y

# 删除不再需要的包
echo "删除不再需要的包..."
sudo apt autoremove -y

# 清理软件包缓存
echo "清理缓存..."
sudo apt clean

echo "系统更新和清理完成！"
```

install

```bash
sudo apt install <path to .deb file>
# 备用
sudo dpkg -i <path to .deb file>
```

remove

```bash
# 查询软件名
dpkg -l | grep electron-stu

# 仅仅删除程序
sudo apt remove xxxx*

sudo apt autoremove
# 备用
sudo dpkg -P <path to .deb file>
```

## 基本设置

### 中文

```bash
sudo apt install ibus-pinyin
```

### keyboard

```bash
ibus restart
ibus-setup
```

### 设置远程访问

#### ssh 远程访问

服务端设置 ssh

```bash
# 安装 SSH 服务
sudo apt install net-tools
sudo apt install openssh-server

# 检查 SSH 服务状态
sudo systemctl status ssh

# 如果需要，启用服务
sudo systemctl enable ssh
sudo systemctl start ssh
```

客户端使用 ssh

<!-- ssh -v ubuntu@134.175.124.152 -->

```bash
ssh -v 用户名@ip地址
exit
scp ... ...
```

- 多用户访问
- 桌面远程访问

### settings

再次点击图标实现最小化

```bash
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
```

<!--
## Homebrew

https://docs.brew.sh/Homebrew-on-Linux -->

### ip设置固定

```bash
# 查看现在网络
ip a
route -n
ip route | grep default
```

iphone 热点连接配置

```
网段：   172.20.10.0/28
网关：   172.20.10.1
掩码：   255.255.255.240

DNS:     8.8.8.8, 1.1.1.1
```

静态 IP 必须避开 DHCP 已经分配的 IP

### 显示隐藏文件(.xxxxx)

按 ctrl + h

## 常用软件

### gnome extension

```bash
sudo apt install gnome-shell-extensions chrome-gnome-shell gnome-tweaks
```

<https://extensions.gnome.org/>

- lipboard Indicator
- Vitals
- OpenWeather

```bash
sudo apt install inetutils-traceroute
sudo apt-get install gnome-shell-pomodoro
```

### preload

```bash
sudo apt -y install preload
sudo preload -l
sudo systemctl status preload.service
sudo cat /var/log/preload.log
```

### preview image, video

```bash
sudo apt install gnome-sushi
```

### AppImage 类型的软件

不好用，不如deb

```bash
# 安装依赖
sudo apt install fuse3
sudo apt install libfuse2

chmod +x ./xxx.AppImage
./xxx.AppImage
```

### flameshot 截图

<https://zhuanlan.zhihu.com/p/166559142>

```bash
sudo apt install flameshot
flameshot gui
```

### 办公软件

#### libreoffice

兼容office太差, 建议卸载

#### onlyoffice

兼容office好

#### wps

有一些字体报错， 需要安装字体包（在星火商店）

## 默认打开方式

```bash
xdg-open .
```

右键 属性 打开方式
<https://blog.csdn.net/weixin_43994864/article/details/110468818>

## 使用技巧

### 右键添加文件

<https://cn.linux-console.net/?p=18873>

在 `~/Templates` 里面 放置一些想创建的文件, 右键就可以新建了

### open image

```bash
eog xxx.png
```

## 进阶设置

### 查看重启记录

```bash

last reboot
```

```bash
reboot   system boot  6.14.0-28-generi Tue Sep 23 00:14   still running
reboot   system boot  6.14.0-28-generi Mon Sep 22 21:22 - 00:14  (02:52)
reboot   system boot  6.14.0-27-generi Wed Aug 13 00:05 - 00:14 (41+00:08)
reboot   system boot  6.14.0-24-generi Tue Jul 22 22:40 - 00:14 (62+01:33)
reboot   system boot  6.14.0-24-generi Fri Jul 18 21:41 - 22:40 (4+00:58)
reboot   system boot  6.11.0-26-generi Sun Jun 22 01:52 - 21:41 (26+19:48)
reboot   system boot  6.11.0-25-generi Mon May 12 23:20 - 21:41 (66+22:21)
reboot   system boot  6.11.0-21-generi Thu Apr 17 00:27 - 23:19 (25+22:52)
reboot   system boot  6.11.0-21-generi Wed Apr 16 01:35 - 23:19 (26+21:44)
reboot   system boot  6.11.0-21-generi Wed Apr 16 00:20 - 23:19 (26+22:59)
reboot   system boot  6.11.0-21-generi Mon Apr 14 23:54 - 23:19 (27+23:24)
reboot   system boot  6.11.0-21-generi Fri Apr  4 00:54 - 23:19 (38+22:24)
reboot   system boot  6.11.0-19-generi Sun Mar 23 23:11 - 00:54 (11+01:42)
reboot   system boot  6.11.0-17-generi Sun Feb 23 20:52 - 00:54 (39+04:01)
reboot   system boot  6.11.0-17-generi Sun Feb 23 20:22 - 20:52  (00:30)
reboot   system boot  6.11.0-17-generi Sun Feb 23 19:52 - 20:21  (00:29)
```

### xxx

sing-box
v2rayA
X-ui面板

### 改server脚本

```bash
#!/bin/bash
# Ubuntu Desktop → 简化伪服务器优化脚本（去掉健康监控，保留模式切换）

echo "=== Ubuntu Desktop → 伪服务器优化（简化版） ==="

# 1️⃣ 禁用休眠 / 挂起
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
echo "✅ 已禁用休眠和挂起"

# 2️⃣ 禁用自动更新重启
sudo systemctl disable --now unattended-upgrades
echo "✅ 已禁用 unattended-upgrades 自动重启"

# 3️⃣ 模式选择：Desktop / Server
echo "选择运行模式："
echo "1) 保留桌面环境（Desktop）"
echo "2) 切换命令行模式（Server）"
read -p "请选择 (1/2): " GUI_CHOICE

if [[ "$GUI_CHOICE" == "2" ]]; then
    sudo systemctl set-default multi-user.target
    echo "✅ 已切换到命令行模式（Server）"
else
    sudo systemctl set-default graphical.target
    echo "✅ 保留桌面模式（Desktop）"
fi

# 4️⃣ 禁用非必要桌面服务
# services=( "bluetooth.service" "cups.service" "cups-browsed.service" "avahi-daemon.service" "ModemManager.service" )
services=( "cups.service" "cups-browsed.service" "avahi-daemon.service" "ModemManager.service" )
for service in "${services[@]}"; do
    sudo systemctl disable "$service" 2>/dev/null
    echo "✅ 已禁用 $service"
done

# 5️⃣ 日志优化
sudo journalctl --vacuum-size=200M
grep -q "SystemMaxUse" /etc/systemd/journald.conf || echo "SystemMaxUse=200M" | sudo tee -a /etc/systemd/journald.conf
sudo systemctl restart systemd-journald
echo "✅ 日志限制完成（最大 200M）"

# 6️⃣ Swap 优化
SWAPFILE=/swapfile
if [ ! -f "$SWAPFILE" ]; then
    sudo fallocate -l 4G $SWAPFILE
    sudo chmod 600 $SWAPFILE
    sudo mkswap $SWAPFILE
    sudo swapon $SWAPFILE
    echo "$SWAPFILE none swap sw 0 0" | sudo tee -a /etc/fstab
    echo "✅ 创建 4G swap"
else
    echo "✅ swap 已存在，跳过创建"
fi

sudo sysctl vm.swappiness=10
grep -q "vm.swappiness=10" /etc/sysctl.conf || echo "vm.swappiness=10" | sudo tee -a /etc/sysctl.conf
echo "✅ swappiness 设置完成"

# 7️⃣ Docker 自启（如果安装了 Docker）
if command -v docker &> /dev/null; then
    sudo systemctl enable docker
    echo "✅ Docker 服务自启"
else
    echo "⚠ 未检测到 Docker，跳过 Docker 设置"
fi

# 8️⃣ 创建模式切换脚本
sudo tee /usr/local/bin/server-mode << 'EOF'
#!/bin/bash
case $1 in
    "desktop")
        sudo systemctl set-default graphical.target
        sudo systemctl start gdm3 2>/dev/null
        echo "✅ 已切换到桌面模式"
        ;;
    "server")
        sudo systemctl set-default multi-user.target
        sudo systemctl stop gdm3 2>/dev/null
        echo "✅ 已切换到服务器模式"
        ;;
    "status")
        echo "当前模式: $(systemctl get-default)"
        echo "运行时间: $(uptime -p)"
        echo "内存使用: $(free -h | grep Mem | awk '{print $3"/"$2}')"
        echo "磁盘使用: $(df -h / | awk 'NR==2{print $5}')"
        ;;
    *)
        echo "用法: server-mode [desktop|server|status]"
        ;;
esac
EOF
sudo chmod +x /usr/local/bin/server-mode
echo "✅ 已创建模式切换脚本 /usr/local/bin/server-mode"

echo ""
echo "🎉 优化完成！"
echo "• 使用 server-mode desktop/server/status 切换和查看模式"
echo "• 建议重启系统以生效所有优化"

read -p "是否现在重启？(y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo reboot
fi

```

使用方法

```bash

# 保存为文件，例如：
nano ~/ubuntu-server-lite.sh

# 赋予执行权限：
chmod +x ~/ubuntu-server-lite.sh

# 执行脚本：
sudo ~/ubuntu-server-lite.sh

# 查看状态：
server-mode status
# 切换到桌面：
server-mode desktop
# 切换到命令行模式：
server-mode server
```

### 内存扩充

#### resize memswap

```bash
# look swap
swapon --show
free -h

# off swap
sudo swapoff -a
sudo rm /swapfile

# mk swap, 设置和内存一样大，可以休眠到磁盘
sudo dd if=/dev/zero of=/swapfile bs=1G count=16
sudo chmod 0600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 编辑 /etc/fstab，把对应行注释掉。
# /swapfile none swap sw 0 0
sudo swapon -a # 根据 /etc/fstab 启动， 系统开机会自动执行

```

https://askubuntu.com/questions/178712/how-to-increase-swap-space
https://help.ubuntu.com/community/SwapFaq#Why_is_my_swap_not_being_used.3F

#### zswap

查看

```bash
# 是否开启
cat /sys/module/zswap/parameters/enabled


mount | grep debugfs
# 如果没输出，挂载它（临时，重启失效）
sudo mount -t debugfs none /sys/kernel/debug


# 实时观察
sudo grep -r . /sys/kernel/debug/zswap/
watch -n 2 "sudo grep -r . /sys/kernel/debug/zswap/ | sed 's|.*/||'"
```

开启：

```bash
sudo nano /etc/default/grub
```

```
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash zswap.enabled=1 zswap.compressor=zstd zswap.zpool=zsmalloc zswap.max_pool_percent=30"
```

```bash
sudo update-grub
sudo reboot
```

#### swappiness

保持默认60. 如果想更多的用zswap, 需要加大数值

```bash
sudo nano /etc/sysctl.conf
vm.swappiness=60

sudo sysctl -p
```

### 屏幕详情

```bash
xrandr
```

### dns setting

```bash
sudo nano /etc/resolv.conf

nameserver 8.8.8.8
nameserver 8.8.4.4
```

### gnome

```bash
# 重启
sudo systemctl restart gdm
```

### X11 wayland 区别

两个图形显示框架

<https://zhuanlan.zhihu.com/p/26028490976>

```bash
# 查看当前会话类型
echo $XDG_SESSION_TYPE


sudo vi /etc/gdm3/custom.conf
# wayland -> X11
# 注意第7行是 #WaylandEnable=false，去掉注释，改成WaylandEnable=false，保存
sudo systemctl restart gdm3
```

### 音频工具ffmpeg

```bash
sudo apt install ffmpeg
ffmpeg -i 音乐文件.mp3
```

## 常见问题

### 无法打开terminal

<https://blog.csdn.net/u010092716/article/details/130968032>

### 无法进入设置

<https://blog.csdn.net/qq_38500436/article/details/106652746>

```bash
sudo apt update
sudo apt install gnome-control-center
```

### wifi 搜索不到网路

```bash
nmcli device
# 如果有 断开连接, 继续下面命令

sudo lspci -k | grep -A 3 -i network
# 寻找 kernel driver in use: mt7921e

sudo modprobe -r mt7921e
sleep 2
sudo modprobe mt7921e

sudo systemctl restart NetworkManager
nmcli device wifi list

```

## 遗留问题

- 查看所有的 history
- 视频没有预览图
- ping 很多网站不通

### sys update

常见一场提示, 原因是改了 apt源

```txt
您的 sources.list 中的一些第三方源被禁用。您可以在升级后用"软件源"工具或包管理器来重新启用它们


在更新您的软件包信息后，无法定位必要的软件包“ubuntu-minimal”。这可能是因为您没有在软件源中使用官方镜像，或您正在使用的镜像负载过重。请查看 /etc/apt/sources.list 文件了解软件源当前的配置列表。
```

```bash
# 查看系统升级日志
cat /var/log/dist-upgrade/main.log
# 查看异常的包
apt-cache policy ubuntu-minimal


# 检查系统更新
do-release-upgrade -c


# apt源 配置文件
cat /etc/apt/sources.list
# 查看所有第三方源
ls /etc/apt/sources.list.d/

# 升级系统
sudo apt update
sudo apt upgrade -y

# 2选1
update-manager

sudo do-release-upgrade

```

## 有价值的链接

<https://www.ufans.top/index.php/archives/148/>

## snap tracker

```bash
sudo systemctl stop snapd
pkill tracker
```
