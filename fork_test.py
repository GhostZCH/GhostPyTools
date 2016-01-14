import os
import time
import signal

_work_pid = 0
_go = True


def master(child_pid):
    print 'master: ', os.getpid(), child_pid
    time.sleep(3)
    os.kill(child_pid, signal.SIGINT)
    print 'kill worker'


def kill_work(sig, frame):
    global _go
    _go = False


def worker():
    signal.signal(signal.SIGINT, kill_work)
    signal.signal(signal.SIGTERM, kill_work)

    global _go
    print 'worker: ', os.getpid(), os.getppid()
    while _go:
        time.sleep(0.5)
        print 'worker'
    print 'worker exit'


if __name__ == '__main__':
    _pid = os.fork()
    if _pid:
        master(_pid)
    else:
        worker()
