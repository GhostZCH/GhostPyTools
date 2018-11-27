class SimpleConsoleChose:
    def __init__(self):
        pass

    def draw_chose(self, chose):
        print(chose)


class ComplexConsoleChose:
    def __init__(self):
        pass

    def draw_chose(self, chose):
        print("/============================================================")
        print("| %s" % chose)


class WelcomeInfo:
    def __init__(self, chose_list, chose):
        self.chose_list = chose_list
        self.chose = chose

    def draw(self):
        for item in self.chose_list:
            self.chose.draw_chose(item)


if __name__ == '__main__':
    list = ['1. query', '2. add', '3. edit', '4. delete']

    simple = SimpleConsoleChose()
    complex = ComplexConsoleChose()

    welcome_simple = WelcomeInfo(list, simple)
    welcome_simple.draw()

    print()
    print()

    welcome_complex = WelcomeInfo(list, complex)
    welcome_complex.draw()