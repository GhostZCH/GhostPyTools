class Composite:
    def __init__(self, name=None):
        self.children = []
        self.name = name

    def add_child(self, child):
        self.children += [child]

    def operation(self):
        if self.name:
            print(self.name)
            return

        for child in self.children:
            child.operation()


#           o
#          / \
#         1   o
#            /  \
#           O   2.2
#          / | \
#    2.1.1  2.1.2  2.1.3

if __name__ == '__main__':
    item21 = Composite()
    item21.add_child(Composite('2.1.1'))
    item21.add_child(Composite('2.2.2'))
    item21.add_child(Composite('2.2.3'))

    item2 = Composite()
    item2.add_child(item21)
    item2.add_child(Composite('2.2'))

    item_root = Composite()
    item_root.add_child(Composite('1'))
    item_root.add_child(item2)

    item_root.operation()
