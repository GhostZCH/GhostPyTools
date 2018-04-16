import operator


def get_rpn(express):
    ops = {
        '(': 0,
        ')': 0,
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
            if p == '(':
                op.append(p)
            elif p == ')':
                while op and op[-1] != '(':
                    re.append(op.pop())
                if op[-1] == '(':
                    op.pop()
            else:
                while op and ops[p] < ops[op[-1]]:
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
    left = rpn
    right = []

    while len(left) > 1:
        right.append(left.pop())
        while left and right and left[-1] not in ops and right[-1] not in ops:
            a = left.pop()
            b = right.pop()
            left.append(ops[right.pop()](a, b))

    return left[0]

if __name__ == '__main__':
    expression = get_rpn('1 + ( 2 + 3 * 5 - 4 ) * 4 - 2 / 2')
    print expression
    print compute_rpn(expression)
