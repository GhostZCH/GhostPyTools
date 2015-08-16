import ThreadPool
import unittest
import logging
import threading
import time

import Queue

print('xxxxxxxxxxxxxxx')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

class TestWork(ThreadPool.IWork):
    def __init__(self, n, handler):
        self._n = n
        self._result = 1
        self._handler = handler

    def run(self):
        # compute n!
        for number in xrange(1, self._n + 1):
            self._result *= number

    def finish(self):
        self._handler(self._result)

class TPoolTest(unittest.TestCase):
    def write_ourput(self, result):
        with self. _mutex:
            print('%s: %s' % (self._count,  result))
            self._count += 1

    def setUp(self):
        self._mutex = threading.Lock()
        self._count = 0

    def tearDown(self):
        pass

    def test_4_threads(self):
        work_num = 1024
        pool = ThreadPool.ThreadPool()

        for i in xrange(work_num):
            pool.add_work(TestWork(100, self.write_ourput))

        que = Queue.Queue()
        x = que.get()

        while self._count < work_num:
            time.sleep(0.1)
        else:
            pool.stop()
            print('over')

if __name__ == '__main__':
    unittest.main()
