+++
title = 'Js Ts Base'
subtitle = ""
date = 2024-12-31T15:48:54+08:00
draft = true
toc = true
series = ["js,ts"]
+++

[toc]

## 执行环境

```
+---------------------------------------+
|            JavaScript 代码            |
+------------------+--------------------+
                   ↓
+---------------------------------------+
|                V8 引擎                |
| - 解析器 Parse                         |
| - 字节码 Ignition                     |
| - JIT 编译 TurboFan                   |
| - 调用栈 Call Stack                    |
| - 垃圾回收 GC                          |
+------------------+--------------------+
                   ↓（触发异步）       
+---------------------------------------+
|    浏览器 Web APIs / Node.js libuv    |
| - setTimeout                           |
| - fetch                                 |
| - 文件 IO                               |
| - 网络 IO                               |
+------------------+--------------------+
                   ↓（事件循环调度）
+---------------------------------------+
|             Event Loop                 |
|   - Microtasks（Promise…）            |
|   - Macrotasks（Timeout…）            |
+---------------------------------------+

```

## js



书写:

* 在html中 用""写js代码
* script 一般写在 **body里面的最后**
    * 这样做的好处是 javaScript 代码可以在整个页面加载完成之后读取
* 单独写入js文件


规范: 
- 小驼峰          
- 常量, 全大写

js是弱类型的语言，运算时，自动转换类型

## 基础

### 调试

```js
console.log()
console.dir()
console.table()

debugger

instanceof
typeof a //查看类型
this //面向对象语言中 this 表示当前对象的一个引用
```

### 基础解惑

```js
// 类型
let a = [1,2,3];

let obj = {'a':1, 'b':2};
obj["a"]
obj["b"]
Object.keys(obj) // 查看 所有key

// 定义
// 块级作用域：用一对花括号创建的作用域（块）。
const a = "haha";  // 作用域在{}块内, 只读常量
let a = 13;  // 作用域在{}块内
var a = "haha";  // 作用域在函数内

typeof 43;
typeof '43';
typeof ture;

// 三元运算
const canVote = age >= 18 ? "Yes" : "No";

// 赋值表达式的返回值为右边
y = (x=90+5)
y

```


```js
// 值和类型都判断, 优先使用, 能不用 == 就不用, 它会转换类型判断, 遗留的功能
===

// void
<a href="javascript:void(document.form.submit())">Click here to submit</a>
```



### 常用的内置数据类型

| 类型   | 用途       | 常用方法                                                      |
| :----- | :--------- | :------------------------------------------------------------ |
| Array  | 数组       | push, pop, shift, unshift, slice, splice, map, filter, reduce |
| Map    | 键值对集合 | set, get, has, delete, clear                                  |
| Set    | 去重集合   | add, has, delete, clear                                       |
| Object | 对象       | keys, values, entries, assign                                 |
| String | 字符串     | split, substring, slice, indexOf, replace, toUpperCase        |
| Number | 数字       | parseInt, parseFloat, toFixed, isNaN                          |
| Math   | 数学运算   | Math.max, Math.min, Math.sqrt, Math.floor, Math.ceil          |
| Date   | 日期时间   | now, getTime, getFullYear, getMonth                           |
| RegExp | 正则表达式 | test, exec, match, replace                                    |
| JSON   | JSON 处理  | stringify, parse                                              |


Symbol
- Undefine
- Null

TODO: 原型链

概念
    创建属性方法的东西
定义构造函数后
    结构
        prototype
            constructor
                定义的构造函数
    使用
        Object.prototype.func1 = function(){}
            为所有对象创建属性，方法
        函数名.prototype
            为这个构造函数创建属性，方法
使用方法
    Object.create({})

