# coding:utf-8
from abc import ABCMeta, abstractproperty

"""
visitor模式展示
典型的调用为:
A.apply(B)
实例B访问实例A内部,B就是一个visitor
"""


class Engineer(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def write(self, Code):
        """
        :param Code: 访问者
        :return:
        """
        pass


class BaseEngineer(Engineer):
    def __init__(self, name, age, languages):
        self.name = name
        self.age = age
        self.languages = languages

    def write(self, Code):
        return Code.visit(self)


class BackEndDeveloper(BaseEngineer):
    def __init__(self, name, age, languages=['C', 'Java', 'Python']):
        super(BackEndDeveloper, self).__init__(name, age, languages)


class FrontEndDeveloper(BaseEngineer):
    def __init__(self, name, age, languages=['Html', 'Css', 'JavaScript']):
        super(FrontEndDeveloper, self).__init__(name, age, languages)


class iOSDeveloper(BaseEngineer):
    def __init__(self, name, age, languages=['OC']):
        super(iOSDeveloper, self).__init__(name, age, languages)


class AndriodDeveloper(BaseEngineer):
    def __init__(self, name, age, languages=['Java']):
        super(AndriodDeveloper, self).__init__(name, age, languages)


class Code(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def visit(self, Engineer):
        pass


class BaseCode(Code):
    _temp = "I'm {name} ,{age} years old ,I can write {langs}"

    def __init__(self, name):
        self.name = name

    def visit(self, Engineer):
        msg = self._temp.format(name=Engineer.name, age=Engineer.age, langs=','.join(Engineer.languages),
                                lang=self.name)
        if self.name not in Engineer.languages:
            msg += ", Damn! I hate %s" % self.name
        else:
            msg += ", Haha, I like %s " % self.name
        print msg


class BaseCodeFactory(object):
    def name_list(self, names):
        return [BaseCode(name) for name in names]


if __name__ == "__main__":
    Jack, Max, John, Lucy = BackEndDeveloper("Jack", 22), \
                            iOSDeveloper("Max", 31), \
                            AndriodDeveloper("John", 25), \
                            FrontEndDeveloper("Lucy", 23)

    Java, C, Html, Css = BaseCode("Java"), BaseCode("C"), BaseCode("Html"), BaseCode("Css")

    for engineer in Jack, Max, John, Lucy:
        for lan in Java, C, Html, Css:
            engineer.write(lan)
