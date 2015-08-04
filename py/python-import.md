###Python Import

 现有包目录如下，main中用到pkg中的内容。
 

 - sub_ppk.modx中自定义了urllib2 ，跟sys.modules里重名
 - 如果modz同时要用系统的urllib2的时候，这时候应该怎么做？（当然可以改名，这里不讨论改名的情况）
 - 因为一些原因sub_ppk.modx中需要用到subppk.modz中的东西，如何引入modz比较便于阅读和修改？

---

    ├── pkg
    │   ├── __init__.py
    │   ├── mod.py
    │   ├── sub_ppk
    │   │   ├── __init__.py
    │   │   ├── modx.py
    │   │   ├── urllib.py
    │   └── sub_ppk_2
    │          ├── __init__.py
    │          └── modz.py
    └── main.py

---
modx.py

    from __future__ import absolute_import
    from ..sub_ppk_2.modz import item
    
    import pkg.sub_ppk.urllib as myurlib
    import urllib as sysurlib
    
    
    print "Get %d bytes" % len(sysurlib.urlopen("http://douban.com").read())

main.py
    
    from pkg.sub_ppk.modx import myurlib, sysurlib
    if __name__ == "__main__":
        print myurlib
        print sysurlib
        
modz.py

    item = "this is mod z"

其余文件都为空

###先来了解相对引入

    import urllib
    import sys

上述语句，执行的时候，会先从sys.modules里查找，之后是sys.path，你可以试着

    import sys
    for module in  sys.modules:
        print module
    for p in  sys.path:
        print p

来查看import是按什么顺序查找模块的（**参见 [引入顺序][1]**），基本顺序是是 sys.modules > local > sys.path，所以当前目录内的东西是可能会覆盖sys.path里的东西的。为了解决这个问题有了：

###绝对引入


    from __future__ import absolute_import
    import mylib.urllib as mylib
    import urllib as syslib
    
注释掉第一行，那么main中的调用会报错，因为两个urllib都是自己定义的

###带层次结构的相对引入

在modx中，如果我想引入mod_a中的item对象

####隐式相对引入

    import ..mod_a
####显示相对引入

    from pkgggg.mod_a import item

第一种写法，可读性较差
第二种写法，改名字会比较复杂
PEP8推荐 第一种 
https://mail.python.org/pipermail/python-dev/2013-July/127399.html


参考 https://www.python.org/dev/peps/pep-0328/#id10


  [1]: https://docs.python.org/2/tutorial/modules.html#the-module-search-path
