import operator


def get_rpn(express):
    ops = {
        '(': 3,
        ')': 3,
        '*': 2,
        '/': 2,
        '+': 1,
        '-': 1,
    }

    parts = express.split()
    op = []
    re = []
    for p in parts:
        if p not in ops:
            re.append(int(p))
        else:
            if p == ')':
                while op[-1] != '(':
                    re.append(op.pop())
                op.pop()
            else:
                while op and op[-1] != '(' and ops[op[-1]] >= ops[p]:
                    re.append(op.pop())
                op.append(p)

    while op:
        re.append(op.pop())

    return re


def compute_rpn(rpn):
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.div
    }

    result = []
    for i in rpn:
        if i not in ops:
            result.append(i)
        else:
            b = result.pop()
            a = result.pop()
            result.append(ops[i](a, b))

    return result[0]

if __name__ == '__main__':
    expression = get_rpn('1 + ( 2 + 3 * 5 - 4 ) * 4 - 2 / 2')
    print expression
    print compute_rpn(expression)
