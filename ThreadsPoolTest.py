import ThreadPool

class TestWork(ThreadPool.IWork):
    def __init__(self, n):
        self._n = n
        self._result = 1

    def run(self):
        # compute n!
        for number in xrange(self._n):
            self._result *= number

    def get_result(self):
        return self._result


if __name__ == '__main__':
    pool = ThreadPool.ThreadPool()

    for i in xrange(1024):
        pool.add_work(TestWork(100))
