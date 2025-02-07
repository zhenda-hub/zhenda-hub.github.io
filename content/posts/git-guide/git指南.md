+++
title = 'Git资源'
subtitle = ""
date = 2024-01-08T23:37:30+08:00
draft = false
toc = true
tags = ["git", "tools"]
+++

<!-- [toc] -->

## 官方文档

<https://git-scm.com/book/zh/v2>

## git 重要概念

-   commit
    -   以 commit 节点为根基, 记录历史, 当前 commit 为 HEAD
-   branch
    -   分支实际上是可移动的指针, 代表一系列commit
    -   用于并行开发
    -   创建删除非常轻量
-   代码仓库
    -   远程仓库
        -   部署在服务器中，供用户访问
    -   本地仓库
        -   信息都存放在 **.git文件夹** 里面，  **.git文件夹** 所在的文件夹就是仓库

## git 远程仓库平台

-   github

    -   最强大的国际git平台，海量的优秀仓库
    -   actions
        -   CICD
    -   pages

        -   静态网页部署
        -   编写 md 发布到全网

    -   railway
        -   部署 web 项目

-   gitlab
    -   支持自建远程仓库
        -   https://docs.gitlab.com/ee/update/package/#upgrade-using-the-official-repositories
    -   ci/cd

-   gitee

    -   国内使用方便
    -   CICD
        -   需要自己弄服务器


## 大体流程

![流程图](../imgs/git-liucheng.jpg)

-   工作区
-   本地仓库
-   远程仓库

## 参与开源项目

-   提交 issue
-   提交代码
    -   fork
    -   在分支编写代码
    -   pull request
-   检查代码
    -   review pr

## 环境搭建

```bash
# 克隆
git clone 远程的 ssh
# 初始化
git init
git remote add origin sshxxx
git push --set-upstream origin main
```



## git 使用方法

### .gitignore

作用: 设置忽略跟踪的文件或文件夹

.gitignore文件编辑的规则:

```bash
# 忽略.log 结尾的文件
*.log
# 忽略.vscode文件夹
.vscode/
# 多级目录下的 config
**/config
# 只忽略根目录下的 fd
/fd/
```

命令

```bash
# 查看是否被忽略
git check-ignore -v 文件
# 删除远程仓库
git rm-r -cached 文件名
```


### branch

**一个功能: 一个branch, 多个commit**

```bash
# 命名
main  # 分支保护, 稳定可发布的分支
dev
origin/xxx-bbb

feature/xxx-bbb
fixbug/xxx-bbb
refactor/xxx-bbb
docs/xxx-bbb

backup/xxx-bbb
tmp/xxx-bbb
```

```bash
# 本地feature1分支, 同步 远程dev分支 的最新更改
git pull --rebase origin dev
```

```bash
# cherry-pick 合并特定commit
git checkout main
git cherry-pick commitidxxxx
# 有冲突
git add xxx
git cherry-pick --continue 
# 取消 operation
git cherry-pick --abort
# skip patch
git cherry-pick --skip
```


pull request: 开发分支发起对主分支的合并请求

### tag

tag 很稳定

通常对main分支的commit, 创建 tag

命名规则: v1.0.0-20230525


```bash
# 查所有
git tag
# 查详情
git show tag 名
# 增加
git tag -a 版本名 -m''
# 删除
git tag -d 版本名

# 切换, 和分支一样
git checkout tag 名

# 远程仓库交互
git pull --tags
git push --tags
```

### 保持完美提交的方法

提交格式

功能（作用域）：描述

功能:

| 功能名称 | 含义 |
|---|---|
| refactor | 重构 |
| fix | 改功能 |
| revert | 撤销提交 |
| feat | 新功能 |
| test | 测试 |
| docs | 文档 |
| ci | ci流水线 |
| xx! | 表示不兼容 |


个人使用

-   add： xxx
-   delete： xxx
-   update
              


```bash

# git rebase 整理 本地commit
git rebase -i commitid
git rebase -i HEAD~3

git rebase --continue
git rebase --abort
git rebase --skip
```

```vim
pick 2a923b73 fix: conf
pick b5b06654 remove: entrypoint.sh

# Rebase 5aa07cc4..b5b06654 onto 5aa07cc4 (2 commands)
#
# Commands:
# p, pick <commit> = use commit
# r, reword <commit> = use commit, but edit the commit message
# e, edit <commit> = use commit, but stop for amending
# s, squash <commit> = use commit, but meld into previous commit
# f, fixup [-C | -c] <commit> = like "squash" but keep only the previous
#                    commit's log message, unless -C is used, in which case
#                    keep only this commit's message; -c is same as -C but
#                    opens the editor
# x, exec <command> = run command (the rest of the line) using shell
# b, break = stop here (continue rebase later with 'git rebase --continue')
# d, drop <commit> = remove commit
# l, label <label> = label current HEAD with a name
# t, reset <label> = reset HEAD to a label
# m, merge [-C <commit> | -c <commit>] <label> [# <oneline>]
# .       create a merge commit using the original merge commit's
# .       message (or the oneline, if no original merge commit was
# .       specified); use -c <commit> to reword the commit message
#
# These lines can be re-ordered; they are executed from top to bottom.
#
# If you remove a line here THAT COMMIT WILL BE LOST.
#
# However, if you remove everything, the rebase will be aborted.
```

