+++
title = 'Python_basic'
subtitle = ""
date = 2024-09-18T15:15:14+08:00
draft = false
toc = true
tags = ["Python"]
+++

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

## 多行import

```python
from .utils.helpers import (
    format_datetime,
    calculate_price,
    generate_order_number,
)
```