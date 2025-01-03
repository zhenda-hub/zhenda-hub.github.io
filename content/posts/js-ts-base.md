+++
title = 'Js Ts Base'
subtitle = ""
date = 2024-12-31T15:48:54+08:00
draft = true
toc = true
tags = ["js"]
+++


## js

规范: 
- 小驼峰          
- 常量, 全大写

js是弱类型的语言，运算时，自动转换类型

## 基础


```js
// 类型
let a = [1,2,3];

let obj = {'a':1, 'b':2};
obj["a"]
obj["b"]

// 定义
// 块级作用域：用一对花括号创建的作用域（块）。
let a = 13;  // 作用域在{}块内
var a = "haha";  // 作用域在函数内
const a = "haha";  // 作用域在{}块内, 只读常量

typeof 43;
typeof '43';
typeof ture;

// 三元运算
const canVote = age >= 18 ? "Yes" : "No";

// 赋值表达式的返回值为右边
y = (x=90+5)
y
// if
if (condition) {
} else {
}

// for
let arr = [3, 5, 7];

for (const[i, v] of arr.entries()) {
    console.log(i, v)
}

// error
throw new Error("Not Equal");
```

```js

Math

Number

new Date()
```


### DOM

```js

window.document

window.location

a = window.setInterval(3)
window.clearInterval(a)

a = window.setTimeout(3)
window.clearTimeout(a)
```

## 异步请求




