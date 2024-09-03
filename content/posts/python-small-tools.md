+++
title = 'Python Small Tools'
subtitle = ""
date = 2024-06-03T13:06:57+08:00
draft = true
toc = true
tags = []
+++

-   其他小工具
    -   格式化
        -   json
        -   pprint
            -   pprint
            -   pformat
    -   性能测试
        -   line_profiler
            -   kernprof -l -v script_name.py
                -   生成结果
        -   cprofile
            -   python -m cProfile py 文件
                -   运行时查看性能
        -   py-spy
            -   可视化分析
    -   schedule
        -   各种定时任务
    -   argparser
        -   ArgumentParser()
            -   设置规则
                -   add_argument()
                    -   参数
                        -   参数类型
                            -   位置参数
                                -   xxx
                            -   可选参数
                                -   --xxx
                                -   -x
                                    -   短选项
                        -   设置相关
                            -   主要
                                -   type
                                -   help
                                -   default
                                -   choices=[1,2,3]
                                    -   规定参数范围
                            -   次要
                                -   action
                                    -   store
                                        -   默认存储
                                    -   布尔
                                        -   store_true
                                        -   store_false
                                        -   有参数则为标记值，否则为相反值
                                    -   列表
                                        -   append
                                            -   可多次调用传参
                                    -   计数
                                        -   count
                                -   dest
                                    -   指定属性名
                -   互斥组
                    -   parser.add_mutually_exclusive_group()
            -   parse_args()
        -   运行
            -   -h
                -   查看帮助
        -   作用
            -   命令行解析
        -   mkdocs
        -   sphinx
            -   docstring
                -   numpy
                -   google
            -   sphinx-quickstart
                -   创建
                -   设置分离
            -   make html
                -   创建
            -   make clean
                -   清除
            -   添加 html 文档
    -   python 和命令行
        -   python -m http.server 8888
            -   直接出网站
        -   python -m json.tool demo.json
            -   查看 json 文件
    -   mypy
