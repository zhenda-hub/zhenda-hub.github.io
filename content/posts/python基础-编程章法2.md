+++
title = 'Python基础 编程章法2'
date = 2023-11-23T00:37:34+08:00
draft = true
toc = true
tags = ["Python", "Software Architecture"]
+++


[TOC]
今天继续分享一下自己的近期心得：

## python之禅

```bash
Python 3.10.11 | packaged by Anaconda, Inc. | (main, Apr 20 2023, 18:56:50) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import this
The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!
>>>
```

其中有两句很有启发：

1. **If the implementation is hard to explain, it's a bad idea. 如果代码实现很难解释，则是一个糟糕的想法。**

    编写代码，思路先行。没有思路，或思路混乱的话，写出来的代码注定是问题重重。
    我们可以**先写注释，后写代码**。这样思路会清晰

2. **Simple is better than complex. 简洁好于复杂。**

    有时候我们会遇到复杂多变的业务逻辑，但是能把复杂的业务逻辑用尽量简单的代码写出来（也需要考虑代码可读性），才是高手。这可能不是很容易，但这是我们需要追求的目标。

## 对于单一职责和复用性的思考

这两个原则都很重要，但是又有一些矛盾，我们应该怎么遵循它们呢？
单一职责的优势： 代码简单明确，易于维护
复用性的优势：提高开发效率，避免重复造轮子

有时候我们想自己编写一套可复用代码，方便开发人员的使用。 但是这需要对业务逻辑充分理解并合理的拆分， 横向对比各各框架，选择最适合的，还需要考虑后续的功能迭代和维护。因此这不是一件容易的事情。如果写的通用代码被广泛使用后，发现有更好的实现方式或通用功能设计不是很合理，需要迭代，那么迭代成本通常是很大的。而且编写通用的代码，可能不适应复杂多变的业务。会成为累赘。因此**不要急于提高复用性， 谨防过度设计**

建议项目初期**优先遵循单一职责**编写代码，经过深思熟虑后，再**慢慢提炼出可复用的代码**

其实，复用性是重构追求的一个要点，**项目需要不断的，小步的，缓慢进行。才能成为优质的项目**
