+++
title = 'Django教程'
subtitle = ""
date = 2024-04-30T14:07:14+08:00
draft = true
toc = true
tags = ["web"]
+++

## 通信协议

-   HTTP

| 请求方式 | 传参方式                           | 示例                                              |
|----------|------------------------------------|---------------------------------------------------|
| GET      | 查询字符串 (Query Parameters)      | `GET /users?id=123`                               |
|          | 路径参数 (Path Parameters)         | `GET /users/123`                                  |
|          | 请求头 (Headers)                   | `Authorization: Bearer token`                     |
| POST     | 请求体 (Request Body)              | `POST /users`<br>`{ "name": "John", "age": 30 }`  |
|          | 表单数据 (Form Data)               | `POST /users`<br>`name=John&age=30`               |
|          | 请求头 (Headers)                   | `Content-Type: application/json`                  |
| PUT      | 请求体 (Request Body)              | `PUT /users/123`<br>`{ "name": "Jane", "age": 25 }`|
|          | 路径参数 (Path Parameters)         | `PUT /users/123`                                  |
|          | 请求头 (Headers)                   | `Content-Type: application/json`                  |
| PATCH    | 请求体 (Request Body)              | `PATCH /users/123`<br>`{ "age": 31 }`             |
|          | 路径参数 (Path Parameters)         | `PATCH /users/123`                                |
|          | 请求头 (Headers)                   | `Content-Type: application/json`                  |
| DELETE   | 路径参数 (Path Parameters)         | `DELETE /users/123`                               |
|          | 请求头 (Headers)                   | `Authorization: Bearer token`                     |



    -   get
        -   url传参(对数据长度有限制(大约 2048 个字符)
            -   http://example.com/api?k1=v1&k2=v2
    -   post
        -   传参
            -   类型
                -   request header
                    -   Content-Type 指明数据格式
                -   request body
                    -   json
                    -   form-data
                    -   text
            -   url传参 
    -   put
        -   传参同 post, 只是需要对象存在
    -   delete

-   websocket
-   TCP
-   UDP

## 网站开发逻辑梳理

### 初级阶段，使用 admin 后台快速建站

-   model

    -   model 分类
        -   普通的继承
        -   abstruct 抽象基类
        -   proxy 添加额外的方法
    -   模型管理器
        -   objects =
    -   自定义 BaseModel

    ```python
    class BaseModel(models.Model):
        """为模型类补充字段"""
        create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
        update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

        class Meta:
            # 说明是抽象模型类
            abstract = True
    ```

    ```python
    class ProjectModel(BaseModel):
        """项目"""
        user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)

        name = models.CharField(verbose_name='项目名', max_length=30)
        what = models.TextField(verbose_name='项目描述')
        why = RichTextUploadingField(verbose_name='项目意义')
        priority_choices = ((0, '不重要不紧急'), (1, '不重要紧急'), (2, '重要不紧急'), (3, '重要紧急'))
        priority = models.IntegerField(verbose_name='优先级', default=0, choices=priority_choices)
        public = models.BooleanField(verbose_name='是否公开', default=False)

        start_date = models.DateField(verbose_name='计划开始日期')
        end_date = models.DateField(verbose_name='计划完成日期')

        # how = RichTextUploadingField(verbose_name='执行步骤', config_name='default')
        how = MDTextField(verbose_name='执行步骤')

        attachments = models.FileField(verbose_name='附件', upload_to='attachments/%Y/%m/%d/', null=True, blank=True)
        status = models.BooleanField(verbose_name='是否完成', default=False)
        think = models.TextField(verbose_name='项目感想', null=True, blank=True)

        class Meta:
            verbose_name = '项目'
            verbose_name_plural = verbose_name

        def __str__(self):
            return self.name
    ```

-   admin 后台管理

    -   管理模型类

        -   添加模型类到 admin
            ```python
            # 直接添加
            admin.site.register(ProjectModel)
            ```
        -   自定义模型类的功能页面

            ```python
            # 自定义模型类的admin
            class ProjectModelAdmin(admin.ModelAdmin):
                # list页面
                list_display = ['user', 'name', 'what', 'priority', 'end_date', 'duration', 'status']
                list_filter = ['user', 'status', 'priority', 'end_date']
                search_fields = ['name', 'what', 'why', 'how', 'think']
                ordering = ['status', '-priority', 'end_date']
                # detail页面
                readonly_fields = ['user']  # 只读字段，不能编辑

            # 添加自定义的ProjectModelAdmin
            admin.site.register(ProjectModel, ProjectModelAdmin)
            ```

    -   ## 邮件重置密码

### 直接编写后台逻辑和前台模板页面

-   url
    -   include()
        -   name
        -   namespace
    -   view 中访问
        -   reverse()
    -   基本格式
        -   ''
        -   create/
        -   \<int:pk\>/
        -   \<int:pk\>/update/
        -   \<int:pk\>/delete/
    -   传参数
        -   使用<>来传参
    -   ## 嵌套的 url
-   view

    - 概念：处理请求， 返回响应。通常会操作数据库
    -   请求和响应
        -   https://docs.djangoproject.com/zh-hans/5.0/ref/request-response/
        -   HttpRequest
            -   可以在中间件中设置各种需要的属性
        -   HttpResponse
            -   分类
                -   纯文本
                -   json
                -   html
                -   文件
                -   redirect
    -   数据库操作
        -   https://docs.djangoproject.com/en/5.0/ref/models/querysets/#get
    -   FBV
        -   很直观，完全自主可控的写法
    -   CBV
        -   django提供了一些类来作为view, 不是很好用
    -   中间件， 钩子
        -   概念：在HttpRequest到达view的前后，自定义额外的处理逻辑

-   template

    -   页面的主要类型
        -   list
        -   detail
        -   delete_confirm
    -   语法
        -   tags
            -   常用语法
                -   {% extends 'xxx.html' %} **必须在 html 的最开头**
                -   {% load xxx %} **每个模板页都要 load 自己使用的 tag， 而不能通过 extend 继承**
                -   {% include xxx %}
                -   {% block xxx %} {% endblock xxx %}
                -   {% url 'namespace:name' %}
            -   自定义 tag
                -   在 app 内创建 templatetags/demo.py
                -   {% include demo %}
        -   variables
            -   {{ var1 }}
        -   filters
        -   comments
    -   overwrite
        -   模板加载顺序 DIRS -> APP_DIRS -> others

-   form
    -   Form: 灵活设置需要的字段
    -   ModelForm：针对模型，添加了数据的验证和保存的功能

## 具体功能

### 用户和邮箱

新项目的用户模型

```python
# app/models.py
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

# project/settings.py
settings.AUTH_USER_MODEL = 'appname.User'

# app.admin.py
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    ...
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ["custom_field"]}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ["custom_field"]}),)
```

老项目的用户模型

使用OneToOneField
```python
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
```


### 权限

-   RBAC： 基于角色控制访问
-   分类
    -   retrieve detail
    -   create
    -   retrieve list
    -   update detail
    -   delete detail

### celery 处理异步任务和定时任务

### 缓存

## 前后端分离

-   DRF
    -   概念
        -   对 django 框架进一步封装的第三方包，以便于写出 restfulAPI
    -   Serialization
        -   data
            -   to_representation() 重写序列化逻辑
            -   valid_xxxx() 重写验证逻辑
    -   APIView
        -   Request
        -   Response
            -   status.xxx
        -   顺序
            -   as_view()
                -   dispatch()
                    -   Authentication
                    -   Permission
                    -   Throttling
            -   view func
    -   Viewset
    -   Router
-   VUE
-   CORS 报错
    -   pip install django-cors-headers
    -   https://www.cnblogs.com/WiseAdministrator/articles/11488681.html

## 网站部署

```bash
pythono manage.py check --deploy
```

配置 nginx 和 uwsgi

## django 源码风格

广泛使用 Minin 和 decorator

## 相关文档

-   [Django Doc](https://docs.djangoproject.com/zh-hans/5.0/)
-   [DRF Doc](https://www.django-rest-framework.org/tutorial/quickstart/)

## 常见问题

### CORS

浏览器的同源策略: 是一个重要的安全机制. 禁止不同源访问.

源由协议、域名和端口号组成, 例如 

- http://127.0.0.1:8000
- ws://127.0.0.1:8000

跨域请求: CORS是一种机制，允许服务器声明哪些源可以访问它的资源。这需要**服务器端的配置**。