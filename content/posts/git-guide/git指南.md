+++
title = 'Git资源'
subtitle = ""
date = 2024-01-08T23:37:30+08:00
draft = true
toc = true
tags = ["git", "tools"]
+++

## 官方文档: <https://git-scm.com/book/zh/v2>

## git 原理

-   以 commit 节点为根基
-   各个分支实际上是可移动的指针
    -   创建删除非常轻量
-   当前 commit 为 HEAD
-   远程仓库部署在服务器中，供用户访问
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
    -   pull request
-   检查代码
    -   review pr

## 环境搭建

-   基础

    -   下载 git软件
    -   配置个人信息
        ```bash
        # 查看 git 信息
        git config -l
        # 编辑个人信息来显示提交记录
        git config --global user.name "Your Name"
        git config --global user.email "Your Email"
        ```
    -   ssh
        -   作用
            -   免密码 pull push 代码
        -   安装后，配置密钥
            -   ssh-keygen -t rsa -C '你的邮箱地址'
                -   生成 ssh
        -   在网站创建远程仓库
            -   添加 pub 的 ssh
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

## git 使用方法

-   基础
    -   .gitignore
        
        -   .gitignore文件编辑的规则
            ```
            # 忽略.log 结尾的文件
            *.log
            # 忽略.vscode文件夹
            .vscode/
            # 多级目录下的 config
            **/config
            # 只忽略根目录下的 fd
            /fd/
            ```
        -   相关命令
            ```bash
            # 查看是否被忽略
            git check-ignore -v 文件
            # 删除远程仓库
            git rm-r -cached 文件名
            ```    
    -   增删改查
        -   查
            -   git log
                -   和远程提交记录一致
                -   参数
                    -   --stat
                        -   简略文件
                    -   -p
                        -   详细信息
                    -   --graph
                        -   提交图
                -   查看操作
                    -   e
                    -   y
                    -   q
                        -   退出
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
                    -   开发了一半
                        -   git stash && git stash drop
                        -   git stash save 'xxx'
                        -   git stash pop
                        -   git stash list
                            -   git stash clear
                -   本地提交
                    -   撤销远程提交
                        -   git revert id1 id2
                    -   git commit -m ''
                        -   提交格式
                            -   功能（作用域）：描述
                            -   type
                                -   个人
                                    -   add： xxx
                                    -   delete： xxx
                                    -   update
                                    -   refactor：
                                        -   重构
                                    -   fix：
                                        -   改功能
                                    -   revert
                                        -   撤销提交
                                -   添加
                                    -   feat
                                    -   test
                                    -   docs
                                    -   ci
                                -   后加！
                                    -   表示不兼容
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
    -   指定文件
        -   拉去指定文件
            -   git checkout 分支名 文件名
        -   查看指定文件提交历史
            -   git reflog 文件名
        -   回退旧版本
            -   git checkout commitid 文件名
        -   回到最新版
            -   git checkout HEAD 文件名
    -   标签
        -   概念
            -   一个标签，一个提交版本
        -   查
            -   git tag
                -   查看所有 tag
            -   git show tag 名
                -   查看详情
        -   增删
            -   git tag -a 版本名 -m''
                -   任何一次提交后，都可以创建 tag
                    -   tag 很稳定，保持和提交点一致
                -   创建 tag
                -   命名规则
                    -   v1.0.0-20230525
            -   git tag -d 版本名
                -   删除标签
        -   git checkout tag 名
            -   切换到 tag 和分支一样
        -   远程仓库交互
            -   git pull --tags
            -   git push --tags
-   进阶
    -   子模块
        -   使用场景
            -   一个仓库内嵌套另一个仓库，需要维护好总的仓库
        -   作用
            -   管理好嵌套结构
        -   标志文件
            -   .gitmodules
        -   命令
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

## ci/cd

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
