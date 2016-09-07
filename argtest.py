def main(*list_args, **dict_args):
    print list_args
    print dict_args

if __name__ == '__main__':
    l = [1, 2, 3]
    d = {'x': 100, 'y': 200}
    main(*l, **d)

    print 'again'
    main(1, 2, 3, 4, x=100, y=200)
