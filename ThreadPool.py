import threading
import Queue

class IWork:
    def __init__(self):
        pass

    def run(self):
        pass

    def get_result(self):
        pass


class ThreadWorker(threading.Thread):
    def __init__(self, get_work, worker_id):
        threading.Thread.__init__(self)
        self._get_work = get_work
        self._id = worker_id

    def run(self):
        work = self._get_work()
        while work:
            work.run()
            work = self._get_work()


class ThreadPool:
    def __init__(self, max_size=4):
        self._pool = []
        self._que = Queue.Queue(maxsize=1024)
        self._lock = threading.Lock()

        for i in xrange(max_size):
            worker = ThreadWorker(self._get_work)
            self._pool.append(worker)
            worker.start()

    def _get_work(self):
        with self._lock:
            return self._que.get()

    def add_work(self, work):
        self._que.put(work)
