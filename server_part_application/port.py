#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

from server_part_application.thread import thread_def
from config import *


if __name__ == '__main__':

    sock = socket.socket()
    sock.bind(('', PORT))
    sock.listen(2)
    # db = DbAdapter

    while True:
        conn, addr = sock.accept()
        print('a2')
        threading.Thread(target=thread_def, args=(conn, addr,)).start()
        # print('connected:', addr)
        # while True:
        #     data = conn.recv(1024)
        #     print(data)
        #     if not data:
        #         break
        #     conn.send(data.upper())
        #
        # conn.close()
