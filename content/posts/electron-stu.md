+++
title = 'Electron Stu'
subtitle = ""
date = 2025-08-12T16:12:13+08:00
draft = true
toc = true
tags = []
+++



## quickstart

```bash
npm init -y
npm install electron --save-dev

```


```json
// package.json
"main": "main.js",
  "scripts": {
    "start": "electron .",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
```


```bash
npm run start
```


```js
// 加载页面
.loadFile()
```


为了将 Electron 的不同类型的进程桥接在一起，我们需要使用被称为 预加载 的特殊脚本。


## package

最简单的软件要300M

### 前置

#### 环境

```bash
npm install --save-dev @electron-forge/cli
npx electron-forge import
```

如果发布rpm包, 需要安装环境

```bash
sudo apt install rpm
```

#### 添加 元数据

```json
// package.json
"description": "a demo for stu electron",
"author": "zhangzhenda <zhangsan@example.com>",
```

#### 本地打包

```bash
npm run make
```

### github的cicd打包






## link
<https://www.electronjs.org/zh/docs/latest/>
