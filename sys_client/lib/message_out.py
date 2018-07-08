# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Wu Yan Jun

"""
客户端收到私聊消息后，弹出消息内容
实现方法：
    法1：利用 MessageBox 自定义弹出内容，但是，会显示两个窗口，返回值太过单一，重定义功能太过麻烦
    法2：自己写个？ 可以的， 思路：搞个窗口，显示个message，加俩按钮，绑定两个函数处理不同操作
"""

import tkinter
import datetime
import threading
from tkinter import ttk

from office_worker_system.sys_client.lib import personal


class func(threading.Thread):
    def __init__(self, message, name, ip):
        super().__init__()
        self.message = message
        self.name = name
        self.ip = ip
        self.dict = {}

    def run(self):
        self.tk = tkinter.Tk()
        # 窗口名称
        self.tk.title('{}的消息'.format(self.name))

        # 获取客户端窗口大小
        width = self.tk.winfo_screenwidth()
        height = self.tk.winfo_screenheight()

        # 显示位置
        self.tk.geometry('200x200+%d+%d' % (width - 220, height - 280))

        # 设置窗口大小不可变
        self.tk.resizable(0, 0)

        # 消息内容
        self.tk_message = tkinter.Message(self.tk, text=self.message)  # expand=1 居中显示
        self.tk_message.pack(expand=1)

        # 查看、取消按钮
        self.frame = tkinter.Frame(self.tk)
        ttk.Button(self.frame, text='查看', command=self.read).grid(row=0, column=0, padx=2, pady=2)
        ttk.Button(self.frame, text='忽略', command=self.tk.quit).grid(row=0, column=1, padx=2, pady=2)
        self.frame.pack(side=tkinter.BOTTOM)

        self.tk.mainloop()

    # 查看消息 -- 接入私聊窗口
    def read(self):
        self.tk.destroy()
        new_win = personal.Win(self.name, self.ip)
        new_win.setDaemon(True)
        new_win.start()
        self.dict[self.name] = new_win

    # 改变私聊窗口消息内容
    def change_msg(self, win, name, msg):
        win.test.config(state=tkinter.NORMAL)
        time = name + str(datetime.datetime.now()).split('.')[0]
        win.test.insert(tkinter.END, time, 'green')
        win.test.insert(tkinter.END, msg)
        win.test.tag_configure('green', foreground='#008B00')
        win.test.config(state=tkinter.DISABLED)
        win.test.see(tkinter.END)


if __name__ == '__main__':
    a = func('老婆', 'air', '127.0.0.1')
    a.start()
    # a.tk_message.config(text='新内容') # 刷新消息内容
