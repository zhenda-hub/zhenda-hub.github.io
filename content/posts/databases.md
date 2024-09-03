+++
title = 'Databases'
subtitle = ""
date = 2024-06-03T09:21:49+08:00
draft = true
toc = true
tags = []
+++

-   关系型

    -   mysql

        -   基础

            -   环境变量
                -   我的电脑
                    -   高级设置
                        -   path 里添加 mysql 安装路径
            -   配置文件
                -   my.cnf
            -   图形控制软件
                -   Navicat
                    -   步骤
                        -   设置密码不过期
                            -   alter user 'root'@'localhost' identified by 'root' password expire never;
                        -   修改加密规则
                            -   alter user 'root'@'localhost' identified with mysql_native_password by 'root';
                        -   连接 mysql
                            -   设置编码
                        -   创建数据库
                        -   新建查询
                            -   写 sql
                    -   可以选择代码来运行
                        -   快捷键
                            -   ctrl, shift, r
            -   默认数据库
                -   mysql
                    -   管理用户的表
                        -   user
                -   performance
                -   sys
                -   test
                    -   每个用户一个测试用的数据库
            -   查看字符集格式
                -   show variables like 'char%';
            -   最基本操作！！！！！
                -   命令行访问
                    -   启动
                        -   service mysql restart
                        -   service mysql start
                    -   登录
                        -   mysql -h localhost -u root -p;
                            -   --port=
                            -   root
                    -   基本操作
                        -   show databases;
                        -   use mysql;
                            -   选择数据库
                        -   show tables;
                        -   desc 表；
                        -   select database();
                            -   查看当前数据库
                        -   exit;
            -   sql 语句

                -   分类

                    -   权限管理

                        -   DCL

                            -   运维重点

                                -   用户密码控制
                                    -   查看用户
                                        -   select user,host from mysql.user
                                    -   设置密码等级
                                        -   set global validate_password.policy=LOW
                                        -   set global validate_password.length=1
                                    -   重新设置密码
                                        -   mysqladmin -uroot -p password
                                -   查看权限
                                    -   show grants for 用户@host
                                -   远程连接设置

                                    -   概念
                                        -   一个 pc 连接另一个 pc 的 mysql
                                    -   主要步骤
                                        _ 创建用户
                                        _ 语法
                                        _ create user 用户@host identified by 密码
                                        _ 例子
                                        _ create user 'zzd'@'%' identified by 'root'
                                        _ 给与权限
                                        _ 语法
                                        _ grant 权限 on 表 to 用户@host
                                        _ 例子
                                        _ grant all on _._ to 'zzd'@'%'
                                        _ 删除用户
                                        _ drop user ‘用户’@‘ip’ \* 例子

                                              * update user set host='%' where user='root';
                                                  * nat方式连接，查看虚拟ip

                                        -   刷新授权表，立即生效
                                            -   flush privileges;

                                    -   其他相关操作
                                        -   管理员身份运行
                                            -   mysqld -install
                                        -   访问速度慢
                                            -   修改 my.ini
                                                -   在 mysqld 里面添加一句话
                                                    -   skip-name-resolve

                                -   帮助信息
                                    -   ? Account Management

                    -   数据库，表

                        -   DDL

                            -   database
                                -   create database 库名称 (各个列的内容);
                                -   drop database 库名称
                                -   use 库名称
                                    -   选择库
                            -   table

                                -   语句

                                    -   create table 表名称 (各个列的内容);
                                        -   primary key
                                            -   中文：主键，非常关键
                                                -   唯一且非空
                                        -   auto_increment
                                            -   用于整数

                                    *   alter table 表名称
                                        -   ADD
                                            -   name char(1)
                                        -   DROP
                                            -   MODIFY
                                                -   内容
                                            -   change oldname, name
                                                -   内容和列名
                                    *   drop table 表名称

                                -   约束

                                    -   概念
                                        -   对于表中的各个列内容的限制
                                    -   分类

                                        -   非外键
                                            -   字段后面
                                                -   primary key
                                                    -   中文：主键，非常关键
                                                    -   唯一且非空
                                                -   auto_increment \* 用于整数
                                                -   UNIQUE
                                                -   NOT NULL
                                                -   DEFAULT
                                                -   CHACK( sex='boy' || sex='girl')
                                                    -   选择约束
                                            -   表
                                                -   constraint 匿名 PRIMARY KRY(字段)
                                                    -   唯一且非空
                                                -   constraint 匿名 CHACK( sex='boy'||sex='girl')
                                                -   constraint 匿名 UNIQUE(字段)
                                            -   表外部添加
                                                -   alter table 表名称 add
                                                    -   constraint 匿名 PRIMARY KRY（）
                                                -   alter table 表名称 modify
                                                    -   auto_increment
                                        -   外键

                                            -   概念
                                                -   子表通过外键，关联父表主键
                                                -   相当于：类通过组合使用其他类
                                            -   使用
                                                -   子表重写
                                                    -   表类型的
                                                        -   constraint 匿名 foreign key (子表字段) references 父表名 (父表字段)
                                                        -   外部添加
                                                            -   alter table 表名称 add
                                                                -   constraint 匿名 foreign key (子表字段) references 父表名 (父表字段)
                                            -   删除

                                                -   外键策略

                                                    -   目的
                                                        -   方便修改或删除父表
                                                    -   重新设置策略
                                                        -   删除原来的外键约束
                                                            -   alter table 表名称 drop foreign key 外键匿名
                                                        -   外部添加
                                                            -   on update cascsde on delete cascade
                                                                -   会直接删除子表内容
                                                                    -   方便，但危险
                                                            -   on update set null on delete set null
                                                    -   分类

                                                -   一般情况
                                                    -   先删除子表，再删除父表

                                -   表的字段
                                    -   添加
                                        -   alter table 表名 add 字段 A 类型 after 字段 B
                                            -   添加字段 A，放在字段 B 后面
                                    -   删除
                                        -   alter table 表名 drop 字段
                                    -   修改
                                        -   alter table 表名 change 旧字段 新字段 新类型
                                            -   改字段名，改类型
                                        -   alter table 表名 modify 字段 新类型
                                            -   改字段的类型
                                -   表的索引
                                    -   添加
                                        -   alter table 表名 add index 索引名（字段）
                                    -   删除
                                        -   alter table 表名 drop index 索引名 （字段）
                                -   查看建表语句
                                    -   show create table 表名字
                                -   修改表名
                                    -   rename table A to B
                                    -   alter table A rename to B

                            -   view
                                -   with check option
                                    -   控制选择条件
                            -   procedure
                                -   存储过程 相当于函数
                                    -   创建
                                        -   （in ， out）
                                            -   begin
                                                -   if
                                                    -   then
                                                -   else
                                                -   end if;
                                            -   select found_rows() into
                                                -   返回查询个数
                                            -   end;
                                    -   调用
                                        -   函数名（'', @rst）
                                        -   select @rst;
                                            -   打印查询个数
                            -   帮助信息
                                -   ? Data Definition

                    -   数据
                        -   DML！！！！
                            -   添加一行数据
                                -   insert into 表名称（字段 1，字段 2） values ('A','B')
                                -   insert into 表名称 values ('A','B')
                            -   删
                                -   删一行数据
                                    -   delete from 表名称 where
                                -   清空表的数据
                                    -   truncate table 表名称
                                        -   重新建表
                                        -   自增的主键不会保留
                                    -   delete from 表名称
                                        -   自增的主键会保留
                            -   改
                                -   update 表名称 set 字段 1=‘’， 字段 2=‘’ where 条件
                            -   帮助信息
                                -   ? Data Manipulation
                            -   数据类型
                                -   字符
                                    -   VARCHAR
                                        -   一句话
                                    -   TEXT
                                        -   大文章
                                -   数字
                                    -   INT
                                    -   FLOAT
                                    -   DOUBLE
                                -   时间
                                    -   DATE
                                    -   TIMESTAMP
                                    -   time
                                    -   DATETIME
                                    -   NOW()
                        -   DQL
                            -   select
                                -   函数
                                    -   单行函数
                                        -   lower()
                                        -   upper()
                                        -   length（）
                                        -   substring（字段， start， stop）
                                            -   下标从 1 开始
                                        -   abs（）
                                        -   ceil()
                                        -   floor()
                                        -   round()
                                        -   curdate()
                                        -   curtime()
                                        -   now()
                                        -   sysdate()
                                            -   实际执行时间
                                        -   条件分支
                                            -   if(条件，A，B)
                                            -   ifnull(条件，执行)
                                            -   nullif(val1, val2)
                                                -   val1 等于 val2，则返回 null，否则返回 val1
                                            -   case
                                            -   database()
                                            -   user()
                                            -   version()
                                    -   多行函数
                                        -   概念
                                            -   对多个数据处理，返回一个结果
                                        -   特点
                                            -   自动忽略 null 的值
                                            -   min（字段）
                                            -   max（字段）
                                            -   avg（字段）
                                            -   sum()
                                            -   count（字段）
                                -   显示数据总数
                                    -   select count(\*) from 表名
                                -   显示数据
                                    -   SELECT \* FROM 表名
                                    -   SELECT \* FROM 表名 \G
                                -   单表查询
                                    -   单表操作
                                        -   去重
                                            -   distinct
                                    -   执行顺序，从上往下
                                        -   from
                                        -   分组前筛选
                                            -   where
                                                -   条件 A and 条件 B
                                                    -   or
                                                    -   in（12，23）
                                                -   like ’‘
                                                    -   ’%A%‘
                                                        -   %多个字符
                                                    -   ’\_A%‘
                                                        -   \_代表一个字符
                                                -   is null
                                        -   按照字段的不同内容分组
                                            -   group by
                                        -   选择字段展示
                                            -   select
                                        -   having
                                            -   分组后筛选
                                        -   排序
                                            -   order by 字段
                                                -   asc
                                                    -   升序
                                                -   desc
                                                    -   降序
                                -   多表查询
                                    -   连接方式
                                        -   只显示匹配的表信息，不匹配的信息忽略
                                            -   交叉连接
                                                -   select \* from 表 A cross join 表 B
                                                    -   很多重复内容
                                            -   自然连接
                                                -   select \* from 表 A natural join 表 B
                                                    -   匹配 所有同名列
                                                        -   同名列只展示一次
                                            -   内连接
                                                -   select \* from 表 A inner join 表 B
                                                    -   using 同名列字段
                                                        -   选择 同名列
                                                    -   on A.字段=B.字段
                                                        -   设置 同名列
                                                            -   设置 A 的字段，匹配 B 的字段
                                                                -   自连接
                                                    -   on A.字段 betwen B.小字段 and B.大字段
                                        -   显示匹配和不匹配的表信息
                                            -   左外连接
                                                -   select \* from 表 A left outer join 表 B
                                                    -   展示左表的全部信息
                                            -   右外连接
                                                -   select \* from 表 A right outer join 表 B
                                                    -   展示右表的全部信息
                                            -   合并左外连接，右外连接
                                                -   添加 union
                                                    -   select _ from 表 A left outer join 表 B union select _ from 表 A right outer join 表 B
                                                -   select \* from 表 A full outer join 表 B
                                                    -   展示左外连接和右外连接合并的全部信息，但 mysql 不支持这个语法
                                    -   分类
                                        -   两表查询
                                        -   三表查询
                                            -   可以看成两表查询
                                        -   自己查询
                                            -   可以看成两表查询
                                -   子查询
                                    -   概念
                                        -   多个 sql 语句合并成，提高查询效率，总的 sql 语句依赖子的 sql 语句，子 sql 语句称为子查询
                                    -   select where （）
                                        -   不相关子查询
                                            -   概念
                                                -   可以独立运行的子查询
                                            -   分类
                                                -   单行
                                                    -   查询结果为一个
                                                        -   =
                                                        -   >
                                                        -   <
                                                -   多行
                                                    -   查询结果多一个
                                                        -   all（）
                                                        -   any（）
                                                        -   in（）
                                        -   相关子查询
                                            -   起一个别名

                -   默认不区分大小写
                    -   可以设置区分
                        -   binary

            -   事务
                -   需求背景
                    -   银行转账，两个账户需要确保都完成，或都不完成
                -   特性
                    -   ACID
                        -   原子性
                        -   一致性
                        -   隔离性
                        -   持久性
                -   原理
                    -   默认一条 sql 语句，为一个事务
                    -   可以手动开启事务，执行多条 sql 语句
                -   流程
                    -   start transaction
                        -   手动开始一个事务
                    -   多条 sql 语句
                        -   操作缓存，不操作数据库
                    -   可以选择
                        -   rollback
                            -   撤销
                        -   commit
                            -   提交
                -   事务并发
                    -   多个事务同时进行，同时操作缓存
                        -   问题
                            -   脏读
                                -   数据错了
                            -   不可重复读
                                -   数据变了
                            -   幻读
                                -   数据多了
                        -   解决方法
                            -   事务隔离级别
                                -   repeatable read
                                -   read uncommitted
                                -   read committed
                                -   sarializable
                            -   查看隔离级别
                                -   select @@transaction_isolation
                -   事务分类
                    -   本地事务
                    -   分布式事务
                        -   操作不同数据库，来保证一致性
            -   索引
                -   作用
                    -   相当于书的目录，快速查找
                -   可以建立多个索引
                -   常用索引类型
                    -   primary key
                    -   unique
                    -   not null
                -   联合索引
                    -   优点
                        -   就像查字典一样，通过减少搜索的范围，增大索引效率，更快速的查找数据
                        -   复合索引比两个单独索引效果好
                    -   特点
                        -   最左匹配
                            -   字段 1
                            -   字段 1 字段 2
                            -   字段 1 字段 2 字段 3
                            -   左边不能少，右边可以少
                            -   像字典一样
                        -   不起作用的匹配
                            -   字段 2
                            -   字段 3
                            -   字段 2 字段 3
                    -   将多个字段设置为索引
                    -   定义
                        -   添加
                            -   alter table 表名 add index 索引名 (字段 1，字段 2)
                                -   字段需要非空
                                -   字段顺序非常重要
                        -   删除
                            -   alter table 表名 drop index 索引名
                        -   查
                            -   show index from 表名
                    -   使用场景
                        -   排序
                        -   分组
                        -   外键
                    -   不应当使用的场景
                        -   表需要频繁增删改
                        -   第一个字段数据量很大

        -   进阶

            -   设计表
                -   存储引擎（做表类型）
                    -   查看数据库的引擎
                        -   show engines
                    -   分类
                        -   InnoDB
                            -   事务型
                            -   并发
                            -   外键
                            -   崩溃后可以恢复
                        -   MyISAM
                -   可以通过界面来分析字段
                -   命名
                    -   小写字母下划线
                        -   主键索引名
                            -   pk\_字段名
                        -   唯一索引名
                            -   uk\_字段名
                        -   普通索引名
                            -   idx\_字段名
                -   一个表代表一个类
                    -   表要小而精， 和类一样
                        -   将字段很多的表分为多个表
                    -   字段
                        -   必须的
                            -   id
                                -   自增
                            -   create_time
                                -   非空
                            -   update_time
                                -   非空
                            -   is_deleted
                                -   软删除
                                    -   保证数据完整性
                                        -   藏数据。。
                                    -   查
                -   设置搜索频率高的字段为索引
                    -   原理
                        -   索引会按照特定的数据结构（如 B 树、B+树）对字段值进行排序和存储，使得数据库引擎可以更快速地定位到需要查询的数据，而不需要逐行扫描整个表
                -   少用外键， 逻辑可以写在代码里
                    -   减小数据库计算压力
                    -   外键多了，数据库无法扩容
                    -   不能做分库分表
                        -   不同数据库不能用外键
                -   表的字段很多时
                    -   分表
                        -   条件查询
                        -   相信内容
            -   多实例
                -   一个 pc 装多个 mysql，port 不同
            -   高端操作

                -   主从同步

                    -   原理

                        -   从机查看主机二进制日志
                            -   binary log
                                -   二进制日志
                        -   详细描述

                    -   新问题

                        -   ms 级别的同步延迟

                    -   作用
                        -   读写分离，缓解数据库压力
                            -   应用场景
                                -   读请求很多，写请求较少
                            -   操作
                                -   主机配置
                                -   同步内容
                                -   主机授权
                                    -   grant replication slave on _._ to 'repl'@'%';
                                -   从机连接
                        -   高可用
                            -   一个挂了另一个跟上
                            -   注意点

                -   集群
                    -   数据库集群方式？？

            -   调优
                -   show profiles
                    -   大局时间
                -   show profile
                    -   细节时间
                -   performance_schema
                -   分库分表
            -   数据库连接池
                -   概念
                    -   分配、管理和释放 数据库的连接
                    -   数据库的连接
                        -   tcpip 连接
                        -   数据库登录
                        -   sql 执行
                        -   数据库退出
                        -   tcpip 断开连接
                -   好处
                    -   减少网络开销，减少数据库登录，退出
                -   步骤
                    -   创建
                        -   栈
                    -   管理
                        -   客户端请求连接
                            -   空闲的数据库的连接
                                -   有
                                    -   分配
                                -   没有
                                    -   是否达到最大连接数
                                        -   否
                                            -   创建新的连接
                                        -   是
                                            -   等待时间
                                                -   超时报警
                        -   客户端释放连接
                            -   删除
                            -   保留
                    -   关闭

        -   原理
            -   b+树
                -   又矮又胖，查询效率高
                -   二叉树效率低
        -   用 python 操作
            -   import pymysql
                -   步骤
                    -   q = connect(host, port, user, password, db, charset)
                    -   p = q.cursor()
                    -   sql 语句
                        -   查
                            -   p.execute(sql, params) 或者 p.executemany(sql, params)
                                -   必须两个参数，防止 sql 注入语句
                                -   sql：语句，参数用%s
                                -   params： 元组参数
                            -   p.fetchall()
                        -   增删改
                            -   try
                                -   p.execute(sql, params) 或者 p.executemany(sql, params)
                                    -   必须两个参数，防止 sql 注入语句
                                    -   sql：语句，参数用%s
                                    -   params： 元组参数
                                -   q.commit()
                                -   except
                                    -   q.rollback()
                                -   else
                    -   p.close()
                    -   q.close()
            -   sqlalchemy
                -   使用类和对象转为 sql

    -   PostgreSQL
        -   支持海量数据
    -   支持 sql 语句，
        -   3306
    -   适用于复杂查询
        -   子查询
        -   聚合函数
            -   count
            -   sum
            -   avg
            -   max
            -   min
        -   分组
        -   排序
        -   过滤

