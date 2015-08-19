
import time
import logging
import ThreadPool
import unittest

console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logging.getLogger().setLevel(logging.ERROR)

class TestWork(ThreadPool.IWork):
    def __init__(self, n):
        ThreadPool.IWork.__init__(self)
        self._n = n
        self._result = 1

    def run(self):
        # compute n!
        for number in xrange(1, self._n + 1):
            self._result *= number

    def on_finish(self):
        # print(self._result)
        pass


class TPoolTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def pool_test(self, thread_num):
        work_num = 1024  # total work num
        start = time.clock()
        pool = ThreadPool.ThreadPool(thread_num)
        for i in xrange(work_num):
            pool.add_work(TestWork(1000))  # compute 1000!
        pool.wait()
        print '%4d  threads: %0.6f seconds' % (thread_num, time.clock() - start)

    def test_threads(self):
        self.pool_test(1)
        self.pool_test(4)
        self.pool_test(8)
        self.pool_test(12)
        self.pool_test(13)
        self.pool_test(14)
        self.pool_test(15)
        self.pool_test(16)
        self.pool_test(32)
        self. pool_test(1024)

if __name__ == '__main__':
    unittest.main()
