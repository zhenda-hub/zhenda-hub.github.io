+++
title = '键盘 Win 键失灵、Alt 和 Win 互换：切到了 Mac 模式'
subtitle = "RK989：三个键同时失灵，按一次 Fn + A 复原"
date = 2026-08-31T00:00:00+08:00
draft = false
toc = true
series = ["life"]
aliases = ["/posts/system/keyboard/"]
tags = ["键盘模式", "Fn组合键"]
featureimage = "featured.webp"
+++

按 Alt 弹出开始菜单，按 Win 没反应，Fn 那排音量键也没了。不是驱动，也不是键盘坏了：**它停在了 Mac 模式**。玩 GTA5 误触 `Fn + S`，`Fn + A` 按一次，三个症状一起消失。

## 模式切换

| 组合键 | 作用 |
|---|---|
| `Fn + A` | Windows 模式 |
| `Fn + S` | Mac 模式 |

Mac 模式下 Win↔Alt 互换、Fn 层多媒体键失效。三个症状是同一个原因，不是三处坏。

## RK989 常用 Fn 速查

| 功能 | 组合键 |
|---|---|
| Windows 模式 | `Fn + A` |
| Mac 模式 | `Fn + S` |
| 锁/解锁 Win 键 | `Fn + Win` |
| 左 Win 和 Alt 互换 | `Fn + Alt(左)` |
| 恢复出厂 | `Fn + 空格` 长按 3 秒 |
| 蓝牙设备 1/2/3 切换 | `Fn + Q/W/E` |

⚠️ `Fn+W/E` 是**蓝牙设备切换**,不是系统模式。网上写的 "Fn+W=Win" 是 AULA 狼蛛的键位,别照抄。

## 一眼判断模式

- 按 Win 键弹出开始菜单 = Windows 模式
- 按 Win 没反应、按 Alt 反而弹出 = Mac 模式
- 切换模式/蓝牙时键盘指示灯会闪

## 经验

1. 游戏(GTA5 等)容易误触 Fn 组合键,按键失灵先查键盘模式
2. 音量调不了先查键盘,再查系统
3. VID 18F8 是通用 OEM ID(AULA/RK 共用),认准键盘背面型号
