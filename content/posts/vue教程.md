+++
title = 'Vue教程'
subtitle = ""
date = 2024-05-24T10:16:28+08:00
draft = true
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

-   nodejs
    -   运行环境
    -   npm
        -   nodejs 的包管理器
    -   npm
        -   配置源
            -   get registry
            -   config set registry 地址
        -   list
            -   默认显示本地
            -   -g
                -   全局
        -   -v
            -   查看版本
        -   config list
            -   查看 config
        -   install 模块名
            -   安装
        -   update 模块名
            -   更新
        -   uninstall 模块名
            -   卸载
        -   init
            -   生成 package.json
        -   run serve
            -   运行项目
-   启动项目方式
    -   create vue
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
        -   style
    -   项目结构
        -   router
        -   views
        -   App.vue
            -   主文件
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
    -   组建间传参
        -   defineProps
-   vue-router
    -   RouterLink
        -   <RouterLink :to="{ name: 'video' }">Video</RouterLink>
    -   RouterView
        -   view
            -   指的是子 html
-   axios
    -   http 请求
-   vuex
    -   状态保持
-   表单
-   部署
-   第三方样式库
    -   https://element.eleme.cn/#/zh-CN/component/installation
    -   https://vant-ui.github.io/vant/#/zh-CN/quickstart
