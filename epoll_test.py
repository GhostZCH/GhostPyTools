import socket
import errno
import select
import traceback

_TEST_DATA = "HTTP/1.0 200 OK\r\nContent-type :text/plain\r\nContent-length: 1024\r\nConnection: Keep-Alive\r\n\r\n" + '0' * 1024

# _TEST_DATA = "HTTP/1.0 200 OK\r\nContent-type :text/plain\r\nContent-length: 1024\r\n\r\n" \ + '0' * 1024


def get_svr(port=8000):
    svr = socket.socket()
    svr.bind(('', port))
    svr.listen(1024)

    return svr


def get_epoll(svr, max_fd=10240):
    epoll = select.epoll(max_fd)
    epoll.register(svr.fileno(), select.EPOLLIN)
    return epoll


def accept(svr, epoll):
    conn, _ = svr.accept()
    epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET | select.EPOLLHUP)
    conn.setblocking(False)
    conn.settimeout(0.1)
    return conn


def handle_event_recv(client):
    try:
        while True:
            buf = client[0].recv(1024)
            if not buf and not client[1]:
                print 'not buf', client[0].fileno(), client[1]
                return True, True

            client[1] += buf
            if '\r\n\r\n' in client[1]:
                client[3] = 'keep-alive' in client[1].lower()
                return True, False

    except socket.error, ex:
        if ex.errno == errno.EAGAIN:
            print 'AGAIN'
            return True, True
        else:
            traceback.print_exc()
            return False, False


def handle_event_send(client):
    try:
        while True:
            send_len = client[0].send(_TEST_DATA[client[2]:])
            if not send_len:
                print 'not send_len'
                return False, False

            client[2] += send_len
            if client[2] >= len(_TEST_DATA):
                return True, False

    except socket.error, ex:
        if ex.errno == errno.EAGAIN:
            print 'AGAIN'
            return True, True
        else:
            traceback.print_exc()
            return False, False


def loop(svr, epoll):
    client_list = {}
    while True:
        for fd, event in epoll.poll(0.1, 1024):
            if fd == svr.fileno():
                conn = accept(svr, epoll)
                client_list[conn.fileno()] = [conn, '', 0, False]
                continue

            if event & select.EPOLLHUP:
                epoll.unregister(fd)
                client_list[fd][0].close()
                del client_list[fd]
                continue

            if event & select.EPOLLIN:
                ok, goon = handle_event_recv(client_list[fd])
                if not ok:
                    return
                if not goon:
                    client_list[fd][2] = 0
                    epoll.modify(fd, select.EPOLLOUT | select.EPOLLET | select.EPOLLHUP)
                continue

            if event & select.EPOLLOUT:
                ok, goon = handle_event_send(client_list[fd])
                if not ok:
                    return
                if not goon:
                    # client_list[fd][0].close()
                    # epoll.unregister(fd)
                    # del client_list[fd]
                    if client_list[fd][3]:
                        client_list[fd][1] = ''
                        epoll.modify(fd, select.EPOLLIN | select.EPOLLET | select.EPOLLHUP)
                    else:
                        client_list[fd][0].close()
                        epoll.unregister(fd)
                        del client_list[fd]
                continue


def main():
    svr = get_svr()
    epoll = get_epoll(svr)

    try:
        loop(svr, epoll)
    except:
        traceback.print_exc()
        epoll.close()
        svr.close()


if __name__ == '__main__':
    main()
