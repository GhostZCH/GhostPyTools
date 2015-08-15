import threading
import Queue



class IWork:
    def __init__(self):
        pass

    def run(self):
        pass

class Worker(threading.Thread):
    def __init__(self, get_work):
        threading.Thread.__init__(self)
        self._get_work = get_work

    def run(self):
        work = self._get_work()
        while work:
            work.run()
            work = self._get_work()


class TPool:
    def __init__(self, num):
        self._pool = []
        self._que = Queue.Queue(maxsize=1024)
        self._lock = threading.Lock()
        for i in range(num):
            worker = Worker(self._get_work)
            self._pool.append(worker)
            worker.start()

    def _get_work(self):
        with self._lock:
            return self._que.get()

    def add_work(self, work):
        self._que.put(work)

if __name__ == '__main__':


