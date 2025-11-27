+++
title = 'Python基础 虚拟环境管理 Anaconda'
date = 2023-11-23T21:49:57+08:00
draft = false
toc = true
series = ["Python"]
+++

[toc]

## python虚拟环境的必要性

背景：在我们实际开发的python项目，因为常常依赖第三方库，并且第三方库之间的版本也需要相互兼容，程序才可以正常执行。

痛点：

1. 只使用一个环境运行所有python项目时，会出现版本不兼容的问题。
2. 当第三方库很多，不便于项目迁移和部署。

方案：使用python虚拟环境。

## python虚拟环境的基本原理

1. python程序和一般电脑上的程序不同，一般程序只能安装一次，但是python程序可以 __多次安装在系统的不同位置，不同位置的python程序可以安装各自的第三方包__
2. 使用运行python程序中的activate文件，可以修改 __操作系统的环境变量__(让操作系统知道我们想用的程序在哪)，来使用不同位置的python程序

---


<!--
| 工具    | 特点          | 使用场景                                      |
|---------|---------------|-----------------------------------------------|
|---------|---------------|-----------------------------------------------|
-->

## Python 包管理工具

工具层出不穷, 还没学会一个, 就来两个

| 工具             |     推荐等级 |                                         代表年份（首次出现 / 走红） | 备注 & 来源                                                    |
| -------------- | -------: | ------------------------------------------------------: | ---------------------------------------------------------- |
| **uv**         | ✔✔✔（最推荐） |                            **2024–2025**. ([GitHub][1]) | Astral 的新一代工具，2024 起公开活跃并在 2024–2025 年迅速流行。                |
| **Rye**        |    ✔（备选） | **2024**. ([Armin Ronacher's Thoughts and Writings][2]) | Armin/胴体团队 2024 年左右推出并宣传为“one-stop”方案。                     |
| **PDM**        |        ✔ |             **2020**（早期 2020 年开始活跃）. ([PDM Project][3]) | PDM 的 release/开发记录从 2020 年可见明显活动。                          |
| **Poetry**     |   部分场景适合 |                           **2018（初始发布）**. ([Poetry][4]) | 官方 history 显示 0.1.0 在 2018-02-28 发布。                       |
| **Hatch**      |     适合写库 |              **2017（项目起始） / v1 稳定版 2022**. ([Hatch][5]) | Hatch 项目自 2017 开始，v1 稳定重写并在 2022 年成为稳定主线。                  |
| **pip-tools**  |     老旧但稳 |                **2015（pip-tools 1.0）**. ([nvie.com][6]) | pip-tools 1.0 在 2015 年发布（pip-compile / pip-sync）。          |
| **pip + venv** |     基础水平 |            **pip 2008；venv（标准库）2013 前后普及**. ([维基百科][7]) | pip 最早可追溯到 2008，venv 随 Python3.x 标准化后在 2012–2014 逐步成为常用方案。 |

[1]: https://github.com/astral-sh/uv "GitHub - astral-sh/uv: An extremely fast Python package and project manager, written in Rust."
[2]: https://lucumr.pocoo.org/2024/2/4/rye-a-vision/?utm_source=chatgpt.com "Rye: A Vision Continued"
[3]: https://pdm-project.org/latest/dev/changelog/?utm_source=chatgpt.com "Changelog"
[4]: https://python-poetry.org/history/ "History | Poetry - Python dependency management and packaging made easy"
[5]: https://hatch.pypa.io/1.13/history/hatch/ "Hatch history - Hatch"
[6]: https://nvie.com/posts/pip-tools-10-released/ "pip-tools 1.0 released » nvie.com"
[7]: https://en.wikipedia.org/wiki/Pip_%28package_manager%29 "pip (package manager) - Wikipedia"


### conda常用命令, nice!

```bash
# 虚拟环境管理
# 查看所有环境和当前环境(前面有*标记的)
conda info --envs
# 切换并进入环境
conda activate 环境名
# 退出环境
conda deactivate
# 创建指定版本的python环境
conda create --name 环境名 python=3.9
# 删除环境
conda remove --name 环境名 --all

# 环境中的包管理
conda list
# 更新所有包到最新的兼容版本
conda update --all

# 导出环境包
conda env export > freeze.yml
# 导入, 注意防止环境名重复
conda env create -f freeze.yml
```

### venv

```bash                      
# 创建环境
python3 -m venv myenv         

# 激活环境
source myenv/bin/activate


# 安装包
pip install <package>         
```

```cmd
.venv\Scripts\activate
```



### pip-tools

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

### pipdeptree

```bash
pip install pipdeptree
# pipdeptree 默认是分析当前环境里的包
pipdeptree
```


### uv

<https://github.com/astral-sh/uv?tab=readme-ov-file>



```bash
# 指定python版本创建项目
uv init --python 3.9

# 管理包
uv add requests
uv remove requests

# 同步环境
uv sync                    # 第一次会创建 .venv

# 运行python
uv run python --version


# 和 requirements.txt 交互
uv add -r requirements.txt
uv export -o requirements.txt

# pylock.toml
uv export -o pylock.toml
```


### poetry

```bash
poetry new myproject
poetry add <package>
```


### pyenv

不太支持windows

| 命令                                 | 功能说明                                                         |
|-------------------------------------|------------------------------------------------------------------|
| `pyenv install <version>`           | 安装指定版本的 Python，例如 `pyenv install 3.9.7`                 |
| `pyenv uninstall <version>`         | 卸载指定版本的 Python                                            |
| `pyenv versions`                    | 列出已安装的所有 Python 版本                                      |
| `pyenv version`                     | 显示当前使用的 Python 版本                                        |
| `pyenv global <version>`            | 设置全局的 Python 版本，例如 `pyenv global 3.9.7`                  |
| `pyenv local <version>`             | 在当前目录设置本地的 Python 版本，例如 `pyenv local 3.8.5`         |
| `pyenv shell <version>`             | 为当前 shell 会话临时设置 Python 版本，例如 `pyenv shell 3.7.3`   |
| `pyenv rehash`                      | 重新生成 `shims`，每次安装或卸载 Python 版本后需要执行            |
| `pyenv which <command>`             | 显示当前 Python 环境中某个命令的绝对路径，例如 `pyenv which python`|
| `pyenv doctor`                      | 检查 pyenv 是否安装正确并配置好                                   |
| `pyenv update`                      | 更新 pyenv 本身及其插件                                           |

其他有用的插件命令

| 命令                                 | 功能说明                                                         |
|-------------------------------------|------------------------------------------------------------------|
| `pyenv virtualenv <version> <name>` | 创建一个基于指定 Python 版本的虚拟环境                            |
| `pyenv virtualenvs`                 | 列出所有使用 pyenv 创建的虚拟环境                                 |
| `pyenv activate <name>`             | 激活指定的虚拟环境                                                |
| `pyenv deactivate`                  | 退出当前的虚拟环境                                                |
