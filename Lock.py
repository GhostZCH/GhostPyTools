import threading


if __name__ == '__main__':

    rlock = threading.RLock()
    with rlock:
        with rlock:
            print("hello RLock")

    lock = threading.Lock()
    with lock:
        with lock:
            print("can not print")

