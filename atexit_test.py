import atexit


def test(a, b, c):
    print 'test', a, b, c


if __name__ == '__main__':
    atexit.register(test, a=1, b=2, c=3)
    atexit.register(test, 4, 5, 6)
    atexit.register(test, 7, b=8, c=9)
    print('end for main')


# end for main
# test 4 5 6
# test 1 2 3
