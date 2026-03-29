+++
title = 'Multi User'
subtitle = ""
date = 2026-03-28T21:07:46+08:00
draft = false
toc = true
series = ["system"]
+++

## pc

电脑全面支持



| 对比项           | Windows               | Linux                       |
| :--------------- | :-------------------- | :-------------------------- |
| 私有安装路径     | 用户 AppData 目录     | $HOME/local 或～/.local     |
| 共有安装路径     | Program Files 目录    | /usr/local 或 /opt          |
| 权限控制         | 安装时选择 + UAC 验证 | 文件系统权限（ugo）+ 组管理 |
| 环境变量         | 自动配置              | 需手动配置（私有安装）      |
| 卸载影响         | 私有仅影响当前用户    | 私有仅删除用户目录文件      |
| 共有影响所有用户 | 共有需 root 权限卸载  |                             |


软件安装在个人目录, 则为私有软件


## pad

部分安卓支持
ipad不支持

## phone

部分安卓支持
ios不支持
