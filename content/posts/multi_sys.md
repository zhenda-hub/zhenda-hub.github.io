+++
title = 'Multi_sys'
subtitle = ""
date = 2025-02-06T23:26:55+08:00
draft = true
toc = true
tags = []
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

关闭 Secure Boot


```cmd
sc.exe query vboxsup
sc start vboxsup
```
