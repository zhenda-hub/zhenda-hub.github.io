+++
title = 'Python Import'
subtitle = ""
date = 2025-01-10T15:37:28+08:00
draft = false
toc = true
tags = []
+++



# python 中的 import

## 导包方式

```python
import xxx
import xxx as xxx2
from xxx import func1, func2
from xxx import *
```

相对导入
绝对导入



当前目录: 命令行执行的目录
导包目录: 被执行文件的目录会默认被加入pythonpath的第一个位置


包名， 文件名 要区分开



## 常见问题

### 导入失败

python import 失败
大概率是因为 项目根目录不在 pythonpath 里




解决方法:


1 使用 -m运行

```bash
python -m xxx.file
```

2. 添加 项目根目录到 pythonpath 里

2.1. 命令行解决

```bash
export PYTHONPATH=./
```

```cmd
set PYTHONPATH=./
```

```powershell

```

2.2. 代码解决

```python
import sys, os
sys.path.insert(0, os.cwd())
```


### 循环导入

解决方案:

重构项目结构, 在外层新建文件导入后使用