## 常用备忘内容

```bash
# 比较文件内容
git diff
git diff commitidxxx -- ./path1/path2/xxx.py

# 查看commit

# e y 上下 , q 退出
git log --stat
git show commmitid
```

```bash
# 修改上次commit
git commit --amend -m ""

# 撤销提交记录
git reset --hard xxx

git push -f


# 空提交, 为了触发自动化动作
git commit -m "retrigger checks" --allow-empty


# 撤销工作区的文件
git checkout xxx.py
# 撤销指定文件的add状态
git reset xxx.py
# 撤销add状态
git reset
# 撤销 commit 到 add
git reset --soft id
# 撤销 commit 到 0
git reset --hard id


# 开发了一半
git stash && git stash drop
git stash save 'xxx'
git stash pop
git stash list
git stash clear


# 指定文件
# 拉去指定文件
git checkout 分支名 文件名
# 查看指定文件提交历史
git reflog 文件名
# 回退旧版本
git checkout commitid 文件名
# 回到最新版
git checkout HEAD 
```



## 其他

### 子模块

使用场景: 一个仓库内嵌套另一个仓库，需要维护好总的仓库

作用: 管理好嵌套结构

标志文件: .gitmodules

命令:

```bash
# 一次性 clone 包括子仓库的主仓库
git clone --recurse sshxxxx
# 查看状态
git submodule status
# 详细状态
git submodule summary
# 添加
git submodule add sshxxx <not existed path>
# 删除
git submodule remove <path>
# 批量更新
git submodule update --remote
#
git submodule init
# 对子模块批量操作
git submodule foreach 命令
# 对子模块批量操作
git submodule update --remote --rebase
```

### ci/cd

-   概念
    -   自动测试/自动部署
-   实现原理
    -   使用命令自动化执行任务
-   流程
    -   工具
        -   travis ci
        -   github
            -   actions
                -   自动推送
        -   gitee
        -   gitlab
    -   配置文件
    -   触发条件
        -   提交代码
        -   定时
-   ci
    -   开发和代码前通过测试用例
    -   yaml
        -   stages
        -   beforescript
            -   stage
            -   script
                -   test1
                -   test2
            -   tags
            -   artifacts
                -   when
                    -   on_success
                    -   always
                -   paths
            -   allow_failure
            -   retry
                -   2
            -   only
-   cd
    -   推送部署
        -   服务器
        -   第三方平台
    -   回滚


### 使用ssh, 免密码访问

1. 创建密钥

```bash
# 生成 ssh
ssh-keygen -t rsa -C '你的邮箱地址'

# 测试连接
ssh -T git@github.com

```

2. 添加 ssh 公钥 (pub) 到代码仓库 github 或 其他平台

#### 问题

SSH 默认使用端口 22, 如果网络阻止访问, 可以改为 443

~/.ssh/config
```plaintext
Host github.com
    Hostname ssh.github.com
    Port 443
```



