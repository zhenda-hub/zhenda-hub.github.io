+++
title = 'Vue教程'
subtitle = ""
date = 2024-05-24T10:16:28+08:00
draft = false
toc = true
tags = ["web"]
+++

[toc]

## document

-   https://cn.vuejs.org/
-   https://cn.vuejs.org/tutorial/
-   https://www.vueframework.com/docs/v3/cn/style-guide
-   https://cn.vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram

## 前置知识

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

npm install xxx
npm uninstall xxx
npm update xxx

npm install

# 运行功能
npm run dev
npm run build
```

## 创建命令

```bash
npm create vue@latest
npm install
npm run dev
npm run build
```

## 项目结构

```bash
├───assets  # 用于存放静态资源，如图片、字体文件、全局样式等
├───router  # 存放路由配置文件
├───stores  # 用于管理全局数据
├───components  # 存放可复用的 页面内 组件, 如按钮、表单、导航栏等
├───views  # 存放路由视图组件（页面级组件）
├───App.vue
└───main.js
```

## 页面结构

```html
<template>
  <div class="todo-item">
    <h2>{{ title }}</h2>
    <button @click="markAsDone">Mark as Done</button>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
  },
  methods: {
    markAsDone() {
      console.log('Task completed');
    },
  },
};
</script>

<style scoped>
.todo-item {
  font-family: Arial, sans-serif;
  margin-bottom: 1em;
}
</style>

```
## 风格

- 选项式(简单, 类)
- 组合式(复杂, 函数)
  - 响应式状态变量
  - Vue 的响应式系统

## 基础

Attribute 绑定

```html
<div v-bind:id="dynamicId"></div>
<div :id="dynamicId"></div>
```
动态绑定多个值
```js
const objectOfAttrs = {
  id: 'container',
  class: 'wrapper',
  style: 'background-color:green'
}
```

```html
<div v-bind="objectOfAttrs"></div>
```

### 基本js结构

选项式
```js
export default {
  // 此选项的值应为 返回一个对象的函数
  // 请确保始终通过 this 来访问响应式状态
  data() {
    return {
      someObject: {}
    }
  },
  // 它应该是一个 包含所有方法的对象
  // 你不应该在定义 methods 时使用箭头函数，因为箭头函数没有自己的 this 上下文
  methods: {
    increment() {
      this.count++
    }
  },
  // 钩子在组件的模板和 DOM 已经被渲染并挂载完成后调用，此时组件已经完全挂载到页面上
  mounted() {
    const newObject = {}
    this.someObject = newObject

    console.log(newObject === this.someObject) // false
  },
  // xxx
  computed: {

  }
}
```
组合式

```js
import { ref, computed, onMounted } from 'vue'
import { Delete, Edit } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getTodoList } from '@/api/todo'

const newTodo = ref('')
const filter = ref('all')

// 初始化时获取数据
onMounted(() => {
  fetchTodos()
})

// 删除待办事项
const deleteTodo = (todo) => {
  todos.value = todos.value.filter(t => t.id !== todo.id)
  ElMessage.success('删除成功')
}
```

逻辑

- v-if 绑定条件很少改变
- v-show 需要频繁切换
- v-for

```js
const items = ref([{ message: 'Foo' }, { message: 'Bar' }])
```

```html
<li v-for="item in items">
  {{ item.message }}
</li>
```

#### 表单

v-model

```js
<script setup>
import { ref } from 'vue'

const message = ref('')

const selected = ref('')

const picked = ref('One')
</script>
```

```html
<textarea v-model="message" placeholder="add multiple lines"></textarea>

<span> Selected: {{ selected }}</span>
<select v-model="selected">
  <option disabled value="">Please select one</option>
  <option>A</option>
  <option>B</option>
  <option>C</option>
</select>

<div>Picked: {{ picked }}</div>
<input type="radio" id="one" value="One" v-model="picked" />
<label for="one">One</label>
<input type="radio" id="two" value="Two" v-model="picked" />
<label for="two">Two</label>
```

#### 事件

```js
function say(message) {
  alert(message)
}
```

```html
<button @click="say('hello')">Say hello</button>
<button @click="say('bye')">Say bye</button>
```


#### 请求

#### 生命周期钩子

<https://cn.vuejs.org/guide/essentials/lifecycle.html>

```html
mounted(){}
```

## 样式库

-   <https://element-plus.org/zh-CN/component/overview.html>
-   <https://element.eleme.cn/#/zh-CN/component/installation>
-   <https://vant-ui.github.io/vant/#/zh-CN/quickstart>

### element plus

```html
<template #prefix>
  <el-icon><Key /></el-icon>
