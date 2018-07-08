# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Wu Yan Jun
# Email: 527439841@qq.com

"""
初次运行时，会让用户输入主机IP地址，
"""

import os
import tkinter
from tkinter import ttk
from tkinter import messagebox


from office_worker_system.sys_client.lib import register_win


# 检查是否已获取主机ip
def check_if_host_exists():
    path = r'host_data\\'
    try:
        os.makedirs(path)
    except Exception:
        pass

    # 判断文件是否存在
    if os.path.isfile(path + 'host_ip.txt'):
        with open(path + 'host_ip.txt', 'r') as file:
            ip = file.readlines()[0]
            if check_(ip):
                register_win.Login(ip)
            else:
                get_ip_win()
    else:
        get_ip_win()


def get_ip_win():
    win = tkinter.Tk()

    height = win.winfo_screenheight() // 2  # 获取当前屏幕高度
    width = win.winfo_screenwidth() // 2  # 获取当前屏幕宽度
    win.geometry('300x150+%d+%d' % (width, height))  # 设定窗口位置与大小
    win.resizable(0, 0)  # 设定窗口大小不可变

    num = 30
    ttk.Label(win, text='主机IP').grid(row=0, column=0, padx=num, pady=num)
    ip_entry = ttk.Entry(win)
    ip_entry.grid(row=0, column=1, padx=num, pady=num)

    # 弹出登录、注册窗口
    def go(event=None):
        ip = ip_entry.get()
        if check_(ip):
            with open(r'host_data\host_ip.txt', 'w') as file:
                file.write(ip)
            win.destroy()
            register_win.Login(ip)
        else:
            messagebox.showwarning('提示', 'IP地址无响应，请更换地址')

    ttk.Button(win, text='确定', command=go).grid(row=1, columnspan=2, padx=num // 2, pady=num // 2)
    win.bind('<Return>', go)
    win.mainloop()


# 判断ip是否有效
def check_(ip):
    cmd = 'ping ' + ip
    result = os.popen(cmd).read()
    if '传输失败' in result or '请求超时' in result:
        return False
    else:
        return True


if __name__ == '__main__':
    check_if_host_exists()
