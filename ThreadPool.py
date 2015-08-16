import threading
import Queue
import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

class IWork:
    def __init__(self):
        pass

    def run(self):
        pass

    def finish(self):
        pass


class ThreadWorker(threading.Thread):
    def __init__(self, get_work, worker_id):
        threading.Thread.__init__(self)
        self._get_work = get_work
        self._id = worker_id
        logging.info('ThreadWorker.__init__: %s' % worker_id)

    def run(self):
        logging.info('ThreadWorker.run: %s' % self._id)
        print('ThreadWorker.run: %s' % self._id)
        work = self._get_work()
        while work:
            logging.info('ThreadWorker.run.work.run: %s' % self._id)
            work.run()
            work.finish()
            work = self._get_work()
        logging.info('ThreadWorker.run.work == None, thread exit: %s' % self._id)
        print('ThreadWorker.run.work == None, thread exit: %s' % self._id)

class ThreadPool:
    def __init__(self, max_size=4):
        self._pool = []
        self._que = Queue.Queue(maxsize=1024)
        self._lock = threading.Lock()
        self._is_stop = False

        for i in xrange(max_size):
            worker = ThreadWorker(self._get_work, i)
            self._pool.append(worker)
            worker.start()

    def _get_work(self):
        if self._is_stop:
            return None

        with self._lock:
            return self._que.get()

    def add_work(self, work):
        if isinstance(work, IWork):
            self._que.put(work)
            return

        raise Exception('parm error: work mush a instance of IWork, your worke is a %s' % type(work))

    def stop(self):
        self._is_stop = True