JS(基于对象)
    注释
        /*xxx*/
    相关工具
        运行环境
            nodejs
    结构
        ECMAScript
            欧洲计算机协会定制的语法规范
                基础
                    书写
                            在html中 用""写js代码
                            <script>一般写在</body>前面
                                这样做的好处是 javaScript 代码可以在整个页面加载完成之后读取
                        单独写入js文件
                            <script src="static/demo.js"></script>
                    规范
                        小驼峰
                        全大写
                            常量
                    js是弱类型的语言，运算时，自动转换类型
                    数据类型
                        声明
                            变量
                                装数据类型
                                会强制将变量声明提升到作用域最开始
                                解析器会把变量的声明提升到开头
                                声明
                                    let a = 13;
                                        更科学 更好
                                            不会提升变量定义
                                            不能重复声明
                                            作用域在{}块内
                                        不会绑定到window的属性
                                    var a = "haha";
                                        作用域在函数内
                                        绑定到window属性
                            常量
                                const MY_CST = 123;
                                    必须赋值
                                    {}块级作用域
                        运算符
                            typeof a
                                查看类型
                            this
                                面向对象语言中 this 表示当前对象的一个引用
                            in
                                判断索引或属性是否在对象内
                            delete property1
                                删除属性
                            赋值
                                =
                                +=
                            计算符号
                                如果是string类型，先尝试将它转为number类型，再判断
                                    %
                                    /
                                    *
                                    -
                                        ===
                                            全等
                                                值和类型都判断
                                                优先使用
                                        ==
                                            NaN!=NaN
                            位运算
                                &
                                |
                                ~
                                ^
                                <<
                                    >>
                                    >>>
                                        无符号右移
                            void
                                <a href="javascript:void(document.form.submit())">Click here to submit</a>
                            instanceof

                            原始数据类型
                                    Number
                                        是有范围的
                                            Infinity
                                                无穷
                                            NaN
                                                计算失败
                                            Number.MAX_VALUE
                                                最大安全数
                                            Number.MIN_VALUE
                                                最小安全数
                                        toFixed(2)
                                            小数点后两位
                                        进制
                                            二进制
                                                0b01010
                                                0B01010
                                            八进制
                                                0o777
                                                0O777
                                            16进制
                                                0XFFF
                                                0xFFF
                                        科学计数法
                                            123e2
                                                123*100
                                            123e-2
                                                123*0.01
                                    BigInt
                                        可以更精确地表示大整数
                                        Math
                                            属性
                                                PI
                                                E
                                            方法
                                                计算
                                                    abs()
                                                    pow()
                                                    sqrt()
                                                转换
                                                    round（）
                                                    floor()
                                                    ceil()
                                                比较
                                                    min()
                                                    max()
                                        Date
                                            创建
                                                var now = new Date()
                                                new Date(1995, 11, 25)
                                            获取
                                                getFullYear()
                                                getMonth()+1
                                                    显示需要+1
                                                getDate()
                                                    日
                                                getHours()
                                                getMinutes()
                                                getSeconds()
                                                getMilliseconds()
                                    String
                                        常用方法
                                            创建
                                                模板
                                                    可以换行
                                                    `hi is ${age} years old`
                                                        使用反引号包含
                                                ”“
                                                ‘’
                                                + 
                                                    a+b
                                                合并
                                                    concat（）
                                            length
                                            获取
                                                charAt（下标）
                                                    获取单个字符
                                                substr(a, count)
                                                    count：子串个数
                                                substring(a,b)
                                                    b：结束位置
                                            查找
                                                indexOf()
                                                search
                                            大小写转换
                                                toUpperCase()
                                                toLowerCase()
                                            替换
                                                replace（）
                                        eval()
                                            字符串转代码
                                        和array转换
                                            ''.split（”“）
                                                字符串转数组
                                            [].join（”“）
                                                数组转字符串
                                        正则表达式
                                            定义
                                                var reg = /^$/
                                            使用
                                                reg.test(str1)
                                    Regex
                                Bool
                                    true
                                    false
                                Symbol
                                    属性的类型
                                    Undefine
                                        undefine
                                    Null
                                        null
                            类型转换
                                num->str
                                    String(123.54)
                                    '123'.toString()
                                    123.toPrecision()
                                        准确转数字
                                    123.toExponential()
                                        指数计数法
                                    123.toFIxed()
                                        默认保留整数
                                str->num
                                    Number('432')
                                    parseInt()
                                    parseFloat()
                        对象类型
                            Array
                                创建
                                    var arr = [1,2,3]
                                    var arr = new Array()
                                    js的数组不会越界
                                    元素长度
                                        .length
                                            减小可以改变数组大小
                                常用方法
                                        查
                                            indexOf（”value“）
                                        尾巴
                                            push（）
                                                尾部添加n个元素
                                            pop（）
                                                删除尾巴
                                        头部
                                            unshift（）
                                                头插法
                                            shift（）
                                                删除头部
                                        改
                                            lst【0】 = 123
                                    获取
                                        ‘’.join（）
                                        slice（a,b）
                                            获取子数组
                                    concat()
                                        合并数组
                                    splice(pos,count, value)
                                        在pos剪切count个，补上value
                                    循环
                                        fruits.forEach((item, index, array) => {console.log(item, index);});
                                    排序
                                        sort()
                                        sort(function(a,b){return a-b})
                                        sort(function(a,b){return b-a})
                                    倒叙
                                        .reverse()
                                    复制
                                        const fruitsCopy = [...fruits];
                                        深拷贝

                                    解构
                                        var [one, two, three] = [1,2,3];
                                    flat()
                                        转为1维度的
                                    filter（func）
                                绑定属性
                                    [].a1 = 'qq'
                                Object
                                    创建
                                        let d1 = {a:1, b:2}
                                        let d1 = new Object()
                                            不推荐
                                    key类型
                                        String
                                        Symbol
                                    对象
                                        Object.create(dct)
                                        可以继承
                                        get
                                        set
                                    可以放置函数在内
                                        d1 = {func1(){}, var1:11}
                                    查增改删
                                        和python的字典一样
                                        delete person.abc
                                        定义构造函数
                                            ch = new Person('ch')
                                            构造函数大写字母开头
                                        原型链
                                            概念
                                                创建属性方法的东西
                                            定义构造函数后
                                                结构
                                                    prototype
                                                        constructor
                                                            定义的构造函数
                                                使用
                                                    Object.prototype.func1 = function(){{}
                                                        为所有对象创建属性，方法
                                                    函数名.prototype
                                                        为这个构造函数创建属性，方法
                                            使用方法
                                                Object.create({})
                                Map
                                    一种字典
                                        key 可以是任何值（函数，对象。。。）
                                        转json没有原生支持
                                    查
                                        get()
                                        keys()
                                        values()
                                        has()
                                        size
                                    set()
                                        增
                                        改
                                    删
                                        delete()
                                        clear()
                                    循环
                                        forEach(func)
                                Set
                                    集合
                                        去重
                                    查
                                        has()
                                    增
                                        add()
                                    删
                                        delete()
                                JSON
                                    dct = JSON.parse(jsonText)
                                    jsonText = JSON.stringify(dct)
                                    json格式
                                        只有属性，没有方法
                                        属性或字符串使用双引号
                        encodeURI()
                        decodeURI()
                        函数
                            创建
                                function () {}
                                const func1 = (x,y) => x-y;
                                    es6新写法
                                设置函数名
                                    function fun1（）{}
                                    var fun2 = function(){}
                            参数
                                获取函数的参数
                                    arguments
                                默认参数
                                    function multiply(a, b = 12) {return a * b;}
                                剩余参数
                                    ...theArgs
                            回调函数
                                函数声明作为另一函数的实参
                            IIFE
                                迭代器
                                    需要显式地维护其内部状态，不推荐
                                生成器函数
                                    function* foo() {  yield 1;  yield 2;  yield 3;}
                            异步
                                async
                                Promise
                                await
                                await Promise.all()
                                    并发执行
                        逻辑语句
                            分支
                                    if ...else if... else...
                                    (condition)？v1：v2
                                switch
                                    case :
                                        break;
                            循环
                                while
                                for
                                    遍历值
                                        for （let i of iter） {}
                                    遍历属性
                                        for （let k in iter） {}
                                    正序
                                        for(var i=0; i<str.length; i++)
                                    倒序
                                        for(var i=str,length-1; i>=0; i--)
                                do{}
                                    while();
                        异常处理
                            try... catch... finally...
                            throw...
                        作用域
                            局部变量在函数执行完毕后销毁。
                            全局变量在页面关闭后销毁
                                函数外定义的变量
                    导入模块
                        import { ... as ... } from "xxx.js"
                    类
                        class

                        封装
                            #属性
                            #方法
                        继承
                            extends

                    交互函数
                        console
                            log
                                日志
                                打印内容
                            table
                        document.write()
                            页面显示
        BOM
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

        DOM
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
    CDN
        是包含可分享代码库的服务器网络
    异步请求
        ajax
            jquery
                固定写法
            XMLHttpRequest()
                open（）
                send()
            promise
    js的库(框架)
        jQuery
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
