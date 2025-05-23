+++
title = 'Tornado Tutorial'
subtitle = ""
date = 2024-05-26T01:17:25+08:00
draft = false
toc = true
tags = ['web']
+++

-   websocket
    -   概念
        -   可以双向发送消息
        -   WebSocket 允许服务器主动向客户端推送数据，实现实时性更强的通信
    -   WebSocketHandler
-   web

    -   RequestHandler

        -   调用的执行顺序
            ![code-order](../imgs/code-order.jpg)
        -   set_default_headers
        -   initialize
            -   子类初始化
        -   入口

            -   get

                -   self.request

                -   self.get_argument('k') # 获取一个参数
                -   self.get_arguments('k') # 获取一个参数列表

            -   post
                -   json.loads(self.request.body)
            -   put
            -   delete
            -   prepare
            -   on_finish
            -   redirect
            -   write
                -   所有 JSON 输出都应该包装在一个字典中
            -   render()
                -   返回 html

        -   header

        -   cookies

        -   get_current_user
        -   status

    -   authenticated
        -   用户认证
    -   tornado.ioloop.PeriodicCallback()
        -   定时任务


<https://www.tornadoweb.org/en/stable/web.html>
