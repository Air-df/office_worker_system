# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Wu Yan Jun & Li Xin Hao

"""
程序运行主界面
"""

import datetime
import socket
import threading
import multiprocessing
import time, json, random, hashlib
from urllib import request, parse
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

####
# 导入客户端下载模块
from office_worker_system.sys_client.lib.module_down_load_client import down_load_from
# 导入客户端上传模块
from office_worker_system.sys_client.lib.module_up_load_client import main as up_main
# 导入以下模块，按功能顺序依次为：放松以下（贪吃蛇）、文件查找、私聊窗口、消息弹出、记录保存、远程视图、界面设置、天气获取
from office_worker_system.sys_client.lib import snake, whereis_, personal, message_out, save_records, get, set_alpha, \
    get_wether


class Win(multiprocessing.Process):
    def __init__(self, name, host):
        super().__init__()
        self.name = name  # 昵称
        self.host_ip = host

    def run(self):
        self.win = Tk()
        self.win.title('Fly')

        # 设置窗口居中
        x = self.win.winfo_screenwidth() // 2  # 获取屏幕宽度
        y = self.win.winfo_screenheight() // 2  # 获取屏幕高度
        width = 850
        height = 670
        self.win.geometry('%dx%d+%d+%d' % (width, height, x - width // 2, y - height // 2))
        self.win.resizable(0, 0)  # 设置窗口大小不可变
        #################
        # self.win.overrideredirect(True)
        self.win.attributes("-alpha", 1)  # 窗口透明度80 %
        self.xx, self.yy = 0, 0

        def move(event):
            # global xx, yy
            new_x = (event.x - self.xx) + self.win.winfo_x()
            new_y = (event.y - self.yy) + self.win.winfo_y()
            s = "850x680+" + str(new_x) + "+" + str(new_y)
            self.win.geometry(s)

        self.win.bind("<B1-Motion>", move)

        self.msg_frame = Frame(self.win)
        self.person_frame = Frame(self.win)
        self.send_frame = Frame(self.win)
        self.file_frame = Frame(self.win)
        self.weather_frame = Frame(self.msg_frame)

        th = threading.Thread(target=self.weather)
        th.setDaemon(True)
        th.start()
        self.msg()
        self.write()
        self.person()
        self.file()

        self.msg_frame.grid(row=1, column=0, padx=10, pady=5)
        self.person_frame.grid(row=1, column=1, padx=10, pady=10)
        self.send_frame.grid(row=2, column=0, padx=10, pady=5)
        self.file_frame.grid(row=2, column=1, padx=10, pady=10)
        self.weather_frame.grid(row=0, padx=10, pady=5)
        self.win.bind('<Return>', self.send_msg)  # 绑定事件， 回车发消息

        a = threading.Thread(target=self.recv_msg)
        a.setDaemon(True)
        a.start()
        self.win.mainloop()

    # 会话窗口
    def msg(self):
        self.test = scrolledtext.ScrolledText(self.msg_frame, wrap=WORD, height=33)
        self.test.grid(row=1, column=0)
        self.test.config(state=DISABLED)  # 设置会话窗口不可编辑

    # 消息发送窗口
    def write(self):
        height = 10
        self.send = scrolledtext.ScrolledText(self.send_frame, height=height, )
        self.send_button = ttk.Button(self.send_frame, text='发送', command=self.send_msg)
        self.save_button = ttk.Button(self.send_frame, text='保存聊天记录', command=self.save)
        self.send.pack()
        self.send_button.pack(side=RIGHT, pady=5)
        self.save_button.pack(side=RIGHT, pady=5)

    # 在线人数列表
    def person(self):
        # 个人信息Frame
        my_frame = Frame(self.person_frame)

        # 昵称
        info_frame = Frame(my_frame)
        Label(info_frame, text=self.name, fg='green', font=('微软雅黑', 13)).pack(padx=10, pady=10)
        info_frame.pack()
        my_frame.pack(side=TOP)

        # 在线成员
        self.lbox = Listbox(self.person_frame, width=30, height=23, selectmode=BROWSE)  # 通过鼠标的移动选择
        self.lbox.bind('<Double-Button-1>', self.double_click)
        self.lbox.pack()

    # 功能按钮
    def file(self):
        长 = 10
        宽 = 8
        ####8
        ttk.Button(self.file_frame, text='上传文件', command=self.upload_file).grid(padx=长, pady=宽, row=0, column=0)
        ttk.Button(self.file_frame, text='下载文件', command=self.download).grid(padx=长, pady=宽, row=0, column=1)
        ttk.Button(self.file_frame, text='远程视图', command=self.see).grid(padx=长, pady=宽, row=1, column=0)
        ttk.Button(self.file_frame, text='自动翻译', command=self.translate_win).grid(padx=长, pady=宽, row=1, column=1)
        ttk.Button(self.file_frame, text='搜索文件', command=self.search).grid(padx=长, pady=宽, row=2, column=0)
        ttk.Button(self.file_frame, text='放松一下', command=self.play).grid(padx=长, pady=宽, row=2, column=1)
        ttk.Button(self.file_frame, text='界面设置', command=self.set_alpha_func).grid(padx=长, pady=宽, row=3, column=0)
        ttk.Button(self.file_frame, text='我要退出', command=self.destroy_all_func).grid(padx=长, pady=宽, row=3, column=1)

    # 天气显示
    def weather(self):
        num = 15
        ttk.Label(self.weather_frame, text='城市', width=6).grid(row=0, column=0)
        ttk.Label(self.weather_frame, text='天气', width=6).grid(row=0, column=2)
        ttk.Label(self.weather_frame, text='温度', width=6).grid(row=0, column=4)
        self.location_label = ttk.Label(self.weather_frame, text='hold on 。。。', width=20)
        self.weather_label = ttk.Label(self.weather_frame, text='wait a second。。。', width=20)
        self.temp_label = ttk.Label(self.weather_frame, text='searching。。。', width=20)
        self.location_label.grid(row=0, column=1)
        self.weather_label.grid(row=0, column=3)
        self.temp_label.grid(row=0, column=5)
        try:
            info = get_wether.main()
            self.location_label.config(text=info[0])
            self.weather_label.config(text=info[1])
            if info[2]:
                temp = info[2] + '~' + info[3]
            else:
                temp = info[3]
            self.temp_label.config(text=temp)
        except:
            info = '网络不畅。。。'
            self.location_label.config(text=info)
            self.weather_label.config(text=info)
            self.temp_label.config(text=info)

    # 获取发送消息内容
    def send_msg(self, event=None):
        self.message = self.send.get(index1='0.0', index2='end')  # 获取消息内容

        if self.message != '\n\n':
            self.send.delete(index1='0.0', index2='end')  # 清空输入框内容
            # 发送消息内容到服务器
            self.send_to_host()
        else:
            messagebox.showwarning('警告', '消息不能为空')

    # 退出
    def destroy_all_func(self):
        self.win.destroy()
        sys.exit(0)

    # 导入设置透明度按钮
    def set_alpha_func(self):
        set_alpha.main(self.win)

    # 导入放松一下按钮函数
    def play(self):
        snake.choice()

    # 搜索文件按钮
    def search(self):
        whereis_.main()

    # 获取要上传的文件
    def get_file(self):
        self.upload_file()

    # 发送文件到服务器
    def upload_file(self):
        host = self.host_ip
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        up_main((host, 9999), sk)

    # 下载操作
    def download(self):
        down_load_from(self.host_ip)

    # 远程视图
    def see(self):
        def go():
            host = self.host_ip
            sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            datas = 'see' + '@@@'
            sk.sendto(datas.encode(), (host, 9999))
            print(datas)
            get.main()
        th = threading.Thread(target=go)
        th.setDaemon(True)
        th.start()

    # 翻译窗口
    def translate_win(self):
        win = Tk()
        win.title('在线翻译')
        width = win.winfo_screenwidth() // 2
        win.geometry('400x200+%d+0' % width)
        win.resizable(0, 0)

        num = 5
        self.translate_text = scrolledtext.ScrolledText(win, width=60, height=5)
        self.translate_text.pack(padx=num, pady=num)

        ttk.Button(win, text='查询', command=self.insert_into_translate).pack(fill=BOTH)

        self.result = scrolledtext.ScrolledText(win, width=60, height=5, stat=DISABLED)
        self.result.pack(padx=num, pady=num)

        win.bind('<Return>', self.insert_into_translate)
        win.mainloop()

    # 双击好友列表--弹出私聊窗口
    def double_click(self, event):
        # 拿到对应名字的IP，sendto 发消息
        name = self.lbox.selection_get()
        addr = self.conn_dict[name]
        print([name, addr[0]])
        new_win = personal.Win(name, addr[0])
        new_win.setDaemon(True)
        new_win.start()

    # 保存聊天记录
    def save(self):
        data = self.test.get(index1='0.0', index2='end')
        save_records.func(data)

    # 获取本机ip
    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return str(ip)

    # 发送消息到服务器
    def send_to_host(self):
        host = self.host_ip
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.connect((host, 9999))

        user_name = self.name  # 用户名
        time = str(datetime.datetime.now()).split(' ')[1].split('.')[0]  # 时间
        sk.sendall((user_name + ' ' + time + ':' + self.message).encode())

        sk.close()

    # 接收消息并更新对话框
    def recv_msg(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.bind((self.get_host_ip(), 9998))

        # 线程字典 用户名：对应线程
        th_dict = {}
        while True:
            msg, addr = sk.recvfrom(4096)

            # 判断消息是否为消息人列表
            if '@@@' in msg.decode():
                """
                获取在线人员信息
                显示在线人员列表
                """
                # 处理消息列表 转换为字典形式
                self.conn_dict = eval(msg.decode().split('@@@')[1])
                # 清空在线列表
                self.lbox.delete(0, END)
                # 重新插入在线人员
                for i in self.conn_dict:
                    self.lbox.insert(END, i)
            else:
                print(msg.decode(), addr)
                date = ':'.join(msg.decode().split(':')[:-1:])
                name = date.split()[0]
                msg = msg.decode().split(':')[-1]

                # 判断是否为主机消息
                if addr[0] == self.host_ip:
                    self.test.config(state=NORMAL)  # 解锁会话窗口

                    self.test.insert(END, date + '\n', 'green')  # 会话窗口插入时间
                    self.test.insert(END, '  ' + msg)  # 会话窗口插入消息内容
                    self.test.tag_configure('green', foreground='#008B00')  # 设置颜色
                    self.test.see(END)  # 始终展示最低端

                    self.test.config(state=DISABLED)  # 插入结束冻结窗口

                # 非主机消息则弹出消息提醒
                else:
                    # 判断是否为第一次弹出
                    if name not in th_dict:
                        # if not th_dict[name].is_alive():
                        th = message_out.func(msg, name, addr[0])
                        th.setDaemon(True)
                        th.start()
                        th_dict[name] = th
                    else:
                        # 刷新提示框内容
                        try:
                            th_dict[name].tk_message.config(text=msg)
                        except:
                            print(th_dict[name].is_alive())
                            try:
                                th_dict[name].message = msg
                                win = th_dict[name].dict[name]
                                th_dict[name].change_msg(win, name, msg)
                            except:
                                if not th_dict[name].is_alive():
                                    th = message_out.func(msg, name, addr[0])
                                    th.setDaemon(True)
                                    th.start()
                            #         th_dict[name] = th

    def insert_into_translate(self, event=None):
        msg = self.translate_text.get(index1='0.0', index2='end')
        self.translate_text.delete(index1='0.0', index2='end')

        th = threading.Thread(target=self.translate, args=(msg,))
        th.setDaemon(True)
        th.start()

    def translate(self, msg):
        self.result.config(stat=NORMAL)
        self.result.delete(index1='0.0', index2='end')
        self.result.insert(END, '%s翻译中，请稍等。。。。。' % msg)
        self.result.config(stat=DISABLED)

        content = msg
        base_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        # Request URL:http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule  注释内的有个_o，
        # 如果不删除会显示errorCode=50，并不会给出翻译结果。删除就解决了

        data = {}  # 定义一个字典用来接收传给服务器的内容

        u = 'fanyideskweb'
        d = content
        f = str(int(time.time() * 1000) + random.randint(1, 10))
        c = 'rY0D^0\'nM0}g5Mm1z%1G4'

        sign = hashlib.md5((u + d + f + c).encode('utf-8')).hexdigest()
        # 引号内容为固定
        data['i'] = content  # 需要翻译的内容
        data['from'] = 'AUTO'
        data['to'] = 'AUTO'
        data['smartresult'] = 'dict'
        data['client'] = 'fanyideskweb'
        data['salt'] = f
        data['sign'] = sign
        data['doctype'] = 'json'
        data['version'] = '2.1'
        data['keyfrom'] = 'fanyi.web'
        data['action'] = 'FY_BY_CL1CKBUTTON'
        data['typoResult'] = 'true'

        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(base_url, data=data)
        try:
            response = request.urlopen(req)
            res = response.read().decode('utf-8')
            res = json.loads(res)
            res = res['translateResult'][0][0]['tgt']

            self.result.config(stat=NORMAL)
            self.result.delete(index1='0.0', index2='end')
            self.result.insert(END, msg)
            self.result.insert(END, res)
            self.result.config(stat=DISABLED)
        except:
            self.result.config(stat=NORMAL)
            self.result.delete(index1='0.0', index2='end')
            self.result.insert(END, '查询失败\n请检查网络设置!!')
            self.result.config(stat=DISABLED)


if __name__ == '__main__':
    a = Win('air', '127.0.0.1')
    a.start()
