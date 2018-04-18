import os
import time
import signal
import random

import zmq

_WORKER_CONT = 4
_POLL_TIMEOUT = 1000  # ms
_COLLECT_ADDR = 'tcp://127.0.0.1:8001'  # recv from worker
_DISTRIBUTE_ADDR = 'tcp://127.0.0.1:8002'  # send to worker


class Master:
    def __init__(self):
        self._run = True
        self._sequence = 0

        ctx = zmq.Context()

        self._sender = ctx.socket(zmq.PUSH)
        self._sender.set_hwm(20)
        self._sender.bind(_DISTRIBUTE_ADDR)

        self._receiver = ctx.socket(zmq.PULL)
        self._receiver.set_hwm(24)
        self._receiver.bind(_COLLECT_ADDR)

        self._workers = []

    def forever(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

        poller = zmq.Poller()
        poller.register(self._receiver, zmq.POLLIN)
        poller.register(self._sender, zmq.POLLOUT)

        recv_data = False  # keep running until no data come and get stop signal

        while self._run or recv_data:
            poll_dict = dict(poller.poll(timeout=2000))

            if self._run and self._sender in poll_dict:
                self._sender.send_pyobj((self._sequence, 'payload: %020d' % self._sequence))
                self._sequence += 1
                print("master send seq %s" % self._sequence)
                time.sleep(0.5)

            if self._receiver in poll_dict:
                msg = self._receiver.recv_pyobj()
                print("master recv: [worker %s process seq %s result is %s]" % msg)
                recv_data = True
            else:
                recv_data = False

    def stop(self, sig, _):
        print("master recv sig %s" % sig)

        self._run = False
        for pid in self._workers:
            os.kill(pid, signal.SIGTERM)

    def add_worker(self, pid):
        self._workers.append(pid)


class Worker:
    def __init__(self, worker_id):
        self._id = worker_id
        self._run = True

        ctx = zmq.Context.instance()

        self._receiver = ctx.socket(zmq.PULL)
        self._receiver.set_hwm(2)
        self._receiver.connect(_DISTRIBUTE_ADDR)

        self._sender = ctx.socket(zmq.PUSH)
        self._sender.set_hwm(2)
        self._sender.connect(_COLLECT_ADDR)

    def forever(self):
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)

        poller = zmq.Poller()
        poller.register(self._receiver, zmq.POLLIN)
        poller.register(self._sender, zmq.POLLOUT)

        recv_data = False  # keep running until no data come and get stop signal
        while self._run or recv_data:
            poll_dict = dict(poller.poll(_POLL_TIMEOUT))
            if self._receiver in poll_dict:
                recv_data = True
                seq, payload = self._receiver.recv_pyobj()
                print("worker %s recv %s %s" % (self._id, seq, payload))

                # use sleep simulation process time cost
                time.sleep(random.randint(500, 1000) / 1000.0)

                print("worker %s send %s" % (self._id, seq))
                self._sender.send_pyobj((self._id, seq, seq * seq))
            else:
                recv_data = False

    def stop(self, sig, _):
        print("worker %s recv sig %s" % (self._id, sig))
        self._run = False


def main():
    # master must bind to addresses first
    master = Master()

    for i in xrange(_WORKER_CONT):
        pid = os.fork()
        if pid:
            master.add_worker(pid)
        else:
            Worker(i).forever()

    master.forever()

if __name__ == '__main__':
    main()
