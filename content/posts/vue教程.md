+++
title = 'Vue教程'
subtitle = ""
date = 2024-05-24T10:16:28+08:00
draft = false
toc = true
tags = ["web"]
+++

## document

-   https://cn.vuejs.org/
-   https://cn.vuejs.org/tutorial/
-   https://www.vueframework.com/docs/v3/cn/style-guide
-   https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## 内容总结

### 基本概念

| 名称 | 作用 |
|---|---|
| nvm | node版本管理工具 |
| node | 运行环境 |
| npm | node的包管理工具 |

nvm 命令:

```bash
# 查看
nvm ls
nvm ls-remote

# 设置默认版本
nvm alias default xxx.xxx.xxx

# 使用
nvm use xxx.xxx.xxx
nvm install xxx.xxx.xxx
nvm uninstall xxx.xxx.xxx
```

node 命令:

```bash
node -v
node xxx.js
```
npm 命令:

```bash
# 配置源
npm get registry
npm config set registry 地址

# 查看版本
npm -v
npm config list

# 生成 package.json, 前端通用配置文件
npm init

# 操作包
# 默认显示本地包
npm list
# 显示全局包
npm list -g
npm install

npm install xxx
npm uninstall xxx
npm update xxx

# 运行功能
npm run dev
npm run build
```

## 创建命令

```bash

```

### 项目结构

```

```


### 基础

变量

属性

逻辑

事件

请求

生命周期钩子

### 样式

-   https://element.eleme.cn/#/zh-CN/component/installation
-   https://vant-ui.github.io/vant/#/zh-CN/quickstart
-   ElementPlus


### 部署






-   启动项目方式
    -   create vue(vite)
        -   npm
            -   create vue@latest
            -   install
            -   run dev
            -   run build
    -   vue cli
        -   过时
-   结构
    -   vue 文件结构
        -   script
            -   setup
                -   才可以在 template 中使用
        -   template
            -   `<style scoped>` 可以确保每个组件的样式不会意外地影响其他组件
        -   style
    -   项目结构
        -   src
            -   router
            -   views
            -   App.vue
            -   main.js
        -   index.html
-   基础
    -   变量类型
        -   响应式基础
            -   ref
                -   只适用于对象
            -   reactive
                -   接受任何值类型
        -   其他关键字
            -   computed
                -   计算会被缓存
        -   watch
            -   监听
    -   {{ a++ }}
    -   属性指令
        -   v-bind:id="myId"
        -   :id="myId"
        -   当 id="id"
            -   v-bind:id
            -   :id
    -   逻辑
        -   v-if
            -   创建销毁
        -   v-show
            -   显示隐藏
        -   v-for
    -   事件处理
        -   v-on:
        -   @click
    -   v-model
        -   双向数据绑定
    -   修饰符
        -   很方便的小功能
    -   import ButtonCounter from './ButtonCounter.vue'
    -   export default
        -   export default 是 ES6 的语法，意思是将这个东西导出，你要 import 引入东西，导出了才能引用
-   vue2
    -   export default {}
        -   data(){}
        -   methods(){}
        -   mounted(){}
        -   data(){}
        -   data(){}
-   组件
    -   作用
        -   代码复用
    -   父亲向子传参
        -   defineProps
    -   子向父亲传参
        -   defineEmits
-   vue-router
    -   RouterLink
        -   <RouterLink :to="{ name: 'video' }">Video</RouterLink>
    -   RouterView
        -   view
            -   指的是子 html
-   axios
    -   http 请求
-   状态保持
    -   作用: 父子组件的 数据同步
    -   pinia
    -   vuex
-   表单
