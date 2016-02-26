#Python高级特性

主要整理搜集自：http://stackoverflow.com/questions/101268/hidden-features-of-python?rq=1


1. 列表项

###利用\*和**参数解包

 

```
def draw_point(x, y):
    # do some magic

point_foo = (3, 4)
point_bar = {'y': 3, 'x': 2}

draw_point(*point_foo)
draw_point(**point_bar)
```
###我不要缩进 想要C那样的花括号 
```
from __future__ import barry_as_FLUFL
```
哈哈 你特么在逗我 不过这是[p3k里的特性]，**不要在py2中尝试**

###链式比较计算

```
>>> x = 1
>>> 0 <= x <= 3
True
>>> 0 <= x > -1
True
>>> 0 <= x > -3
True
>>> x < 10 < x*10 < 100
False
```

###装饰器

装饰器接受一个方法或者函数，返回一个新的方法或者函数
```
import sys

def catch_exception(callable):
    def wrapper(*args, **kwargs):
        try:
            return callable()
        except Exception, e:
            print e

    return wrapper

def divide(a, b):
    return a / b

@catch_exception
def divide(a, b):
    return a / b
```
"@"是语法糖，其原理就是把**修饰的对象**作为参数传入。上面的例子中process_exception能够捕捉所有的异常并且打印到系统输出，很自然的，你也可以为不同的函数，定制不同的异常处理机制，所以可以制作返回装饰器的方法。
```

def process_exception(process=lambda e: sys.stdout.write(repr(e) + "\n")):
    def decorator(callable):
        def wrapper(*args, **kwargs):
            try:
                return callable()
            except Exception, e:
                return process(e)

        return wrapper

    return decorator


@process_exception(process=lambda e: sys.stdout.write("Ignore it!!!"))
def divide(a, b):
    return a / b

```

其实@也可以用在类上面，利用它也可以实现最简单的全局单例
```
def singleton(x):
    instance = []

    def wrapper(*args, **kwargs):
        if not instance:
            instance.append(x(*args, **kwargs))
        return instance[0]

    return wrapper


@singleton
class SystemMgr:
    def __init__(self, name):
        self.name = name


managerA = SystemMgr("A")
managerB = SystemMgr("B")
print sm is sm2
```

PS：[python新式类的介绍]

###谨慎使用**可变对象**作为默认参数

```
def bar(items=[]):
    items.append(len(items))
    return items[-1]
```
默认items从函数定义时就生成了，所以之后如果不指定items，内部的items会一直增加，有时候也会故意使用这种特性（zuo si）

```
class Box(object):
    __data__ = []

    @classmethod
    def add(cls, x):
        cls.__data__.append(x)


def add_box(x, box=Box):
    """do something here"""
    return box.add(x)

```

###描述符 Descriptors

通过描述符可以实现类属性的权限控制，详细请看参考[Python 描述符简介]

###**字典默认值** 与 **\__missing__ **函数
当你从某个字典中get 键值的时候，给get方法传入第二个参数，这个参数作为key不存在时候的默认值：
```
count = {}
count[1] = count.get(1,0) + 1
```
有必要指出的是，也可以使用defaultdict模块来达到同样的效果：
```
from collections import defaultdict
count = df = defaultdict(lambda :1)
count[1] += 1
```
defaultdict能做的事情蛮多的，可以看我在知乎上的一个例子:[Python list 累加的问题]

条条大路通罗马，更复杂一点，可以定义自己的\__missing__ 函数，而不是用一行代码完成复杂的逻辑
```
class CountDict(dict):

    def __missing__(self, key):
        return 0

count = CountDict()
print count[0] # >>> 0

```

###Ellipsis 对象

在py2k中 numpy 和scipy支持省略号切片 
```
import numpy
matrix = array([range(10) for i in range(10)])
"""
[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]
""" 一个二维矩阵

print matrix[Ellipsis,2]
print matrix[...,2] # 输出矩阵的第三列,Ellipsis和 '...'是一样的作用
如果没有Ellipsis,你可能要这也弄了 m2 = [i[2] for i in matrix]

```

### for/else 技巧
没有用这个技巧之前：
```
found = False
for i in foo:
    if i == 0:
        found = True
        break
if not found: 
    print("i was never 0")
```
用了之后
```
for i in foo:
    if i == 0:
        break
else:
    print("i was never 0")
```

else（注意缩进） 部分的语句，会在所有的if语句都不能通过之后执行，这样免去了一个中间变量

###iter()函数支持callable对象

```
def seek_next_line(f):
    for c in iter(lambda: f.read(1),'\n'):
        pass
        
        

```
iter函数的说明
```
def iter(source, sentinel=None): # known special case of iter
    """
    iter(collection) -> iterator
    iter(callable, sentinel) -> iterator
    
    Get an iterator from an object.  In the first form, the argument must
    supply its own iterator, or be a sequence.
    In the second form, the callable is called until it returns the sentinel.
    """
    pass
```

iter函数构成的iterator每一次next，会调用第一个callable对象，当某一次调用返回值和sentinel相等就终止

###列表推导变值为惰性求值(generator)

```
a = range(10000)
new_a = [range(i) for i in a] # 立即推导开辟了内存
lazy_new_a = (range(i) for i in a) # generator
```

这是一个省内存的技巧，实施起来也只要把方括号变为括弧就可以。

###字典推导
2.7之后版本可以使用
```
{index:value for index,value in enumerate(range(10))}

```
2.6
```
dict([(k,v) for k,v in something])

```

###多重赋值

```
s = 1,2,3 # tuple
a,b,c = s
```
利用unpack/pack这种特性，可以inplace swap
```
a = 1
b = 2
a, b = b, a
```
深入一点你可以
```
a,b,c,d = range(4)
#甚至iterator也可以
a,b,c,d = xrange(4)
#当然generator也没问题
a,b,c,d = (i for i in range(4))

```
###String Named Format

```
#形式1
"select %(field)s from %(table)s limit %(limit)i" % dict(field="name",table="product", limit=1)

#形式2 该形式不检查格式对象的类型，统一调用str函数

"select {field}  from {table} limit {limit}".format(field="name",table="product", limit=1)

#扩展

def select(field,table,limit):
    return "select {field}  from {table} limit {limit}".format(**locals())

```


###Exception else clause

```
try:
    1/0
except:
    print "raise exception here"
else:
    print "do something if no exception"
finally:
    print "always do something here"

```

###


  [p3k里的特性]: https://www.python.org/dev/peps/pep-0401/
  [python新式类的介绍]:http://www.kaka-ace.com/python2_new-style-and-classic-classes/
  [Python 描述符简介]:http://www.ibm.com/developerworks/cn/opensource/os-pythondescriptors/
  [Python list 累加的问题]:http://www.zhihu.com/question/31298771/answer/52318519