```

-   基础

    -   下载 git软件
    -   配置个人信息
        ```bash
        # 查看 git 信息
        git config -l
        # 编辑个人信息来显示提交记录
        git config --global user.name "Your Name"
        git config --global user.email "Your Email"
        git config --global core.autocrlf false
        ```
    -   ssh
        -   作用
            -   免密码 pull push 代码
        -   安装后，配置密钥
            -   ssh-keygen -t rsa -C '你的邮箱地址'
                -   生成 ssh
        -   在网站创建远程仓库
            -   添加 ssh 公钥 (pub)
            -   仓库名后缀
    -   创建远程仓库

        -   命名规则
            -   小写字符，中横线
        -   开源协议类型
            -   ![开源协议](../imgs/licenses.jpg)

    -   创建本地仓库

        ```bash
        # 克隆，初始化二选一
        # 克隆
        git clone 远程的 ssh
        # 初始化
        git remote add origin sshxxx
        git push --set-upstream origin main
        ```

        -   最好使用英文，方便国际化仓库
        -   主要 md 文件
            -   README.md 介绍项目
            -   CHANGELOG.md 更新日志
            -   CODE_OF_CONDUCT.md 代码准则
            -   CONTRIBUTING.md 贡献指南

    -   远程和本地关联
        ```bash
        # 查看关联
        git remote -v
        # 关联
        git remote add origin 远程的 ssh
        # 取消关联
        git remote rm origin
        # 直接设置
        git remote set-url origin xxx
        ```

-   进阶
    -   多个远程仓库关联
        -   fork
            -   获取别人远程仓库，创建一个副本仓库
            -   命令
                -   建立联系
                    -   查
                        -   git remote -v
                    -   增
                        -   git remote add upstream xxxx
                            -   添加上游仓库
                    -   改
                        -   git remote set_url upstream xxxx
                    -   删
                        -   git remote remove upstream
                -   拉代码
                    -   git fetch upstream
                    -   git pull upstream dev
                -   推代码
        -   pull request
            -   发给别人远程仓库进行代码合并

    -   增删改查
            -   git reflog 分支名
                -   按照分支查询
                    -   越往下 越老版本
        -   撤回
            -   git reset
                -   版本号
                -   HEAD~1
            -   git reset --hard
                -   版本号
                -   origin/分支名
        -   增删改
            -   本地仓库
                -   看修改内容
                    -   git status
                        -   查看暂存区
                    -   查看区别
                        -   比较分支
                            -   git diff 分支 1 分支 2 文件路径
                            -   git diff 要比较的分支
                            -   git diff branch1 branch2 --stat
                        -   比较 commit
                            -   git diff commitid1 commitid2
                        -   git diff
                            -   工作区和暂存区区别
                        -   git diff --cached
                            -   本地仓库和暂存区区别
                -   编辑
                    -   新建
                        -   git add
                            -   .
                                -   所有文件
                            -   文件名
                    -   删除文件
                        -   保留工作区的文件
                            -   git rm -r --cached .
                                -   远程仓库上传错了，就用这个删除
                            -   git rm --cached 文件
                        -   git rm -f 文件名
                    -   撤销
                        -   撤销工作区操作
                            -   git checkout -- .
                                -   工作区不要了
                            -   git checkout -- 文件名
                        -   撤销暂存区 add
                            -   git reset
                        -   撤销 commit 到 add
                            -   git reset --soft id
                        -   撤销 commit 到 0
                            -   git reset --hard id
                -   本地提交
                    -   撤销远程提交
                        -   git revert id1 id2
                    -   git commit --amend -m“”
                        -   commit 写错了，重新提交
                    -   提交已经 git add 的文件, 不用再次 git add
                        -   git commit -am ''
            -   上传操作
                -   拉去最新远程代码
                    -   git pull --rebase origin 远程分支
                    -   git pull origin 远程分支
                        -   处理冲突
                            -   编辑代码重新提交 或 git rebase --skip
                        -   -u 表示默认远程分支
                    -   上传
                        -   git push origin 远程分支
                        -   git push --force
                            -   强制推送 reset 后的代码
                    *   git config --global push.default simple
                        -   设置默认
    -   分支
        -   概念
            -   master
                -   对外发布的版本，是主分支
            -   dev
                -   在测试版写，写好了放到 master
            -   其他分支
                -   按照功能或问题来创建分支
        -   每一次开发，创建一个分支，合入后删除分支
        -   需要远程共享代码时
            -   远程仓库和本地仓库的分支一致
            -   查看
                -   git remote prune origin
                    -   删除不存在的远程分支
                    -   git branch
                        -   查看本地所有分支
                        -   退出
                            -   q
                    -   git branch -r
                        -   查看远程分支
                    -   git branch -vv
                        -   查看分支的映射关系
                        -   git branch -u origin/xxx xxx
                            -   绑定本地分支和远程分支
                    -   git branch -a
                        -   查看本地和远程分支
            -   创建
                -   创建本地分支
                    -   git checkout -b 分支名
                        -   创建并切换分支
                    -   git branch 分支名
                        -   在这个分支基础上创建分支
                    -   有一个本地分支
                        -   git push -u origin 分支名
                            -   创建并绑定
                    -   有一个远程分支
                        -   git fetch
                        -   2 选 1
                            -   git checkout 同名的分支名
                            -   git checkout -b 本地分支 origin/远程分支
                                -   创建本地分支并拉取
                -   本地远程分支关联
                    -   git branch --set-upstream-to=origin/main main
            -   删
                -   删除本地分支
                    -   git branch -d 分支名
                -   删除远程分支
                    -   git push origin -d 分支名
            -   改
                -   切换分支
                    -   git checkout 想切换的分支
            -   合并
                -   git pull
                -   git merge 本地或远程分支名
                    -   保持最新代码！！！！！！！！！
                    -   需要保持一个版本差异
                    -   远程分支
                        -   origin/dev
                -   git rebase
            


```