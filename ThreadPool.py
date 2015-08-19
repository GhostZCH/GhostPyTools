import threading
import Queue
import logging

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)

class IWork(object):
    def __init__(self):
        pass

    def run(self):
        pass

    def on_finish(self):
        pass


class ThreadWorker(threading.Thread):
    def __init__(self, get_work, worker_id):
        threading.Thread.__init__(self)
        self._get_work = get_work
        self._id = worker_id
        logging.info('ThreadWorker.__init__: %s' % worker_id)

    def run(self):
        logging.info('ThreadWorker.run: %s' % self._id)

        while True:
            try:
                work = self._get_work()
            except Queue.Empty:
                continue

            if not work:
                return

            logging.info('ThreadWorker.run.work.run: %s' % self._id)
            work.run()
            work.on_finish()

        logging.info('ThreadWorker.run.work == None, thread exit: %s' % self._id)


class ThreadPool:
    def __init__(self, max_size=4, max_queue_size=1024):
        self._pool = []
        self._que = Queue.Queue(maxsize=max_queue_size)
        self._lock = threading.Lock()
        self._is_stop = False
        self._is_wait = False

        for i in xrange(max_size):
            worker = ThreadWorker(self._get_work, i)
            self._pool.append(worker)
            worker.start()

    def _get_work(self):
        if self._is_stop:
            return None

        with self._lock:
            try:
                return self._que.get_nowait()
            except Queue.Empty, ex:
                if self._is_wait:
                    return None
                raise ex

    def add_work(self, work):
        if isinstance(work, IWork):
            self._que.put(work)
            return

        raise Exception('parm error: work mush a instance of IWork, your work is a %s' % type(work))

    def stop(self):
        self._is_stop = True

    def wait(self):
        logging.warn('ThreadPool.wait: begin wait ')
        self._is_wait = True
        is_run = True
        while is_run:
            is_run = False
            for th in self._pool:
                is_run |= th.isAlive()
        logging.warn('ThreadPool.wait: all thread exit. ')