```js
// Array
let arr = [1, 2, 3];

arr.push(4);          // [1, 2, 3, 4]
arr.pop();            // [1, 2, 3]

arr.unshift(0)  // [0, 1, 2, 3]
arr.shift()     // [1, 2, 3]

arr.slice(0, 2);     // [1, 2]
arr.splice(1, 1);    // [1, 3]
arr.map(x => x * 2); // [2, 4, 6]
arr.filter(x => x > 1); // [2, 3]
arr.reduce((a, b) => a + b, 0); // 6
//循环
fruits.forEach((item, index, array) => {console.log(item, index);});
//深拷贝
const fruitsCopy = [...fruits];
//解构
var [one, two, three] = [1,2,3];
//扩展
const nums = [1, 2, 3];
const more = [...nums, 4, 5];  // [1,2,3,4,5]
flat() //转为1维度的
//绑定属性
[].a1 = 'qq'


// Map
// key 可以是任何值（函数，对象...）转json没有原生支持
let map = new Map();
map.set('a', 1);
map.get('a'); // 1
map.has('a'); // true
map.delete('a');
map.clear();
// Set
let set = new Set();
set.add(1);
set.has(1); // true
set.delete(1);
set.clear();

// Object
// key类型 String, Symbol
let obj = {a: 1, b: 2};
Object.keys(obj);   // ['a', 'b']
Object.values(obj); // [1, 2]
Object.entries(obj); // [['a', 1], ['b', 2]]
Object.assign(obj, {c: 3}); // {a: 1, b: 2, c: 3}

// String
let str = "hello world";
str.split(" ");        // ['hello', 'world']
str.substring(0, 5);  // 'hello'
str.indexOf("world"); // 6
str.replace("world", "JS"); // 'hello JS'
str.toUpperCase();    // 'HELLO WORLD'
// 和array转换
''.split（”“）//字符串转数组
[].join（”“）//数组转字符串
// 模板可以换行
`hi is ${age} years old`


// Number
let num = "42.5";
parseInt(num);    // 42
parseFloat(num);  // 42.5
num.toFixed(1);   // '42.5'
isNaN(num);      // false
// Math
Math.max(1, 5, 3);    // 5
Math.min(1, 5, 3);    // 1
Math.sqrt(16);       // 4
Math.floor(4.7);    // 4
Math.ceil(4.2);     // 5
// Date
let now = new Date();
now.getFullYear();  // 当前年份
now.getMonth();     // 当前月份 (0-11)
now.getDate();      // 当前日期
now.getTime();      // 时间戳
// RegExp
let regex = /hello/i;
regex.test("Hello World"); // true
"hello world".match(regex); // ['hello']
"hello world".replace(regex, "hi"); // 'hi world'

/* JSON
json格式:
只有属性，没有方法
属性或字符串使用双引号
*/
let jsonStr = '{"a":1,"b":2}';
let obj = JSON.parse(jsonStr); // {a: 1, b: 2}
JSON.stringify(obj); // '{"a":1,"b":2}'

//类型转换
//num->str
String(123.54)

    
//str->num
Number('432')
parseInt('432')
parseFloat('432')


```
                       

                  
### 函数

创建
```js
const func1 = (x,y) => {x-y};

let fun2 = function(){
    let m = grid.length, n = grid[0].length
}

function fun1(a, b = 12){
    return a * b;
}
```

```js

// if
if (condition) {
} else {
}

// for

let arr = [3, 5, 7];

for (let i of iter) {}

for (const[i, v] of arr.entries()) {
    console.log(i, v)
}

// error
throw new Error("Not Equal");

/*
try... catch... finally...
throw...
*/

```
    

IIFE
    迭代器
        需要显式地维护其内部状态，不推荐
    生成器函数
        function* foo() {  yield 1;  yield 2;  yield 3;}




### 多模块

ES模块

```js
// math.js
export function add(a, b) {
  return a + b;
}

// app.js
import { add as ad} from './math.js';
console.log(ad(2, 3)); // 输出: 5

```


### 异步请求


```js

// async await
async function getUser() {
  try {
    const res = await fetch('/api/user');
    if (!res.ok) throw new Error('Request failed');
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);
  }
}

// Promise
fetch('/api/user')
  .then(res => res.json())
  .then(data => console.log(data))
  .catch(err => console.error(err));


/*=======================out了================== */

// jQuery.ajax
$.ajax({
  url: '/api/user',
  success(res) {
    console.log(res);
  }
});

// XMLHttpRequest()
const xhr = new XMLHttpRequest();
xhr.open('GET', '/api/user');
xhr.onload = () => {
  console.log(xhr.responseText);
};
xhr.send();
```


## CDN

是包含可分享代码库的服务器网络


## 类

ES5 引入 原型链
ES6 引入 class


* 类
    * class
    * 封装
        * #属性
        * #方法
    * 继承
        * extends            

## BOM

browser object model
    作用
        控制浏览器
    window.
        概念
            js的全局对象，表示浏览器窗口
            全局变量
        存储内容
            document
            弹框
                alert()
                    消息弹框
                confirm()
                    确认框
                let name = prompt()
                    输入字符串
            location
                含义： 当前url
                href
                    完整地址
                    protocol
                    origin
                    host
                        hostname+port
                    hostname
                        ip的域名
                    port
                pathname
            定时器
                间隔
                    x = setInterval()
                    clearInterval(x)
                倒计时
                    x = setTimeout()
                    clearTiemout(x)
                打开关闭页面
                    open()
                    close()
                移动浏览器
                    scrollTo(0,0)
                        滚动到指定位置
                history
                    back()
                    forword()
                    go(index)
                screen
                    avaliWidth
                    avaliHeight
                navigator