</template>
```

```js
import { Delete, Edit } from '@element-plus/icons-vue'
import { Lock, Message, Key } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
```

Element Plus提供了:xs、:sm、:md、:lg、:xl的响应式属性


| 参数 | 说明 | 类型 | 可选值 | 默认值 |
| --- | --- | --- | --- | --- |
| span | 栅格占据的列数 | number | — | 24 |
| offset | 栅格左侧的间隔格数 | number | — | 0 |
| push | 栅格向右移动格数 | number | — | 0 |
| pull | 栅格向左移动格数 | number | — | 0 |
| **xs** | <code><768px</code> 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | — | — |
| sm | <code>≥768px</code> 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | — | — |
| md | <code>≥992px</code> 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | — | — |
| **lg** | <code>≥1200px</code> 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | — | — |
| xl | <code>≥1920px</code> 响应式栅格数或者栅格属性对象 | number/object (例如： {span: 4, offset: 4}) | — | — |
| tag | 自定义元素标签 | string | * | div |


```html
<el-col :xs="24" :sm="8">
```

form

```html
<el-dialog
  v-model="editDialogVisible"
  :title="isEdit ? '编辑待办事项' : '添加待办事项'"
  width="30%"
  :close-on-click-modal="false"
>
  <el-form :model="editForm" label-width="80px">
    <el-form-item label="标题">
      <el-input v-model="editForm.title" />
    </el-form-item>
    <el-form-item label="描述">
      <el-input v-model="editForm.description" type="textarea" />
    </el-form-item>
    <el-form-item label="状态">
      <el-select v-model="editForm.status">
        <el-option label="待办" value="pending" />
        <el-option label="完成" value="completed" />
      </el-select>
    </el-form-item>
    <el-form-item label="优先级">
      <el-select v-model="editForm.priority">
        <el-option label="低" value="low" />
        <el-option label="中" value="medium" />
        <el-option label="高" value="high" />
      </el-select>
    </el-form-item>
    <el-form-item label="截止日期">
      <el-date-picker v-model="editForm.due_date" type="date" />
    </el-form-item>
  </el-form>
  <template #footer>
    <span class="dialog-footer">
      <el-button @click="editDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="saveEdit">确定</el-button>
    </span>
  </template>
</el-dialog>
```



## 开发顺序

- 配置路由
- 初始化状态管理
- 全局布局
- 开发页面级组件
- 开发页面内组件
- 调用 API

## 动态更新

当 URL 路径变化时，Vue Router 会根据配置的路由规则，动态更新并渲染对应的组件到 `<router-view />` 中

## vue-router

```js
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
  ]
})

router.beforeEach((to, from, next) => {})
```
## 输入校验

- 前端获取后端规则：通过接口获取后端定义的验证规则，如密码、用户名格式等。
- 前端实时验证：使用 Vue 的表单绑定和计算属性，动态应用规则进行表单验证。
- 后端最终验证：即使前端验证通过，后端仍需要做最终验证，以确保数据符合要求并避免安全风险。
- 友好的错误反馈：前端根据后端返回的错误信息提供用户友好的提示

## 组件

| 属性/方法	| 作用 |
|---|---|
| this.$store	| 访问 Vuex 的全局状态管理对象 |
| this.$router	| 访问 Vue Router 实例（用于导航操作） |
| this.$route	| 访问当前路由信息 |


## storage

What are Local storage and cookies?
It is important to understand the concept of local storage and cookies. They are examples of web storage which is used to store important data in your browsers.
With the help of local storage, you can store data (up to 5 MB) of a website. You can access this data even after you close the browser. Whereas, cookies can store only 4 KB of data. Unlike Local storage, all data will be lost as soon as you close the browser.

## 缓存

<keep-alive> 是 Vue 提供的一个抽象组件，它能够缓存不活跃的组件实例，而不是每次切换时都销毁它们。这样可以在组件切换时保持组件的状态，避免重复渲染，提高性能


```html
<template>
  <div>
    <router-link to="/a">Go to A</router-link>
    <router-link to="/b">Go to B</router-link>
    <keep-alive>
      <router-view></router-view>
    </keep-alive>
  </div>
</template>

<script>
import ComponentA from './ComponentA.vue';
import ComponentB from './ComponentB.vue';

export default {
  components: {
    ComponentA,
    ComponentB
  }
};
</script>

```

1. 当用户首次访问 /a 时，ComponentA 被渲染并挂载到 DOM 上，触发 mounted 钩子。
2. 用户切换到 /b，ComponentA 被缓存，触发 deactivated 钩子，ComponentB 被渲染并挂载，触发 mounted 钩子。
3. 用户再次切换回 /a，ComponentB 被缓存，触发 deactivated 钩子，ComponentA 从缓存中恢复，触发 activated 钩子，而不会重新触发 mounted

## 部署

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
