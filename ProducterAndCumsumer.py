import threading
import time

_SIG_EXIT = 'exit'

buf = ""
index = 0
mutex = threading.Lock()

con_empty = threading.Condition(mutex)
con_full = threading.Condition(mutex)


def producer():
    global buf, index

    while True:
        with con_empty:
            if buf:
                print("con_empty.wait()")
                con_empty.wait()

            print "producing>>>"
            if index >= 10:
                buf = _SIG_EXIT
                con_full.notify()
                return

            buf += "message: %03d" % index
            index += 1

            print "con_full.notify()"
            con_full.notify()


def consumer():
    global buf

    while True:
        with con_full:
            if not buf:
                print "con_full.wait()"
                con_full.wait()

            if buf == _SIG_EXIT:
                return

            print "consuming>>>"
            print buf
            buf = ''

            print "con_empty.notify()"
            con_empty.notify()


if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)

    producer_thread.start()
    consumer_thread.start()

    consumer_thread.join()
    producer_thread.join()
