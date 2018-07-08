import datetime
import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox


class Win(threading.Thread):

    def __init__(self, name, ip):
        super().__init__()
        self.name = name  # 昵称
        self.ip = ip
        self.port = 9998

    def run(self):
        self.win = Tk()
        self.win.title('与%s聊天中' % self.name)
        self.win.resizable(0, 0)  # 设置窗口大小不可变

        self.msg_frame = Frame(self.win)
        self.send_frame = Frame(self.win)

        self.msg()
        self.write()

        self.msg_frame.grid(row=0, column=0, padx=10)
        self.send_frame.grid(row=1, column=0, padx=10, pady=10)
        self.win.bind('<Return>', self.send_msg)  # 绑定事件， 回车发消息

        # a = threading.Thread(target=self.recv_msg)
        # a.setDaemon(True)
        # a.start()
        self.win.mainloop()

    # 会话窗口
    def msg(self):
        self.test = Text(self.msg_frame, wrap=WORD)
        self.test = scrolledtext.ScrolledText(self.msg_frame, wrap=WORD, height=33)
        self.test.grid(row=0, column=0)
        self.test.config(state=DISABLED)  # 设置会话窗口不可编辑
        self.test.see(END)

    # 消息发送窗口
    def write(self):
        height = 10
        self.send = scrolledtext.ScrolledText(self.send_frame, height=height, )
        self.send_button = ttk.Button(self.send_frame, text='发送', command=self.send_msg)
        self.send.pack()
        self.send_button.pack(side=RIGHT, pady=5)

    # 发送消息
    def send_msg(self, event=None):
        self.message = self.send.get(index1='0.0', index2='end')  # 获取消息内容
        print(self.message)
        self.test.config(state=NORMAL)  # 解锁会话窗口
        user_name = self.name  # 用户名
        time = str(datetime.datetime.now()).split('.')[0]  # 时间
        self.test.insert(END, user_name + ' ' + time + ':\n', 'green')
        self.test.insert(END, self.message)
        self.test.tag_configure('green', foreground='#008B00')
        self.test.config(state=NORMAL)  # 上锁会话窗口
        self.test.see(END)
        if self.message != '\n':
            date = str(datetime.datetime.now()).split('.')[0]
            self.send.delete(index1='0.0', index2='end')  # 清空输入框内容
            """
            发送消息内容到服务器
            """
            self.send_to_host(self.name, self.message, self.ip)  # 发消息
        else:
            messagebox.showwarning('警告', '消息不能为空')

    def send_to_host(self, name, message, host):
        # print("测试send_to_host 开始", self.ip)
        host = host
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.connect((host, 9998))

        user_name = name  # 用户名
        time = str(datetime.datetime.now()).split('.')[0]  # 时间
        sk.sendall((user_name + ' ' + time + ':\n' + message).encode())
        sk.close()

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return str(ip)

    # def recv_msg(self):
    #     sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #     sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     sk.bind((self.get_host_ip(), self.port))
    # 
    #     while True:
    #         msg, addr = sk.recvfrom(4096)
    #         print(msg.decode())
    #         date = ''.join(msg.decode().split(':')[:-1:])
    #         msg = msg.decode().split(':')[-1]
    #         self.test.config(state=NORMAL)  # 解锁会话窗口
    # 
    #         self.test.insert(END, date + '\n', 'green')  # 会话窗口插入时间
    #         self.test.insert(END, msg)  # 会话窗口插入消息内容
    #         self.test.tag_configure('green', foreground='#008B00')  # 设置颜色
    #         self.test.see(END)  # 始终展示最低端
    # 
    #         self.test.config(state=DISABLED)  # 插入结束冻结窗口


if __name__ == '__main__':
    th = Win('name', '127.0.0.1')
    th.start()
