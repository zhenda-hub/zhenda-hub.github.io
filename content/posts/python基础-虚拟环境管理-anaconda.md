+++
title = 'Python基础 虚拟环境管理 Anaconda'
date = 2023-11-23T21:49:57+08:00
draft = true
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

管理python虚拟环境方法很多，我们在此分享知名的anaconda

### conda重要命令汇总

#### 虚拟环境管理

1. 查看所有环境和当前环境(前面有*标记的)： __conda info --envs__
2. 切换并进入环境： __conda activate 环境名__
3. 退出环境： conda deactivate
4. 创建指定版本的python环境： __conda create --name 环境名 python=3.9__
5. 删除环境：__conda remove --name 环境名 --all__

#### 环境中的包管理

1. 查看包的信息： __conda list__
2. 安装包： conda install 包名.  安装了pip之后可以使用：__pip install 包名__
3. 卸载包： conda remove 包名
4. 更新所有包到最新的兼容版本： __conda update --all__

#### 导入导出环境包

1. 导出当前环境的包：__conda env export > freeze.yml__
2. 导入, 注意防止环境名重复：__conda env create -f freeze.yml__