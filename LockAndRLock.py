import threading

if __name__ == '__main__':
    r_lock = threading.RLock()
    print 'start'
    with r_lock:
        with r_lock:
            print 'can print'

    lock = threading.Lock()
    with lock:
        print 'can print'
        with lock:
            print 'can NOT get here'
    print 'can NOT get here'
