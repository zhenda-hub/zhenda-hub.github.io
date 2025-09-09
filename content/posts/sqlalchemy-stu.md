+++
title = 'Sqlalchemy Stu'
subtitle = ""
date = 2025-02-07T12:19:54+08:00
draft = false
toc = true
series = ["python"]
tags = ["python", "sql"]
+++

- <https://docs.sqlalchemy.org/en/20/orm/quickstart.html>
- <https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#one-to-many>
- <https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html>


```
本身知识点
    概念： 通过ORM（对象和表的映射）操作数据库的框架
    步骤
        创建基类
            engine = create_engine（URL）
            Base = declarative_base（engine ）
        定义映射
            子类
                表名
                    __tablename__ = ''
                备注
                    __table_args__ = {'': ''}
                Column（）
                    类型
                        db.
                                Int
                                float
                                double
                                String
                                text
                                longtext
                                Date
                                time
                                datetime
                                bool
                                enum
                    参数
                            primary_key=True
                            autoincrement=True
                        default=
                            doc=
                            comment=
                    外键类
                        ForeignKey('表名.属性')
                            ondelete=''
                                CASCADE
                                DELETE
                                RESTRICT
                relationship('类名')
                    一对多
                        backref=True
                    一对一
                        子表
                            backref=backref('属性', uselist=False)
                    多对多
                        先用Table()设立中间表
                        backref=True， secondary=中间表变量名
        表的操作
            Base.metadata.drop_all()
            Base.metadata.create_all()
        CRUD
                session = sessionmaker(engine )（）
                    增
                        子类对象
                        session = add(子类对象)
                    查
                        session.query(子类名).filter()
                            first()
                    高级
                        session.query().order_by()
                            all()
                        分页查询
                            方法1
                                session.query().slice()
                                    all()
                            方法2
                                session.query().offset().limit()
                                    all()
                session.commit()
        其他
            with_entities（）
            子类.sort.asc()
alembic
    数据库版本管理


```
