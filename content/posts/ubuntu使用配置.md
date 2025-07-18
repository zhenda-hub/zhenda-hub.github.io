+++
title = 'Ubuntu使用配置'
subtitle = ""
date = 2024-04-30T13:43:06+08:00
draft = false
toc = true
tags = ["linux"]
+++

[toc]

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
sudo apt purge <path to .deb file>

sudo apt purge xxxx* 
sudo apt autoremove
# 备用
sudo dpkg -l | grep xxx
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


-  多用户访问
-  桌面远程访问

### settings

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
sudo apt install flameshot
sudo apt-get install gnome-shell-pomodoro
```


### preload

```bash
sudo apt -y install preload
sudo preload -l
sudo systemctl status preload.service
sudo cat /var/log/preload.log
```

### AppImage 类型的软件

```bash
# 安装依赖
sudo apt install fuse

chmod +x ./xxx.AppImage
./xxx.AppImage
```

### 办公软件

#### libreoffice

兼容office太差, 建议卸载

#### onlyoffice

兼容office好

#### wps

有一些字体报错

## 默认打开方式

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


### resize mem swap

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



## 遗留问题

-   查看所有的 history
-   视频没有预览图
-   ping 很多网站不通





### sys update

您的 sources.list 中的一些第三方源被禁用。您可以在升级后用"软件源"工具或包管理器来重新启用它们


在更新您的软件包信息后，无法定位必要的软件包“ubuntu-minimal”。这可能是因为您没有在软件源中使用官方镜像，或您正在使用的镜像负载过重。请查看 /etc/apt/sources.list 文件了解软件源当前的配置列表。

