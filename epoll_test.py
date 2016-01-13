# coding=utf-8

import socket
import errno
import select
import traceback

_TEST_DATA = "HTTP/1.0 200 OK\r\nContent-type :text/plain\r\nContent-length: 1\r\nConnection: Keep-Alive\r\n\r\n" + '0' * 1

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
    conn.setblocking(False)
    epoll.register(conn.fileno(), select.EPOLLIN | select.EPOLLET | select.EPOLLHUP)
    return conn


def handle_event_recv(client):
    try:
        while True:
            buf = client[0].recv(1024)

            if not buf:
                # 连接关闭, 接收结束
                return False, False

            client[1] += buf
            if '\r\n\r\n' in client[1]:
                client[3] = 'keep-alive' in client[1].lower()
                # 需要的数据接收完成,认为结束
                return True, False

    except socket.error, ex:
        if ex.errno == errno.EAGAIN:
            # 上面提前判断了,这里可以省掉,
            # # 缓冲区没有数据了,可能是发送完毕了但是没有关闭sock,也可能是网速慢暂时没有传过来,需要业务层来判断
            # if '\r\n\r\n' in client[1]:
            #     client[3] = 'keep-alive' in client[1].lower()
            #     # 需要的数据接收完成,认为结束
            #     return True, False
            # 没收完, 下次有数据再来收
            return True, True

        else:
            raise ex


def handle_event_send(client):
    try:
        while True:
            send_len = client[0].send(_TEST_DATA[client[2]:])
            if not send_len:
                # 发送失败
                return False, False

            client[2] += send_len
            if client[2] >= len(_TEST_DATA):
                # 发送完成
                return True, False
    except socket.error, ex:
        if ex.errno == errno.EAGAIN:
            return True, True
        else:
            raise ex


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
                ok, again = handle_event_recv(client_list[fd])

                if not ok:
                    # 有错误关闭
                    client_list[fd][0].close()
                    epoll.unregister(fd)
                    del client_list[fd]

                elif not again:
                    # 读取完毕准备发送
                    client_list[fd][2] = 0
                    epoll.modify(fd, select.EPOLLOUT | select.EPOLLET | select.EPOLLHUP)
                continue

            if event & select.EPOLLOUT:
                ok, again = handle_event_send(client_list[fd])

                if not ok:
                    client_list[fd][0].close()
                    epoll.unregister(fd)
                    del client_list[fd]
                elif not again:
                    # 发送完成
                    if client_list[fd][3]:
                        # 判断是否keep-alive, 如果是准备接收数据开始下个对话,如果不是关闭连接
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
