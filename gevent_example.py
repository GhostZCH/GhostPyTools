#!/usr/bin/env python
# coding: utf-8
from gevent import monkey
monkey.patch_socket()

from gevent import socket
from gevent.server import StreamServer


class CHTTPHandler(object):
    def __init__(self, sock):
        self.socket = sock

    def handle(self):
        """Handle multiple requests if necessary."""
        while self.socket:
            self.socket.recv(1024)
            self.socket.sendall("HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nContent-Length: 0\r\n\r\n")
        # self.socket.close()


class CHTTPServer(StreamServer):
    def __init__(self, addr, backlog=1024):
        StreamServer.__init__(self, addr, backlog=backlog)

    def handle(self, sock, _):
        handler = CHTTPHandler(sock)
        handler.handle()


if __name__ == '__main__':
    svr = CHTTPServer(('0.0.0.0', 8000))
    svr.serve_forever()

