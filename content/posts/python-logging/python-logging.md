+++
title = 'Python Logging'
subtitle = ""
date = 2024-06-03T12:52:52+08:00
draft = true
toc = true
tags = []
+++

-   loguru
    -   add（“log1.log”）
        -   记录文件
    -   logger
        -   直接用
            -   exception（）
                -   代替 error（）

*   logging
    -   日志作用
        -   查看程序运行状态
        -   了解用户偏好
    -   多进程下
        -   可能会出问题
        -   debug
            -   调试信息
        -   info
            -   正常运行信息
        -   warning
            -   有异常，但正常运行
        -   有异常，异常运行
            -   exception
                -   自动打印堆栈信息
            -   error
                -   错误信息
                    -   不会显示错误原因
        -   critical
    -   设置一次，到处使用（单例模式）
        -   设置
            -   显式设置
                -   1. logger = logging.getlogger(\_\_name\_\_)
                -   Formatter
                    -   ![formatter1](../imgs/formatter1.jpg)
                    -   ![formatter2](../imgs/formatter2.jpg)
                    -   全能
                        -   '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
                    -   常用
                        -   levelname
                        -   %(asctime)s
                        -   1
                            -   %(filename)s
                            -   %(pathname)s
                            -   %(funcName)s
                        -   %(lineno)s
                        -   %(message)s
                    -   重写 matter 方法
                -   handlers
                    -   2. 创建 handler
                        -   分类
                            -   StreamHandle()
                            -   TimedRotatingFileHandler
                                -   filename
                                -   when
                                    -   设置时间间隔
                                        -   D
                                            -   每天
                                -   interval
                                    -   几个时间间隔
                                -   backupCount
                                    -   保留日志数量
                                    -   360
                                -   th.suffix="%Y%m%d-%H%M.log"
                            -   RotatingFileHandler()
                                -   filename
                                -   encoding
                                -   maxByte
                                -   backupCount
                            -   FileHandler(filename, encoding)
                        -   设置
                            -   setformatter（）
                            -   setLevel()
                                -   设置各个 handler 的 level
                -   3. 添加
                    -   addHandler()
                        -   添加两种 handler
                    -   setLevel()
                        -   设置 log 的 level
                -   防止重复添加 handler
                    -   handlers
            -   导入设置
                -   dict={}
                -   logging.config.dictConfig()
                -   logger = logging.getlogger(\_\_name\_\_)
                -   return
        -   后使用
            -   logger = logging.getlogger(\_\_name\_\_)
                -   单例模式，唯一的对象
            -   logger.debug('')
                -   日志使用%
