class A:
    def __init__(self):
        self.a = 1
        self.b = 2


if __name__ == '__main__':
    a = A()
    print a.__class__
    print a.__dict__
    print a.__module__
    print a.__doc__
    print a.__init__.im_class
    print a.__init__.im_func
    print a.__init__.im_self
