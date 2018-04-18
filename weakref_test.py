import gc
import weakref


class A:
    def __init__(self, obj):
        #self._obj = weakref.ref(obj)
        self._obj = obj

    def __del__(self):
        print "del: a"


class B:
    def __init__(self):
        self._data = A(self)

    def __del__(self):
        print "del: b"


def func(a):
    print func.__class__
    print a

if __name__ == '__main__':
    b = B()
    b.__add__ = func
    #b.x("aaa")
    # del b
    print b + 1

    a = [[1,2,3],[4,5,6]]
    print map(list, zip(*a))
