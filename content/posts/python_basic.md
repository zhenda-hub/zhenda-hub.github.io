+++
title = 'Python_basic'
subtitle = ""
date = 2024-09-18T15:15:14+08:00
draft = false
toc = true
series = ["Python"]
+++
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

## unpack

```bash
>>> a, b, *c = [1,2,3,3,4,5,6]
>>> a,b,c
(1, 2, [3, 3, 4, 5, 6])

>>> a, *b, c = [1,2,3,3,4,5,6]
>>> a,b,c
(1, [2, 3, 3, 4, 5], 6)
```

## 多list

```bash
>>> from itertools import chain

>>> [i for i in chain([1,3,2], ['a','c','e'])]
[1, 3, 2, 'a', 'c', 'e']

>>> [i for i in zip([1,3,2], ['a','c','e'])]
[(1, 'a'), (3, 'c'), (2, 'e')]
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
