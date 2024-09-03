+++
title = 'Ubuntu使用配置'
subtitle = ""
date = 2024-04-30T13:43:06+08:00
draft = true
toc = true
tags = ["linux"]
+++

## install and uninstall

sys_update.sh

```bash
#!/bin/bash
echo "update:"
sudo apt update
echo "upgrade:"
sudo apt upgrade
echo "autoremove:"
sudo apt autoremove
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

## open picture

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


## Remaining matters

-   查看所有的 history
-   视频没有预览图
-   ping 很多网站不通