## DOM

```js

window.document

window.location

a = window.setInterval(3)
window.clearInterval(a)

a = window.setTimeout(3)
window.clearTimeout(a)
```

document object model
    概念
        html文档可以看成一颗树，DOM树
    作用
        获取各个节点的值，进行增删改查
    元素操作
        查
            直接获取元素的方式
                document.getElementById()
                document.getElementByClassName()
                document.getElementTagName()
                document.getElementName()
        改
            属性和样式
                document.getAttriobute("value")
                document.setAttribute("value", "")
            修改值
                ele.innerHTML = 'qwer';
                ele.k = v;
                ele.style.color = "blue";
                    js的事件
                        页面加载事件
                            操作
                                onunload
                                    用户离开页面时被触发
                                onload
                                    用户进入页面时被触发
                            作用
                                全部扫描完body后，才使用js函数。防止js运行失败
                        鼠标事件
                            点击
                                onclick
                                ondblclick
                            状态
                                进出控件边界
                                    onmouseenter
                                    onmouseleave
                                在控件上
                                    onmouseover
                                    onmousemove
                                        在控件上移动
                                    onmouseout
                                手指放下抬起
                                    onmousedown
                                    onmouseup
                        键盘事件
                            onkeydown
                            onkeyup
                            onkeypress
                        form表单事件
                            提交
                                onsubmit
                                onreset
                            焦点
                                onfocus
                                onblur
                                    失去焦点
                            文本
                                onchange
                                    离开输入框时
                                oninput
                    绑定js事件
                        直接1
                            <body onload="checkCookies()">
                        直接2
                            ele.onclick = function(){};
                        间接
                                document.addEventListener()
                                    document.addEventListener('click', function(event) {  console.log('Clicked element ID:', event.target.id);});
                                ele.addEventListener()
                                document.removeEventListener()
                                ele.removeEventListener()
        添加删除
            创建子控件
                document.createElement("")
                document.createTextNode("这是一个新的段落。");
            增删子控件
                appendChild()
                removeChild()





## jQuery


使用
    使用本地
        放到js文件夹里
        src选择路径
    使用cdn
教程
    What is jQuery? (tutorialsteacher.com)
jquery编写位置
    确保 DOM 已完全加载
    这是在编写任何jQuery代码之前需要编写的第一件事。您始终需要检查文档是否已准备就绪，以便安全地与 DOM 进行交互
原理
    添加jQuery属性

选择器
    $("#id")
    $("标签名")
    $(".class名")
jq的DOM
    属性
        添加属性
            $(#id).attr("color","red")
        删除属性
            $("#id").removeAttr("color")
            使用 jQuery 操作 HTML 属性 (tutorialsteacher.com)
    样式
        $("#id").css("color", "blue")
        class操作
            添加
                $("#id").addClass("b")
            删除
                $("#id").removeClass("b")
            切换
                $("#id").toggleClass("b")
    文本
        $("#id").text()
        $("#id").html()
            <font>
        $("#id").val()
    元素
        母元素内部增加子元素
            append()
            appendTo()
        前增加
            before()
            insertBefore()
        后增加
            after()
            insertAfter()
        删除
            删除子
                empty()
            删除母
                remove()
        与原生DOM的转换
            原生->jq
                $(div1)
            jq->原生
                div2[0]
                div2.get(0)
        遍历
            for
            each(fun1(i, e){})
                e是原生的DOM
                i是下标
事件
    直接调用
        click()
            点击绑定函数
        mouseleaves
    指定事件名调用
        on('', function() {})
        bind（“”, function（））
    unbind（）
    one（）
        只执行一次
    事件汇总
        jQuery 事件方法 (w3schools.com)
        DOM Manipulation Methods Reference - jQuery (tutorialsteacher.com)
ajax
    ajax
        示例

        参数
            type
                get
                post
                put
                delete
    jQuery.ajax() | jQuery API Documentation
    get
    post
    load
动画
    默认
        $("#div1").show(3000)
        $("#div1").hide(3000)
        $("#div1").toggle(3000)
            切换隐藏和显示
    自定义
        $("#div1").animate(a, b, c)
    折叠收起
                                   
              



## ts

运行ts的方式:

```bash
npm install -g ts-node
ts-node xxxx.ts
```
