class FactorialProxy:
    def __init__(self, n):
        self.n = n

    def factorial(self):
        'real computing'
        result = 1
        for i in range(self.n):
            result *= i + 1
        return result

if __name__ == '__main__':
    item_list = ['100! = ', FactorialProxy(100),';' , '200! = ', FactorialProxy(200), '.']  # init but not execute

    string = ''
    for item in item_list:
        if isinstance(item, FactorialProxy):
            string += str(item.factorial())  # real execute
        else:
            string += item
    print(string)