+++
title = 'Python基础 类2'
date = 2023-11-23T22:49:27+08:00
draft = true
toc = true
tags = ["Python", "Software Architecture"]
+++

这次我们补充说明 __类的关系__ 这一非常重要的概念

## 类之间的关系

### has关系： 使用依赖

依赖：当B类 has A类时，在 __B类中__ 使用 __A类的对象__

特点：通过A类对象，使用A类所有东西。

举例说明：人有手，有脚，但手不是人，脚也不是人，只是人的一部分

再比如： 一个班级， 可以有很多学生，它们之间的关系就应该是依赖的关系

再比如： 一个人， 可以有一个电脑，人可以使用电脑做各种事情。人和电脑之间的关系就应该是依赖的关系

这种思想经常使用，甚至 __比人们耳熟能详的继承，多态， 还要重要！！__

```python
class Computer:

    def __init__(self, brand) -> None:
        self.brand = brand

    def run_game(self):
        print('运行lol')

    def run_ide(self):
        print('运行vscode')


class People:

    def __init__(self, name, computer: Computer) -> None:
        self.name = name
        self.computer = computer

    def write_code(self):
        print(f'{self.name}使用{self.computer.brand}')  # 调用属性的属性
        self.computer.run_ide()  # 调用属性的方法
        print('开始写代码')


if __name__ == '__main__':
    computer = Computer('机械革命')
    zhangsan = People('张三', computer)  # 把电脑对象作为属性传入， 依赖
    zhangsan.write_code()
```

__运行结果:__

```bash
C:\Users\a7935\PycharmProjects\pythonProject>python chap12_类/has-a2.py
张三使用机械革命
运行vscode
开始写代码
```

**源码分析：**

requests库中的Session使用依赖：

![Session依赖](../imgs/1.jpg)

openpyxl库中的Workbook使用依赖：

![WorkBook依赖](../imgs/WorkBook依赖.jpg)

openpyxl库中的Worksheet使用依赖：

![WorkSheet依赖](../imgs/WorkSheet依赖.jpg)

![Worksheet依赖3](../imgs/Worksheet依赖3.jpg)

### is关系： 使用继承

#### 创建不同对象

当这种is关系的 __属性和方法一样__,  我们无需创建一个类，通过创建不同的对象就可以实现

```python
class People:

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def __str__(self):
        return f'我是{self.name}, 今天{self.age}岁'


if __name__ == '__main__':
    zhangsan = People('小张', 14)
    print(zhangsan)
    lisi = People('老李', 41)
    print(lisi)
```

__运行结果:__

```bash
C:\Users\a7935\PycharmProjects\pythonProject>python chap12_类/is-a2.py
我是小张, 今天14岁
我是老李, 今天41岁
```

#### 继承

概念：B类继承了A类，那么B称为A的子类，A称为B的父类。B类实例化的对象可以使用A类的属性和方法

特点：

1. 子类 __自动实现了父类的方法__。无需手动实现
2. 子列要想继承父类的属性，需要在\_\_init\_\_()中 调用super().\_\_init\_\_()

使用继承的条件：

1. 两个类之间是is关系
2. 子类需要 __扩展父类的属性，方法__

我们可以把那个 __宽泛，笼统的类__ 当作父类，另一个 __具体详细的类__ 当作子类。

#### 扩展属性，方法

例如我们有一个需求：现有一个People类，需要创建一个会游泳的People类。

需求分析：因为会游泳的人也是人，符合条件1；因为不是每个人都会游泳，需要对人类进行扩展，符合条件2。

下面开始实现：

```python
class People:

    def __init__(self, name, age) -> None:
        self.name = name
        self.age = age

    def __str__(self):
        return f'我是{self.name}, 今天{self.age}岁'


class PeopleSwimmable(People):  # 继承语法

    def swim(self):
        print(f'{self.name}在游泳')


if __name__ == '__main__':
    zhangsan = People('小张', 14)
    print(zhangsan)
    lisi = People('老李', 41)
    print(lisi)

    wangwu = PeopleSwimmable('老王', 61)
    print(wangwu)
    wangwu.swim()
```

__运行结果:__

```bash
C:\Users\a7935\PycharmProjects\pythonProject>python chap12_类/is-a3.py
我是小张, 今天14岁
我是老李, 今天41岁
我是老王, 今天61岁
老王在游泳
```

**源码分析：**

openpyxl库中的Cell使用继承，扩展属性，方法：

![Cell扩展](../imgs/Cell扩展.jpg)

requests库中的Request使用继承，扩展属性，方法：

![request扩展](../imgs/request扩展.jpg)

#### 多态

多态：同一个方法，不同类创建的对象来调用，结果不同

##### 重写

重写：是实现多态的非常重要的方式。在子类中，创建父类的 __同名方法__， __修改__ 其实现内容。

注意： __子类重写\_\_init\_\_()方法__，添加新的属性， __需要调用父类的\_\_init\_\_()方法__ 来初始化从父类继承来的属性，否则父类属性无法使用。下面为调用的两种方法：

1. super().\_\_init\_\_()
2. 父类名.\_\_init\_\_(self, )

##### 里氏替换原则：针对is关系，防止滥用多态

概念： __子类对象__ 可以替换任意的 __父类对象__， __程序执行__ 不受影响

实际使用：重写需要保证函数的 __宽进严出__, 参数可以更加宽泛，返回值必须更加严格

```python
class Hero:

    def __init__(self, hp=100, money=1000) -> None:
        self.hp = hp
        self.money = money

    def __str__(self):
        return f'我是{self.__class__.__name__}, 现在血量{self.hp}, 拥有金钱{self.money}'


class Jax(Hero):
    def __init__(self, owner, hp=100, money=1000):
        self.owner = owner
        super().__init__(hp, money)  # super().__init__()

    def __str__(self):
        return super().__str__() + f', 玩家是{self.owner}'


class Zed(Hero):
    def __init__(self, owner, hp=100, money=1000):
        self.owner = owner
        Hero.__init__(self, hp, money)  # 父类名.__init__(self, )

    def __str__(self):
        return super().__str__() + f', 玩家是{self.owner}'


if __name__ == '__main__':
    hero = Hero()
    print(hero)

    jax = Jax('uzi')
    print(jax)

    zed = Zed('faker')
    print(zed)

```

__运行结果:__

```bash
我是Hero, 现在血量100, 拥有金钱1000
我是Jax, 现在血量100, 拥有金钱1000, 玩家是uzi
我是Zed, 现在血量100, 拥有金钱1000, 玩家是faker
```

##### 源码分析

matplotlib库中的Axes3D使用重写：

![Axes3D继承](../imgs/Axes3D继承.jpg)

![Axes重写](../imgs/Axes重写.jpg)

![Axes3d重写](../imgs/Axes3d重写.jpg)

Axes3D的scatter()的参数添加了‘zs’, 'zdir'等， 并且添加了 __默认值__。不需要调用时传参。因此可以使用子类实例替换父类实例

它们的返回值均为：\`~matplotlib.collections.PathCollection\`

sympy库中的LinearEntity2D使用重写：

![LinearEntity2D重写](../imgs/LinearEntity2D重写.jpg)

![LinearEntity重写](../imgs/LinearEntity重写.jpg)

![LinearEntity2D重写2](../imgs/LinearEntity2D重写2.jpg)
