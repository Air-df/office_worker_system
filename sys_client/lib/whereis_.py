#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# coding:utf-8
# Author: Li Xin Hao

import ctypes, os, sys, time
from multiprocessing import *
from threading import Thread
import tkinter, win32con
import win32clipboard as w


def set_string_to_clipboard(str):
    # w.OpenClipboard()
    # w.EmptyClipboard()
    # # for i in str:
    # w.SetClipboardData(win32con.CF_TEXT,str)
    # w.CloseClipboard()
    r = tkinter.Tk()
    r.clipboard_clear()
    r.clipboard_append(str)
    r.destroy()


def getroots():
    lpBuffer = ctypes.create_string_buffer(78)
    ctypes.windll.kernel32.GetLogicalDriveStringsA(ctypes.sizeof(lpBuffer), lpBuffer)
    l = [i.decode() for i in list(lpBuffer) if i != b'\x00']
    roots = [''.join(l[(i - 1) * 3:i * 3]) for i in range(1, len(l) // 3 + 1)]
    print(roots)
    return roots


def search_one_root(namestr, root, put, lisb):
    for rdf in os.walk(root):
        for i in rdf[1:]:
            for j in i:
                if namestr in j:
                    msg = rdf[0] + '\\' + j
                    lisb.insert(tkinter.END, msg)
                    # put.send(msg)
    # put.send('')


def search(namestr, lisb):
    roots = getroots()
    get, put = Pipe(duplex=False)
    # p_list=[]
    for root in roots:
        p = Thread(target=search_one_root, args=(namestr, root, put, lisb))
        p.start()
        # p_list.append(p)
    # n=len(roots)
    # while n>0:
    #     msg = get.recv()
    #     if not msg:
    #         print(msg)
    #         lisb.insert(tkinter.END,msg)
    #         n-=1
    #         print(n)
    # for i in p_list:
    #     i.join()


def main():
    root = tkinter.Toplevel()
    ## 输入窗口体
    f = tkinter.Frame(root)
    f.pack(fill=tkinter.X)
    # 提示
    f_lb = tkinter.Label(f, text='文件名字>>')
    f_lb.pack(side=tkinter.LEFT, fill=tkinter.X)
    # 输入框
    f_et = tkinter.Entry(f, width=80)
    f_et.pack(side=tkinter.LEFT, fill=tkinter.X)

    # 搜索按钮
    def lb_func():
        lisb.delete(0, tkinter.END)
        namestr = f_et.get()
        print(namestr)
        if namestr:
            search(namestr, lisb)

    lb = tkinter.Button(root, text='按钮<<开始搜索>> 1.双击左键打开 2.双击右键复制路径到剪贴板', command=lb_func)
    lb.pack(fill=tkinter.X)
    # 搜索出结果的框
    lisb = tkinter.Listbox(root, height=50, selectmode=tkinter.BROWSE)

    def double_1(e):
        print('double_1')
        file = lisb.selection_get()
        print(file)
        if file:
            os.startfile(file)

    lisb.bind('<Double-Button-1>', double_1)

    def double_3(e):
        print('double_3')
        file = lisb.selection_get()
        if file:
            set_string_to_clipboard(file)

    lisb.bind('<Double-Button-3>', double_3)
    lisb.pack(fill=tkinter.BOTH)

    # a = time.time()
    # search(namestr)
    # print(time.time()-a)


if __name__ == '__main__':
    # Process(target=main).start()
    # main('')
    # os.startfile(r"C:\Users\Administrator\Desktop\mangodb")
    # os.startfile(r"C:\Users\Administrator\Desktop\配置jupyter默认浏览器.txt")
    pass
