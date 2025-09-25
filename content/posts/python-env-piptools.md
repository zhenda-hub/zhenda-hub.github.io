+++
title = 'Python Env Piptools'
subtitle = ""
date = 2025-08-25T14:58:59+08:00
draft = false
toc = true
series = ['python']
+++

简易的, 适合python包管理工具

## pip-tools

```bash
pip install pip-tools

pip-compile requirements.in
# 会删除多余包, 包严格一致
pip-sync requirements.txt




# 更新依赖包 requirements.txt
pip-compile --upgrade


```



```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.in .
RUN pip install pip-tools \
    && pip-compile requirements.in \
    && pip-sync requirements.txt

COPY . .

CMD ["python", "main.py"]

```

## pipdeptree

```bash
pip install pipdeptree
# pipdeptree 默认是分析当前环境里的包
pipdeptree
```

