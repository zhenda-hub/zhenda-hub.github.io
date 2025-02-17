+++
title = 'Multi_sys'
subtitle = ""
date = 2025-02-06T23:26:55+08:00
draft = false
toc = true
tags = ["server"]
+++

## 系统

- 虚拟系统
  - PVE!!!!
    - pvesource
  - ESXi
  - 虚拟软件
    - virtualbox
    - vmware
- 其他系统
  - win
  - linux
  - firPE
  - UNRAID
  - iKuai
  - OpenWRT


## 系统安装

### u盘启动工具

- ETCHER
- ventoy!!!! , 开源
  - 作用
    - 为主机安装多系统
    - 把多系统装进U盘
  - iso, img


### 固件引导方式和固件引导程序

计算机在加载操作系统之前，由底层固件（固件就是存储在主板上、在系统上电时最先运行的软件）来初始化硬件、检测系统状态和加载引导加载器的过程

- BIOS
  - xorboot
  - grub
    - grub2win
    - grub4dos
- UEFI
  - refind


### virtualbox

<https://www.virtualbox.org/wiki/Downloads>

扩展插件:
- VirtualBox Guest Additions
- VirtualBox Extension Pack

<https://www.cnblogs.com/litifeng/p/18193323#:~:text=VirtualBox%20Extension%20Pack&text=VirtualBox%20RDP%E6%94%AF%E6%8C%81%EF%BC%9AExtension%20Pack,%E7%8E%AF%E5%A2%83%E7%9A%84%E5%9C%BA%E6%99%AF%E9%9D%9E%E5%B8%B8%E6%9C%89%E7%94%A8%E3%80%82>


#### ubuntu 上使用 virtualbox的问题:

Q: 创建虚拟机报错
A: 关闭 Secure Boot

Q: 
VirtualBox is not currently allowed to access USB devices. You can change this by adding your user to the 'vboxusers' group. Please see the user manual for a more detailed explanation.

A:
```bash
getent group vboxusers
gpasswd -a $USER vboxusers
getent group vboxusers
```

Q:
usb 挂载

A:
<https://linux.cn/article-15287-1.html>
<https://www.debugpoint.com/enable-usb-virtualbox/#google_vignette>

#### windows 上使用 virtualbox的问题:


Q: 虚拟化报错
A:
```cmd
sc.exe query vboxsup
sc start vboxsup
```


U盘改文件系统 ntfs 

d 为实际盘符
```cmd 
convert d:/fs:ntfs
```
