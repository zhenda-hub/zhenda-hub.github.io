+++
title = 'Front'
subtitle = ""
date = 2025-08-22T16:41:23+08:00
draft = true
toc = true
tags = []
+++

```
基础知识
    整体流程
        网站
            前端
            服务器端
                后端
                数据库
    网络传输三大基石
        URL
            网址
                协议
                    HTTP协议
                    FTP协议
                host
                    本地主机
                        127.0.0.1
                        0.0.0.0
                            本地任意ip
                port
                路径
                    HTML(超文本标记语言)
        协议
        HTML(超文本标记语言)
心得
    前端代码就是拼积木，调样式
    设计布局
    设计控件
三层
    结构层
        HTML
            显示页面的语言
                标记
                    类型
                        双标记
                            <word>
                            </word>
                        单标记
                            <word/>
                    标准结构
                        <html>
                            文件类型
                        <head>
                            页面配置信息
                                title
                                    设置页面的名字
                                lang
                                    zh-CN
                                meta
                                    charset = "utf-8"
                                    name context
                                        author
                                        description
                                        keywords
                                    跳转页面
                                        http-equiv = "refresh"
                                link
                                    引入外部资源
                                        引入css

                        <body>
                            内容
                                    文字
                                        空格
                                            &nbsp;
                                                英语
                                            &emsp;
                                                中文
                                        标题
                                            <h1>~<h6>
                                        段落
                                            <p>
                                                中间空一行
                                        字体
                                            font
                                                color
                                                size
                                    分割线
                                        <hr>
                                            width
                                                300px
                                                    像素为单位
                                                30%
                                                    浏览器的30%的宽度
                                            align
                                                right
                                                left
                                                center
                                    超链接
                                        <a >
                                            作用
                                                跳转页面
                                                设置锚点
                                                下载文件
                                                交互js
                                            href
                                                跳转路径
                                                    填写url
                                                    填写本地文件
                                                跳转锚点
                                                    “#id”
                                                        绑定id
                                            target
                                                _blank
                                                    新建打开
                                                _self
                                                    覆盖打开
                                            download
                                                指定下载链接
                                            name
                                                过时的
                                    图片
                                        <img>
                                            src
                                                本地路径，网上路径

                                                相对路径
                                                    ./abc.png
                                                绝对路径
                                            width
                                            height
                                            alt
                                                加载失败提示语
                                            title
                                                提示
                                    音视频
                                        <embed>
                                            src
                                                路径
                                            width
                                            height
                                        video

                                        audio
                                    列表
                                        无序列表
                                            <ul>
                                                <li>
                                                type
                                        列表嵌套

                                        有序列表
                                            <ol>
                                                <li>
                                                type
                                                start
                                    表格
                                        <table>
                                            <caption>
                                                标题
                                            属性设置
                                                border
                                                    1
                                                cellspacing
                                                    0
                                                bgcolor
                                                align
                                                合并
                                                    colspan
                                                    rowspan
                                            <table border="1" style="border-collapse: collapse;">
                                                边框变一条线
                                            基本使用
                                                <tr>
                                                    列数据
                                                    <th>
                                                        标题
                                                            加粗，居中
                                                    <td>
                                                        行数据
                                            进阶使用

                                <input>
                                    各个参数
                                        核心功能
                                            type
                                                file
                                                    文件上传
                                                登录
                                                    text
                                                    password
                                                按钮
                                                    radio
                                                        name相同才可以单选
                                                        value需要给值
                                                        checked
                                                            默认选中
                                                    checkbox
                                                        复选框
                                                    reset
                                                        恢复页面
                                                    按钮
                                                        <button>
                                                            type
                                                                submit
                                                                    默认值
                                                                button
                                                        submit
                                                            提交按钮
                                                    image
                                                search
                                                    搜索框
                                                hidden
                                                    隐藏内容
                                                    email
                                                    url
                                                    date
                                                    time
                                                number
                                                    min
                                                    max
                                                    step
                                                    value
                                                    数字
                                                color
                                            name
                                            value
                                                键值对：name = value
                                                显示内容
                                        placeholder
                                            提示语
                                        class
                                        id
                                            规定必须独一无二的
                                        权限
                                            disable
                                            readonly
                                        required
                                            设置为必填信息
                                        autofocus
                                            默认光标焦点
                                form表单
                                    作用
                                        把前端获取的数据打包发给后端
                                    <form>
                                        提交信息的参数
                                            method
                                                get
                                                    可见
                                                    快.
                                                    数据长度有限
                                                post
                                                    不可见
                                                    慢
                                                    数据长度无限制
                                            传输文件
                                                要在<form>中加参数
                                                    enctype="multipart/form-data"
                                                        设置连续不间断的字节流
                                            action
                                                提交地址
                                                默认提交当前url
                                            onsubmit="return fun1()"
                                                作用
                                                    表单验证
                                                使用js函数来做数据校验
                                                点击提交后到这里
                                        name
                                            有name才能传到服务端， name一定要写！！！！！
                                            name可以相同
                                        表单各个元素
                                            label
                                                作用
                                                    绑定光标焦点,移动到id的元素上
                                                使用
                                                    for=“id”
                                                        绑定其他的id
                                            元素
                                                <select>
                                                    下拉选择
                                                        name
                                                        <option>
                                                            value
                                                                往后端传的实际数据！！
                                                            selected
                                                                默认选择
                                                        multiple
                                                            可多选
                                                textarea
                                                    文本框
                                            换行
                                                <br>
                                内嵌框架
                                    iframe
                                        必须设置
                                            height
                                            width
                                        name
                                        src
                                            引用其他页面
                        <frameset>
                            框架集合：可以随意分割页面
                            frame
                            设置方式
                                cols
                                rows
    样式层
        CSS
            注释
                /*xxx*/
            CSS（层叠样式表）
                命名规则
                    abc-dbd
                分类
                    内联样式
                        style""
                    内部样式
                        在<head>里面写
                            <style></style>
                                选择器{样式}
                    外部样式
                        导入
                            在<head>里面写
                                <link>
                                    连接css文件
                        书写
                            选择器{样式}
                    三种方式相互覆盖，最近的样式起作用
                结构
                    选择器
                        分类
                            基本选择器
                                优先级
                                    id>class>标签
                                    id
                                        #
                                        不能是数字！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
                                    类名
                                        .
                                    标签
                                        div{}
                                            div标签
                                        div a{}
                                            div下的a标签
                                    设置所有
                                        *
                            关系选择器
                                结构
                                    布局相关
                                        <div>
                                            包含整行
                                            组建网页的大模块
                                            属性
                                                class
                                                id
                                                    align
                                                        center
                                                    style
                                                        width
                                                            px
                                                                像素
                                                            %
                                                                相对于父元素的百分比
                                                        height
                                                    title
                                        <span>
                                            指定行内元素
                                        可通过border设置查看
                                    (dir/span) 基本选择器
                                        后代选择
                                    (dir/span)>基本选择器
                                        儿子选择
                            属性选择器
                                标签[]
                                    选择特定的
                            伪类选择器
                                在超链接使用
                                    记住这个先后顺序
                                        link
                                        visited
                                        hover
                                        active
                    常用属性
                        background-color
                        color
                        text-align: center
                            文字居中
                        margin
                        border: 1px solid red
                            宽度 样式 颜色
                        border-radius: 10px
                            圆角
                        box-shadow: 11px 24px 15px #ABD
                            阴影
                            左右， 上下， 模糊度， 颜色
                            内部阴影
                                inset
                        padding
                    布局
                        display
                            inline
                            block
                            flex
                                子元素改为一行
                            grid
                                子元素改为网格
                                grid-gap
                                grid-column: 2 / 4;
                                grid-row: 1;
                        float
                            目的
                                文字环绕图片
                                使对象浮动到上层
                                    好像是立体的
                            类型
                                left
                            消除对后面对象的影响
                                对设置float的地方
                                    设置height
                                    overflow：hidden
                                对被影响的地方
                                    clear:both
                        position
                            概念
                                定位
                            static
                                默认
                                relative
                                    相对默认位置，反方向移动
                                        left:100px
                                        top:100px
                                    z-index
                                        垂直平面的距离
                                absolute
                                    绝对定位
                                        逻辑
                                            找父级的已经定位的元素，直到<body>
                                        使用
                                            一般在父级设置relative定位，使得小部件设置在大范围内的绝对位置
                                fixed
                                    相对于 浏览器显示的窗口定位
                                    设置
                                        top
                                        bottom
                                        right
                                        left
                                sticky
                                    从
                    响应式
                调试
                    直接浏览器找到css
                        调试数据
                盒子模型
                    结构图
                            margin
                                外
                                居中设置！！
                                    margin-left
                                        auto
                                    margin-right
                                        auto
                            border
                                边
                            padding
                                内
                    注意事项
                        子类元素不能设置margin
                        父类设置了padding后，会变大，应把宽高缩小
    行为层
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

单页
    优点

bootstrap
    环境搭建
        下载官方文件
            bootstrap
            jquery
        导入文件
            css
                <link href="">

            js
                <script src="">

    版本选择
        3
        4
        5
    特点
        侧重移动端
            响应式布局
    layout
        布局容器
                class="container"
        自适应浏览器的宽度
            栅格系统
                基本概念
                    row
                    col
                        列间隙
                            offset
                        列移动
                            pull
                            push
                        列嵌套
                            每一列还可以继续分为12份
        无网格类

    content
        混合
            面板
        单一
            图片
            表格
                hoverable rows
                    可悬停！！
                    <table class="table table-hover">  ...</table>
    表单
        check
        radio
        select
        上传
            打开文件
            打开文件夹
        验证
    components
        alert
            button
                悬停状态
            tooltips
                按钮提示内容
        分页
        carousel
            大屏多图切换
        dropdown
            下拉框
        navbar
            导航栏
            头部固定！！！
        progress
            进度条
                标签
                    显示内容
        scrollspy
            侧边锚点
    做法
        工具网站
            layoutit！！！！
                生成页面 直接下载
        直接去官网抄组件
        找好的页面查看源代码
        找css js， copy下来
框架
    npm
        配置源
            get registry
            config set registry 地址
        list
        -v
            查看版本
        install 模块名
            安装
        update 模块名
            更新
        uninstall 模块名
            卸载
        init
        view 模块名 version
        run serve
            运行项目
    vue
        先安装 npm 后安装 vue
        -v
            查看版本
        create 项目名
            创建项目
font awosome
    图标库
其他
    Hbulider
        复制
            ctrl，shift，r
        注释
            ctrl，shift，/
    vscode
        插件
            css peek
                找到 css
            open in browser
                打开
            html css support
                提示css
                添加设置

    注释
        ctrl， /
            <!-- -->
    长宽像素
        1900
        950
```