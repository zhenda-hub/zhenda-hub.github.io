+++
title = 'Python基础 虚拟环境管理 Anaconda'
date = 2023-11-23T21:49:57+08:00
draft = false
toc = true
tags = ["Python"]
+++

### python虚拟环境的必要性

背景：在我们实际开发的python项目，因为常常依赖第三方库，并且第三方库之间的版本也需要相互兼容，程序才可以正常执行。

痛点：

1. 只使用一个环境运行所有python项目时，会出现版本不兼容的问题。
2. 当第三方库很多，不便于项目迁移和部署。

方案：使用python虚拟环境。

### python虚拟环境的基本原理

1. python程序和一般电脑上的程序不同，一般程序只能安装一次，但是python程序可以 __多次安装在系统的不同位置，不同位置的python程序可以安装各自的第三方包__
2. 使用运行python程序中的activate文件，可以修改 __操作系统的环境变量__(让操作系统知道我们想用的程序在哪)，来使用不同位置的python程序

---


<!--
| 工具    | 特点          | 使用场景                                      |
|---------|---------------|-----------------------------------------------|
|---------|---------------|-----------------------------------------------|
-->

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

