class Line:
    def __init__(self, style='='):
        self.style = style

    def draw(self):
        print(self.style * 40)

class Border:
    def __init__(self, lines):
        self.lines = lines

    def draw(self):
        for line in self.lines:
            line.draw()
        print()


def draw_border(style_list):
    lines = []

    for style in style_list:
        lines.append(Line(style))

    Border(lines).draw()

def init_lines():
    style_list = '*_+='
    line_dic = {}

    for style in style_list:
        line_dic[style] = Line(style)

    return  line_dic

def draw_border_flyweight(style_list):
    line_dic = init_lines()
    lines = []

    for style in style_list:
        lines.append(line_dic[style])

    Border(lines).draw()

if __name__ == '__main__':
    style_list = '*_+=*_+=*_+='

    draw_border(style_list)  # 12 objects

    draw_border_flyweight(style_list)  # 4 objects
