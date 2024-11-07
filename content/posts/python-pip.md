+++
title = 'Python Pip'
subtitle = ""
date = 2024-11-05T16:42:27+08:00
draft = false
toc = true
tags = ["Python"]
+++

python 工具 pip

用来安装第三方包

命令

|类别|命令|含义|
|---|---|---|
| 在线安装 | `pip install xxx` |  |
|  | `pip install -r requirements.txt` |  |
| 在线换源安装 | `pip config list` | 查看源 |
|  | `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xxx` | 换源 |
| 离线安装, 公司很多情况不联网 |  |  |
| tar.gz | `tar -xzvf xxx.tag.gz && cd xxx && pip install .` |  |
| whl | `pip install xxx.whl` |  |
| tar.gz或whl | `pip install --no-index --find-links=xxxx/packages/ -r requirements.txt` | 使用requirements.txt 批量安装包 |
| 其余 | `pip freeze > requirements.txt` |  |
|  | `pip uninstall xxx` |  |
|  | `pip install -u xxx` |  |
|  | `pip check` |  |
