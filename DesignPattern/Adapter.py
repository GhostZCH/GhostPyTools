
class OldInterFace:
    def __init__(self):
        self.config = {}

    def add_config(self, key, value):
        self.config.update({key: value})

    def get_config(self, key):
       return self.config.get(key)


class NewInterFace:
    def __init__(self):
        pass

    def add_config(self, name, value):
        pass

    def get_config(self, name):
        pass


class Adapter(NewInterFace, OldInterFace):
    def __init__(self):
        NewInterFace.__init__(self)
        OldInterFace.__init__(self)
        self.key = 0
        self.map = {}

    def add_config(self, name, value):
        self.map.update({name: self.key})
        OldInterFace.add_config(self, self.key, value)
        self.key += 1

    def get_config(self, name):
        key = self.map.get(name)
        return OldInterFace.get_config(self, key)


def new_sys_func(new_cfg):
    new_clf.add_config('x', 66)
    new_clf.add_config('y', 99)
    print(new_clf.get_config('y'))


class Base1:
    def __init__(self):
        self.name = 'Base1'

    def get_name(self):
        return  self.name

class Base2:
    def __init__(self):
        self.name = 'Base2'

    def get_name(self):
        return  self.name

class Sub(Base1, Base2):
    def __init__(self):
        Base2.__init__(self)
        # 相同的函数和属性只保留一份，和继承的顺序没关系
        # 谁的初始函数在后面，谁的属性和方法就有效
        Base1.__init__(self)

    def print_name(self):
        print(self.name)

if __name__ == '__main__':
    new_clf = Adapter()
    new_sys_func(new_clf)

    for key in new_clf.map:
        print('%s: %s' %( key, new_clf.map.get(key)))

    for key in new_clf.config:
        print('%s: %s' %( key, new_clf.config.get(key)))

    sub = Sub()
    sub.print_name()
    print(sub.name)