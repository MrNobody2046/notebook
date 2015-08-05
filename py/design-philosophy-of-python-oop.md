# Python 面向对象设计哲学


###中心思想
 1. 万物皆对象
 2. 神说要有type于是有type，而后type生出classobj和万物（classobj是旧式类的type O(∩_∩)O~~）


###什么是type?
```
>>>print type
<type 'type'>
>>>type(type)
type
```
上面可以看出type就是type，type是class的抽象，调用type对象将生成class，class调用(实例化)成为instance

type描述class 
class描述instance
instance是看得见（可以交互）摸得着（有内存地址）的实体

记住type只有一个，但是你可以继承自他生成自己的type，比如

```
class AbstractType(type):
 pass

```

```
CLS = lambda *args, **kwargs: \
    type.__new__(type("mcs", (type,), {}),"NewClass",(),
                 { "print_self": lambda ins: ins.__dict__,  "__init__":
                     lambda ins, *args, **kwargs:
                     (ins.__dict__.update(kwargs), None)[1] } )(*args, **kwargs)
```





   

