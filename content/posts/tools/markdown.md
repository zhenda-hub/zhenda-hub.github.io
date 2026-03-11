+++
title = 'Markdown'
subtitle = ""
date = 2024-05-25T15:47:33+08:00
draft = false
toc = true
tags = ['tools']
+++

<!-- [TOC] -->

## 参考链接

-   https://markdown.com.cn/basic-syntax/headings.html
-   https://mermaid.js.org/intro/

## 基础

-   标题
    -   # title
-   ## 无序列表
    -
    *
-   分割线
    -   ***
-   有序列表
    1. aaa
    1. bbb
-   取消 markdown 语法
    -   代码块
        -   多行代码
            ```python
            print('hello')
            ```
        - 单行代码 `cmd`
    -   转义
        -   \
-   字体
    - **字体加粗**
    - _斜体_
    - **_粗斜体_**
-   引用块
    > 法斯蒂芬森地方
    > 法斯蒂芬森地方
    > 法斯蒂芬森地方
    >> sdfsdfsdf
    >> sdfsdfsdf
    >>> sdfsdfsdf
-   换行
    -   <br>
-   注释
    -   <!--  fdgdfgfdgdf -->

## 进阶

-   图片
    -   ![img1](地址)
-   超链接地址
    -   [link1](地址)
    -   <a href="">link2</a>
-   表格
    | 左对其 | 居中 | 右对其 |
    | --- | :---: | ---: |
    | top1 | 1222222 | 2212 |
    |  | 6565 | 656565656 |
    | top2 | 6565 | 656565656 |
    |  | 6565 | 656565656 |
-   html
    -   设置各种 css 颜色
-   勾选框
    - [x] 添加停用词配置
    - [ ] 预览 背景混乱
-   数学公式
    -   $E = mc^2$
    -   $$E = mc^2$$

## 高级

Mermaid Diagram

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;

```

```mermaid
gantt
dateFormat  YYYY-MM-DD
title Adding GANTT diagram to mermaid
excludes weekdays 2014-01-10

section A section
Completed task            :done,    des1, 2014-01-06,2014-01-08
Active task               :active,  des2, 2014-01-09, 3d
Future task               :         des3, after des2, 5d
Future task2               :         des4, after des3, 5d

```

```mermaid
journey
    title My working day
    section Go to work
      Make tea: 5: Me
      Go upstairs: 3: Me
      Do work: 1: Me, Cat
    section Go home
      Go downstairs: 5: Me
      Sit down: 5: Me

```

```mermaid
sankey-beta

%% source,target,value
Electricity grid,Over generation / exports,104.453
Electricity grid,Heating and cooling - homes,113.726
Electricity grid,H2 conversion,27.14

```

```mermaid
---
title: Simple sample
---
stateDiagram-v2
    [*] --> Still
    Still --> [*]

    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]

```

```mermaid
flowchart TB
    A --> C
    A --> D
    B --> C
    B --> D

```

```mermaid
mindmap
Root
    A
        B
        C
    D
        E
        F
    Q
        Q1
        Q2
            1
            2
            3

```
