###Abstract Base Class

先看看abc模块，其实模块的东西并不复杂

- **_C**:
  旧式类
- _InstanceType: 
  type(_C) 旧是类的type
- abstractmethod  
  抽象方法的装饰器，使用了这个装饰器来定义接口，其作用就是强制抽象类的子类实现这个接口，不然则抛弃异常。其原理是在funcobj中加入一个\__isabstractmethod__属性，当ABCmeta创建Class的时候，会把所有该属性为True的类方法加入到abstract(set)中
abstractproperty（继承自property）
    抽象属性装饰器，同样通过\__isabstractmethod__=True来标记描述符
- ABCMeta  
- 抽象类的metaclass
    \__new__首先用super初始化生成Class，然后将抽象方法（包括描述符）加入到 cls.\__abstractmethods__ 中，_abc_registry存放注册之后的子类的若引用，_abc_cache和_abc_negative_cache_version如果做过subclass的判断，会缓存结果加速issubclass方法

##abc的例子

#### Interface实现

当你在抽象类中定义了一些方法，你希望子类来实现的时候，你可能需要这样做，如果子类不实现该方法，上溯到父类（抽象类）中就会报错，但是这样做的问题是，生成instance的时候并不会抛出这个异常，直到你运行到某个忘记实现的方法的时候才会报错。所以使用abc

```
class Shape(object):
    def draw(self):
        raise NotImplementedError("Should have implemented this")
```
通过装饰器+metaclass来实现，在实例化的时候就会抛出一个异常，避免了上面的情况发生
```
import abc


class Shape(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def draw(self):
        pass

    @abc.abstractmethod
    def paint(self):
        pass


class Ellipse(Shape):
    def draw(self):
        print "I am %s" % self.__class__.__name__

    def paint(self):
        print "Look ,here is a %s " % self.__class__.__name__


class Round(Ellipse):
    pass


class Rectangle(Shape):
    pass


if __name__ == "__main__":
    el = Ellipse()
    rr = Round()
    rr.paint()
    rr.draw()
    try:
        rc = Rectangle()
    except Exception, e:
        print e
    print isinstance(rr, Shape)
    print isinstance(rr, Ellipse)
    print issubclass(type(rr), Shape)
    print issubclass(type(rr), Round)

```
