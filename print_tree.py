# -*- coding:utf-8 -*-

# print tree
#
# ├─── 1002
# ├─── 1001
# │   ├─── 1001.2
# │   │   ├─── 1001.2.1
# │   │   │   ├─── 1001.2.1.1
# │   │   │   └─── 1001.2.1.2
# │   │   └─── 1001.2.2
# │   └─── 1001.1
# └─── 1000


def print_tree(tree, pre=''):
    if not tree:
        return

    i = 1
    for k in tree:
        if i < len(tree):
            print pre + '├───', k
            print_tree(tree[k], pre + '│   ')
        else:
            print pre + '└───', k
            print_tree(tree[k], pre + '    ')
        i += 1


def main():
    tree = {
        '1000': {},
        '1001': {
            '1001.1': {},
            '1001.2': {
                '1001.2.1': {
                    '1001.2.1.1': {},
                    '1001.2.1.2': {},
                },
                '1001.2.2': {}
            }
        },
        '1002': {},
    }

    print_tree(tree)

if __name__ == '__main__':
    main()
