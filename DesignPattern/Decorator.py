#encodeing="utf-8"

class MessageBox:
    def __init__(self, message=""):
        self.message = message

    def show(self):
        print(self.message)

    def get_len(self):
        return  max(len(self.message), 1)

class MsgBoxDecorator:
    def __init__(self, msg_box):
        self.msg_box = msg_box
        self.border = ""

    def get_len(self):
        return self.msg_box.get_len()

    def inner_show(self, border):
        print(border)
        self.msg_box.show()
        print(border)

class DoubleBorder(MsgBoxDecorator):
    def __init__(self, msg_box):
        MsgBoxDecorator.__init__(self, msg_box)

    def show(self):
        border = "=" * self.msg_box.get_len()
        self.inner_show(border)

class SingleBorder(MsgBoxDecorator):
    def __init__(self, msg_box):
        MsgBoxDecorator.__init__(self, msg_box)

    def show(self):
        border = "-" * self.msg_box.get_len()
        self.inner_show(border)

def get_msg_box(message, border=''):
    msg_box = MessageBox(message)

    for option in border:
        if option == '=':
            msg_box = DoubleBorder(msg_box)
        elif option == '-':
            msg_box = SingleBorder(msg_box)
        else:
            return msg_box

    return msg_box

# 组合和装饰都使用了类的组合形式，而且都使用一个接口作为所有类的基类，看上去比较相似
# 形式上，每个装饰只包含一个抽象实例，类似于链表。而组合模式则是包含多个实例，类似于树
# 逻辑上，装饰的根本只有一个真实的实例，剩下的都是装饰，是在这一个基础上不断的怎天功能，是为某个功能追加装饰，如同一个人穿衣服，不管穿了多少层，始终还是那个人
# 但是组合模式，却是包含了大量的实例，每个有效的实例都会有不同的行为，模式的目的只是方便通过一个行为激发所有实例的行为
# 类似将一群人分配成各个层级的部门，只要向总经理下达任务，任务就会被所有人执行
if __name__ == '__main__':
    box = get_msg_box("hello border", "=-=-")
    box.show()