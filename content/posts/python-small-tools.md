+++
title = 'Python Small Tools'
subtitle = ""
date = 2024-06-03T13:06:57+08:00
draft = true
toc = true
series = ['python']
+++

-   其他小工具
    -   格式化
        -   json
        -   pprint
            -   pprint
            -   pformat
    -   性能测试
        -   line_profiler
            -   kernprof -l -v script_name.py
                -   生成结果
        -   cprofile
            -   python -m cProfile py 文件
                -   运行时查看性能
        -   py-spy
            -   可视化分析
    -   schedule
        -   各种定时任务
    -   argparser
        -   ArgumentParser()
            -   设置规则
                -   add_argument()
                    -   参数
                        -   参数类型
                            -   位置参数
                                -   xxx
                            -   可选参数
                                -   --xxx
                                -   -x
                                    -   短选项
                        -   设置相关
                            -   主要
                                -   type
                                -   help
                                -   default
                                -   choices=[1,2,3]
                                    -   规定参数范围
                            -   次要
                                -   action
                                    -   store
                                        -   默认存储
                                    -   布尔
                                        -   store_true
                                        -   store_false
                                        -   有参数则为标记值，否则为相反值
                                    -   列表
                                        -   append
                                            -   可多次调用传参
                                    -   计数
                                        -   count
                                -   dest
                                    -   指定属性名
                -   互斥组
                    -   parser.add_mutually_exclusive_group()
            -   parse_args()
        -   运行
            -   -h
                -   查看帮助
        -   作用
            -   命令行解析
        -   mkdocs
        -   sphinx
            -   docstring
                -   numpy
                -   google
            -   sphinx-quickstart
                -   创建
                -   设置分离
            -   make html
                -   创建
            -   make clean
                -   清除
            -   添加 html 文档
    -   python 和命令行
        -   python -m http.server 8888
            -   直接出网站
        -   python -m json.tool demo.json
            -   查看 json 文件
    -   mypy


## random

```python
import random

random.random()
random.uniform(0,10)

random.randrange(0,3,2)
random.randint(0,9)

random.sample([1,2,3,4,5], k=4)  # 不可重复
random.choices([1,2,3,4,5], k=4)  # 可重复
random.choice([1,2,3])

l1 = [1,2,3,4,5]
random.shuffle(l1)
l1
```


## datetime

<https://docs.python.org/zh-cn/3/library/datetime.html#module-datetime>

```python
from datetime import datetime, timedelta

now = datetime.now()
gap = timedelta(days=1)
two = now + gap
print(two)
print(two.replace(day=1))

print(now.strftime("%Y-%m-%d %H:%M:%S"))

obj = datetime.strptime("2022-01-01 14:33:21", "%Y-%m-%d %H:%M:%S")
print(obj)
now.date()
now.time()


```