-   非关系型

    -   不支持 sql 语句，适用于关系简单的数据

        -   k-v

            -   redis

                -   概念
                    -   关系简单的存储
                    -   需要配置环境变量 path
                    -   cs 架构
                        -   启动命令
                            -   redis-server
                        -   使用命令
                            -   redis-cli
                    -   特点
                        -   16 个数据库
                        -   速度快
                            -   操作内存
                                -   效率很高
                            -   单线程
                                -   避免切换上下文
                        -   6379
                -   存储数据类型
                    _ hash
                    _ 遍历快
                    _ set
                    _ sorted set
                    _ list
                    _ string
                -   操作命令
                    -   select 1
                    -   查看
                        -   keys \*
                            -   少用，会卡
                            -   查看所有的键
                        -   get key
                        -   type k1
                            -   看类型
                    -   增
                        -   set key value
                        -   mset k1 v1 k2 v2 ...
                            -   批量
                    -   改
                        -   rename k1 new_k1
                    -   删
                        -   del k1 k2
                        -   flushdb
                            -   删除一个库
                        -   flushall
                            -   删除所有库
                    -   设置密码
                        -   config rewrite
                    -   exit
                -   缓存
                    -   逻辑结构
                        -   数据库
                            -   一级缓存
                                -   sqlalchemy 的 session
                            -   二级缓存
                                -   redis
                            -   三级缓存
                                -   nginx
                                -   最快，但可能是脏数据
                        -   客户端
                -   实际使用
                    -   缓存
                        -   数据同步方式
                            -   更新数据库，删除缓存
                                -   没有缓存，查询数据库
                                -   有缓存，返回缓存数据
                                -   更改收据库后，设置缓存失效
                            -   canal 读取 mysql 的 binlog
                        -   设置合理的有效时间
                    -   消息队列
                        -   发布订阅
                        -   事务
                -   远程连接
                    -   修改 redis.conf
                        -   注释掉里面的 bind
                        -   protected-mode
                            -   改为 no
                -   主从同步

                    -   启动 \* redis 配置文件
                    -   断开

                    -   redis-cli info replication
                    -   原理
                        -   全量同步
                        -   部分同步
                        -   命令传播
                    -   redis-cli role
                    -   master 必须做持久化
                        -   防止丢失

                -   集群
                    -   多台服务器 交叉主从同步
                        -   防止一台服务器挂掉。数据异常

        -   文档数据库
            -   mongoDB

    -   shelve
        -   概念
            -   Python 中的数据库，以二进制存储字典
        -   方法
            -   with shelve.open() as db:
                -   open()
                -   close()
