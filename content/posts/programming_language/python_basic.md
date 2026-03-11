+++
title = 'Python_basic'
subtitle = ""
date = 2024-09-18T15:15:14+08:00
draft = false
toc = true
series = ["Python"]
+++

## 应用场景

- 数据分析（几行代码处理Excel）
- Web开发（Flask/Django）
- 自动化脚本（批量处理文件、爬虫）
- AI/机器学习（最强生态）


## python 数据类型

和绝大多数的文件或编程语言一样

基础的: num str None
复杂的: list, dict, set

## python 函数中, 参数的定义顺序

```python
def func(
    pos1,              # 位置参数
    pos2,              # 位置参数
    pos3: int = 10,    # 带默认值的参数
    *args,             # 可变位置参数
    kw1,               # 关键字参数
    kw2: str = "test", # 带默认值的关键字参数
    **kwargs           # 可变关键字参数
):
    pass

```

## python 类知识点

```python


class Student:

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        
    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data["name"], age=data["age"])
    
    @staticmethod
    def is_valid_age(age: int) -> bool:
        return age > 0

    def say_hello(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def __repr__(self):
        # eval(repr(obj))
        
        return f"Student(name={self.name!r}, age={self.age})"
        
        # dct = {
        #     "name": self.name,
        #     "age": self.age
        # }
        # return f"Student.from_dict({dct})"
    


dir(Student)  # To see all attributes and methods of the class
print(Student.__mro__)  # Output: (<class '__main__.Student'>, <class 'object'>)


# 属性操作
hasattr()
getattr()
setattr()
delattr()

```


### f-string使用

数字 格式化

| 需求           | f-string (推荐)    |
| -------------- | ------------------ |
| 保留2位小数    | "f""{pi:.2f}"""    |
| 千位分隔符     | "f""{num:,}"""     |
| 百分比(1位)    | "f""{ratio:.1%}""" |
| 补零(总宽5)    | "f""{num:05d}"""   |
| 右对齐(总宽10) | "f""{num:>10}"""   |


### repr !r的用法

```python
import datetime

now = datetime.datetime.now()
print(f"Current time: {now}")  # 使用 str()
print(f"Current time (repr): {now!r}")  # 使用 repr()

```

## 多行import,  换行

```python
from .utils.helpers import (
    format_datetime,
    calculate_price,
    generate_order_number,
)
```


## except

```python
try:
    1/0
except Exception as e:
    print(e)
    raise e

```

## * 和 **

unpack
```bash
>>> a, b, *c = [1,2,3,3,4,5,6]
>>> a,b,c
(1, 2, [3, 3, 4, 5, 6])

>>> a, *b, c = [1,2,3,3,4,5,6]
>>> a,b,c
(1, [2, 3, 3, 4, 5], 6)
```

[] 和 {}
```python
# 列表合并
a = [1, 2]
b = [3, 4]
c = [*a, *b, 5]     # → [1, 2, 3, 4, 5]

# 字典合并
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
d3 = {**d1, **d2}   # → {'a': 1, 'b': 3, 'c': 4}
```

传参
```python
def add(a, b, c):
    return a + b + c

lst = [10, 20, 30]
print(add(*lst))




def greet(name, age):
    print(f"Hello {name}, you are {age}")

info = {"name": "Tom", "age": 18}
greet(**info)   # 等价于 greet(name="Tom", age=18)

```

## 多list

```bash
>>> from itertools import chain

>>> [i for i in chain([1,3,2], ['a','c','e'])]
[1, 3, 2, 'a', 'c', 'e']

>>> [i for i in zip([1,3,2], ['a','c','e'])]
[(1, 'a'), (3, 'c'), (2, 'e')]
```

## set操作

```python
A = {1, 2, 3}
B = {3, 4, 5}

print(A & B)   # {3}
print(A | B)   # {1, 2, 3, 4, 5}
print(A - B)   # {1, 2}
print(A ^ B)   # {1, 2, 4, 5}
```

其他常用
            -   collection.
                -   Counter()
                    -   统计个数神器
                    -   most_comon()
                    -   pop
                    -   update
                -   deque()
                    -   双端队列
                    -   1
                        -   append()
                        -   appendleft()
                    -   2
                        -   popleft()
                        -   pop()
                    -   clear()
                -   namedtuple
                    -   创建一个结构体的东西
                    -   不可修改
                    -   简单数据
                    -   方法
                        -   创建
                            -   \_make()
                            -   \_replace()
                                -   返回新实例
                        -   查看
                            -   \_asdict()
                                -   返回字典
                            -   \_fields
                                -   所有字段
                -   orderdict()
                -   defaultdict(lambda:"none")
                    -   为不存在的 key 设置默认值
            -   itertools.
                -   排列组合
                    -   排列
                        -   permutations（）
                            -   不放回，元素不重复
                        -   product（）
                            -   多组
                    -   组合
                        -   combinations
                            -   不放回，元素不重复
                        -   combinations_with_replacement()
                            -   多组
                    -   1
                        -   使用 for
                        -   使用 list()
                -   repeat()
                -   cycle()
            -   dataclass
                -   可以修改
                -   较复杂数据
