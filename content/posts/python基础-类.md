+++
title = 'Python基础 类'
date = 2023-11-23T21:54:28+08:00
draft = true
toc = true
tags = ["Python", "Software Architecture"]
+++

## 一：概念阐述

### 面向对象

因为提高了代码的复用性，开发效率高，而且便于扩展迭代，所以成为了主流的开发思想。其中的核心概念就是类，在面向对象的思想中，可以用类来抽象一切的事物

### 类

__抽象一类事物为一个模型__。用 __属性__ 和 __方法__ 来描述。

#### 属性

描述一类事物的属性，本质上是类中的变量。包括两种：

实例属性：这个类的对象的一种 __个体的属性__

类属性：这个类所有对象的一种 __整体的属性__

#### 方法

描述一类事物的行为，本质上是类中的函数。包括三种：

实例方法：

__self__: 实例方法中，自动添加的一个参数，代表调用此方法的对象。

类方法：

__cls__: 实例方法中，自动添加的一个参数，代表调用此方法的类。用@classmethod装饰

静态方法：

既不使用self，也不使用cls的方法。用@staticmethod装饰

__调用方法的两种方式__：

1. 对象调用方法

2. 类名调用方法

### 对象

是具体的一个一个的事物，由 __类__ 制造而成。

### 实例化

类制造对象的过程

```python
class Person(object):  # 创建类
    pass

if __name__ == '__main__':
    p1 = Person()  # 类加括号：实例化一个对象
```

## 二：python中的顶级父类及其属性和方法

object：顶级父类，继承的源头，默认继承它

\__class__: 查看实例化这个对象的类

\__bases__：查看父类

\__dict\__: 字典形式__显示属性__

dir(obj)：查看obj拥有的方法

\__new__(): 创建对象

\__init\__()：初始化对象的属性，__创建对象自动调用__，可以设置默认参数

\__str\__()：打印对象信息，__必须return字符串，print(对象)的时候__

\__repr\__()：打印对象信息，__必须return字符串，print(对象容器)的时候__，例如[obj1, obj2,...]

type：顶级元类，实例化的源头，一般了解即可

```python
class Person(object):  # 创建类
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(self.name, '吃饭')

    def __str__(self):
        return self.name


if __name__ == '__main__':
    p1 = Person('lisi')  # 类加括号：实例化一个对象
    print('----------------------查看属性和方法-----------------------')
    print(p1.__dict__)  # 以字典形式打印对象属性
    print(dir(Person))  # 打印类的方法

    print('-----------------__class__-----__bases__----------------')
    print(p1.__class__)  # 实例化此对象的类
    print(Person.__bases__)  # 此类的父类们

    print('----------了解---------object-------type-----------------')
    print(object.__class__)  # 实例化object这个对象的是 type这个顶级元类
    print(object.__bases__)  # object没有父类
    print(type.__class__)  # 实例化type这个对象的类是它自己
    print(type.__bases__)  # type的父类是object这个顶级父类
```

运行结果

```bash
----------------------查看属性和方法-----------------------
{'name': 'lisi'}
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'eat']
-----------------__class__-----__bases__------------------
<class '__main__.Person'>
(<class 'object'>,)
----------了解---------object-------type----------------------
<class 'type'>
()
<class 'type'>
(<class 'object'>,)
```

## 三：封装

python中，封装属性，方法的办法是：

 在属性和方法前面加 __两个下滑线__，例如：‘\_\_属性’，‘\_\_方法’

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age  # __ 防止在类的外部使用

    def show(self):
        print(self.name, self.__age)

    def __show2(self):
        print('测试封装方法')


stu = Student('张三', 23)
stu.show()
# stu.__show2()  #AttributeError: 'Student' object has no attribute '__show2'
print(stu.name)
# print(stu.__age)  # AttributeError: 'Student' object has no attribute '__age'
print('-----------------------------------------------')
```

__运行结果：__

```bash
张三 23
张三
-----------------------------------------
```

封装属性，是为了类来控制 __属性的读写__。

使用装饰器 __@property和@属性名.setter__,可以很好控制属性的访问

```python
class Student:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def age(self):
        return self.__age
    # 注释掉，就不能外部修改了
    # @age.setter
    # def age(self, new_age):
    #     self.__age = new_age

if __name__ == '__main__':
    s1 = Student('qq', 12)
    print(s1.name)
    s1.name = 'hahaha'
    print(s1.name)

    print(s1.age)
    s1.age = 20
    print(s1.age)
```

__运行结果：__

```bash
AttributeError: can't set attribute
qq
hahaha
12
```
