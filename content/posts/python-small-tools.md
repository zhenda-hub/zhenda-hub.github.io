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


## 环境变量

```bash
pip install python-dotenv
# .env
```

```python
import os

os.environ
os.getenv('')
```




## 数据类型工具

| 工具 / 库                 | 特点                                         | 适用场景                  | 优点                                  | 缺点                          |
| ---------------------- | ------------------------------------------ | --------------------- | ----------------------------------- | --------------------------- |
| **`dataclass`**        | 简单，标准库自带，自动生成常用方法（如 `__init__`，`__repr__`） | 用于简单的数据容器，数据类模型       | 简洁、轻量，自动生成代码，支持不可变实例（`frozen=True`） | 对复杂逻辑支持较弱                   |
| **`attrs`**            | 更强大的功能，支持字段验证，类型转换，默认工厂函数等                 | 需要更多自定义功能的类，如验证和转换    | 非常灵活，支持字段验证，性能优化                    | 需要第三方依赖，语法较 `dataclass` 稍复杂 |
| **`NamedTuple`**       | 轻量、不可变，适用于简单的元组类                           | 适合非常轻量级的数据容器，尤其是不可变类型 | 轻量，不可变数据结构                          | 功能受限，适用场景比较狭窄               |
| **`pydantic`**         | 强大的数据验证与序列化功能，适合用于 Web 框架                  | Web 开发，复杂数据模型和配置管理    | 数据验证强大，支持 JSON 序列化与反序列化             | 性能较慢，不适合简单的数据结构             |
| **`dataclasses-json`** | 扩展 `dataclass`，添加 JSON 序列化与反序列化支持          | 简单数据类需要 JSON 处理场景     | 基于 `dataclass`，添加 JSON 支持，轻量        | 仅限于 JSON 处理，功能较为单一          |


