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

说到这里可能会很迷惑abc能做什么呢我们来试试
