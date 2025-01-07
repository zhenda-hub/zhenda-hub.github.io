+++
title = 'Css Guide'
subtitle = ""
date = 2024-06-27T15:35:55+08:00
draft = false
toc = true
tags = ['web']
+++

## css选择器

- <https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Basic_selectors>
- <https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Attribute_selectors>
- <https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Styling_basics/Combinators>

## 常用属性

| 属性                  | 描述                                                         | 类型 |
|-----------------------|--------------------------------------------------------------| --- |
| `color`               | 设置文本颜色                                                  | `color` |
| `text-decoration`     | 设置文本装饰（如下划线、删除线等）                             |  |
| `text-align`          | 设置文本对齐方式                                               |  |
| `font-family`         | 设置字体族系                                                   | `font` |
| `font-size`           | 设置字体大小                                                   |  |
| `font-weight`         | 设置字体粗细                                                   |  |
| `line-height`         | 设置行高                                                       |  |
| `letter-spacing`      | 设置字符间距                                                   |  |
| `background-color`    | 设置背景颜色                                                   | `background` |
| `background-image`    | 设置背景图片                                                   |  |
| `background-size`     | 设置背景图片大小                                               |  |
| `margin`              | 外边距                                                     | `margin` |
| `padding`             | 内边距                                                     | `padding` |
| `border`              | 边框                                                       | `border` |
| `width`               | 设置宽度                                                       |  |
| `height`              | 设置高度                                                       |  |
| `display`             | 元素的显示方式（如block、inline、flex、none等）      | `display` |
| `position`            | 元素的定位方式（static、relative、absolute、fixed等）       |  `position`   |
| `top`, `right`, `bottom`, `left` | 设置定位元素的位置                                  | |
| `float`               | 设置浮动                                                       |  |
| `clear`               | 清除浮动效果                                                   |  |
| `flex-direction`      | 设置Flexbox布局的主轴方向                                      |  |
| `justify-content`     | 设置Flexbox布局主轴上子元素的对齐方式                            |  |
| `align-items`         | 设置Flexbox布局交叉轴上子元素的对齐方式                          |  |
| `grid-template-columns`, `grid-template-rows` | 设置Grid布局的列和行的大小和数量         |         |
| `grid-column`, `grid-row` | 设置Grid布局元素所占的列和行范围                             |  |
| `transition`          | 设置过渡效果                                                   |  |
| `animation`           | 设置动画效果                                                   |  |
| `box-shadow`          | 设置阴影效果                                                   |  |
| `overflow`            | 设置元素内容溢出效果(scroll, hidden, visible)                  | `overflow` |
| `opacity`             | 设置透明度                                                     | `opacity` |


## 布局

- <https://developer.mozilla.org/zh-CN/docs/Learn/CSS/CSS_layout/Introduction>
- <https://www.w3schools.com/Css/css_display_visibility.asp>
- <https://www.w3schools.com/Css/css_positioning.asp>

display
- block 块
- inline 行内
- none 隐藏

position
- static 默认位置
- relative 相对于默认位置
- absolute 相对于最近定位的祖先
- fixed  相对于视图

## 优先级

- 内联
- `#`
- `.`
- 类型(p, div)
- `*`

## 案例

分割线样式

```html
<hr style="height:2px;border:none;border-top:2px dotted #185598;" />
<hr style="height:1px;border:none;border-top:1px dashed #0066CC;" />
<hr style="height:1px;border:none;border-top:1px solid #555555;" />
<hr style="height:3px;border:none;border-top:3px double red;" />
<hr style="height:5px;border:none;border-top:5px ridge green;" />
<hr style="height:10px;border:none;border-top:10px groove skyblue;" />
```

链接 <https://www.yisu.com/jc/119190.html>