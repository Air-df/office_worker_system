# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Li Xin Hao

"""
远程视图--接收模块
接收主机信息，在客户端展示
"""

import traceback
import tkinter
import os
from socket import *
from threading import Thread


from PIL import ImageGrab, ImageFilter, ImageTk, Image


def change_i(s, i):
    print('in change picture')
    while True:
        d = s.recv(1024)
        # print(d.decode())
        s.send(d)
        d = eval(d.decode())
        le = d['le']
        del d['le']
        # print(d)
        datas = b''
        while True:
            # print('while')
            data = s.recv(100000)
            datas += data
            if len(datas) >= le:
                # print('break')
                break
        s.send(b'1')
        im = Image.frombytes(data=datas, **d)
        try:
            i.paste(im)
        except:
            pass


def loop(s):
    ima = Image.open('0.gif')
    root = tkinter.Toplevel()
    # 设置窗口居中
    x = root.winfo_screenwidth() // 2  # 获取屏幕宽度
    y = root.winfo_screenheight() // 2  # 获取屏幕高度
    width = 850
    height = 630
    root.geometry('%dx%d+%d+%d' % (width, height, x - width // 2, y - height // 2))
    try:
        i = ImageTk.PhotoImage(ima)
    except:
        pass
    lb = tkinter.Label(root, image=i)
    # 修改 窗口自适应大小
    lb.pack(expand=1)
    t = Thread(target=change_i, args=(s, i))
    t.setDaemon(True)
    t.start()
    # root.mainloop()


def wait_connect():
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ADDR = ('', 7999)
    sock.bind(ADDR)
    sock.listen(1)
    try:
        # print('accept 1')
        s, addr = sock.accept()
        # print('accept 2')
        loop(s)
    except Exception:
        traceback.print_exc()
        s.close()
        sock.close()


def main():
    th = Thread(target=wait_connect)
    th.setDaemon(True)
    th.start()
    # wait_connect()

