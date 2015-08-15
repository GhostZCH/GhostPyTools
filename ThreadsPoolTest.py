import  ThreadPool


if __name__ == '__main__':
    p = TPool(4)

    for i in range(10):
        p.add_work(Work(str(i)))

    time.sleep(2)

    for i in range(10):
        p.add_work(Work(str(i)))