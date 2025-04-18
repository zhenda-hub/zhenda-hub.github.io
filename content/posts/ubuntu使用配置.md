+++
title = 'Ubuntu使用配置'
subtitle = ""
date = 2024-04-30T13:43:06+08:00
draft = false
toc = true
tags = ["linux"]
+++

## install and uninstall

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

```bash
sudo apt install inetutils-traceroute
sudo apt install flameshot
sudo apt-get install gnome-shell-pomodoro
```

install
```bash
sudo apt install <path to .deb file>
# 备用
sudo dpkg -i <path to .deb file>
```

## 中文

```bash
sudo apt install ibus-pinyin
```
## settings

再次点击图标实现最小化

```bash
gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
```

### ~/.xxxrc file settings

-   ~/.bashrc

    ```bash
    # auto ls
    function cd {
        builtin cd "$@" && ls
    }

    # alias
    alias ls='ls --time-style=long-iso'
    alias ll='ls -alFh'

    alias edge='microsoft-edge'
    alias chrome='google-chrome'

    ```
- ~/.profile
    ```bash

    ```
-   ~/.vimrc

    ```bash
    syntax on
    set autoindent
    set tabstop=4
    set shiftwidth=4
    set cursorline
    set backup
    set backupdir=~/.vim/undo
    ```

-   ~/.nanorc

    ```bash
    include "/usr/share/nano/*.nanorc"
    set tabsize 4
    set backup
    ```

<!--
## Homebrew

https://docs.brew.sh/Homebrew-on-Linux -->

## ssh

<!-- ssh -v ubuntu@134.175.124.152 -->

```bash
ssh -v 用户名@ip地址
exit
scp ... ...
```

## open image

```bash
eog xxx.png
```

## resize mem swap

```bash
# resize swap
sudo swapoff -a
sudo dd if=/dev/zero of=/swapfile bs=1G count=32
sudo chmod 0600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# look swap
swapon --show
free -h
```

https://askubuntu.com/questions/178712/how-to-increase-swap-space
https://help.ubuntu.com/community/SwapFaq#Why_is_my_swap_not_being_used.3F

## check screen

```bash
xrandr
```
## dns setting

```bash
sudo nano /etc/resolv.conf

nameserver 8.8.8.8
nameserver 8.8.4.4
```

## keyboard

```bash
ibus restart
ibus-setup
```
## gnome

```bash
# 重启
sudo systemctl restart gdm
```

## 右键添加文件

<https://cn.linux-console.net/?p=18873>

在 `~/Templates` 里面 放置一些想创建的文件, 右键就可以新建了

## 无法打开terminal

<https://blog.csdn.net/u010092716/article/details/130968032>

## Remaining matters

-   查看所有的 history
-   视频没有预览图
-   ping 很多网站不通


## sys update

您的 sources.list 中的一些第三方源被禁用。您可以在升级后用"软件源"工具或包管理器来重新启用它们


在更新您的软件包信息后，无法定位必要的软件包“ubuntu-minimal”。这可能是因为您没有在软件源中使用官方镜像，或您正在使用的镜像负载过重。请查看 /etc/apt/sources.list 文件了解软件源当前的配置列表。


## server app

```bash
sudo apt install net-tools
sudo apt install openssh-server
```


## X11 wayland 区别

两个图形显示框架

<https://zhuanlan.zhihu.com/p/26028490976>

```bash
sudo vi /etc/gdm3/custom.conf
# wayland -> X11
# 注意第7行是 #WaylandEnable=false，去掉注释，改成WaylandEnable=false，保存
sudo systemctl restart gdm3 
```