#!/usr/bin/python3

# -*- coding: utf-8 -*-

'''
@file: make.py

@time: 2018/5/20 22:21
'''
from socket import *
from PIL import ImageGrab, ImageFilter, ImageTk, Image
from threading import Thread


def transmite_datas(datas, sock):
    n = 100
    times = len(datas) // n
    # print(times)
    for i in range(n):
        print(i)
        sock.send(datas[i * times:(i + 1) * times])
    # else:
    #     print('out')


def ons(sock):
    while True:
        # print(1)
        im = ImageGrab.grab()
        im.thumbnail((800, 600))
        mo = im.mode
        # print(mo)
        sz = im.size
        datas = im.tobytes(encoder_name='raw')
        attr = {'mode': mo, 'size': sz, 'le': len(datas)}
        attr = str(attr)
        sock.send(attr.encode())
        # print('发送属性:',attr)
        sock.recv(1024)
        transmite_datas(datas, sock)
        sock.send(b'')
        sock.recv(1024)


def main(addr):
    ADDR = (addr, 7999)
    # print('main')
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        sock.connect(ADDR)
        print('make.connect')
        Thread(target=ons, args=(sock,)).start()
    except Exception:
        sock.close()
        sys.exit(0)

if __name__ == '__main__':
    main(('172.88.13.122', 6666))
