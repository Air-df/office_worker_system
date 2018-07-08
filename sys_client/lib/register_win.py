from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from office_worker_system.sys_client.lib import main_win
# import win32api
import socket
import threading


class Login:

    # 登陆界面
    def __init__(self, host):
        # 创建tcp
        th = Client_tcp(self.get_host_ip())
        # 主线程结束，该线程也结束
        th.setDaemon(True)
        th.start()

        self.host = host         # 主机IP
        self.port = 9999                    # 通讯端口

        self.win = Tk()

        self.win.title("Sky")
        self.win.geometry("550x450+700+300")
        self.label_username = ttk.Label(self.win, text="用户名")
        self.label_password = ttk.Label(self.win, text="密码")
        self.entry_username = ttk.Entry(self.win)
        self.entry_password = ttk.Entry(self.win, show='*')
        self.button_denglu = ttk.Button(self.win, text="登录", command=self.check)
        self.button_login = ttk.Button(self.win, text="注册", command=self.login)

        self.label_username.grid(row=0, rowspan=3, columnspan=2, column=0, ipadx=30, ipady=50)
        self.label_password.grid(row=4, rowspan=3, columnspan=2, column=0, ipadx=30, ipady=50)
        self.entry_username.grid(row=0, rowspan=3, columnspan=2, column=3, ipadx=10, )
        self.entry_password.grid(row=4, rowspan=3, columnspan=2, column=3, ipadx=10, )
        self.button_denglu.grid(row=7, rowspan=3, columnspan=3, column=0, padx=100, )
        self.button_login.grid(row=7, rowspan=3, columnspan=3, column=3, ipadx=10, )

        # 发送 账户信息到服务器
        self.win.bind('<Return>', self.check)    # 实现回车登录 绑定事件失败
        self.win.mainloop()

    def login(self):
        # 注册窗口
        self.win_login = Tk()
        self.win_login.title('注册窗口')
        self.win_login.title("新用户注册")

        self.new_username = Label(self.win_login, text="用户名")
        self.new_password = Label(self.win_login, text="密码")
        self.entry_new_username = Entry(self.win_login)
        self.entry_new_password = Entry(self.win_login)
        self.button_new_button = Button(self.win_login, text="注册", command=self.check_login)

        self.new_username.grid(row=0, column=0)
        self.new_password.grid(row=1, column=0)
        self.entry_new_username.grid(row=0, column=1)
        self.entry_new_password.grid(row=1, column=1)
        self.button_new_button.grid(row=2, columnspan=3, )

        self.win_login.mainloop()

    def check_login(self):
        name = self.entry_new_username.get()
        passwd = self.entry_new_password.get()
        if len(passwd) < 6:
            messagebox.showwarning(message='密码至少为6位')
            return
        if not name:
            messagebox.showwarning(message='用户名不能为空')
            return
        message = '注册:' + name + ':' + passwd
        self.send(message)
        self.recv()
        if self.message.decode() == 'ok':
            print('ok')
            messagebox.showwarning(message='注册成功')
            self.win_login.destroy()  # 关闭注册窗口
            self.win.destroy()  # 关闭登录窗口
            user_name = main_win.Win(name, self.host)  # 弹出聊天窗口
            user_name.start()
        else:
            messagebox.showwarning(message='用户名已存在')
            return

    def check(self, event=None):
        name = self.entry_username.get()
        passwd = self.entry_password.get()
        message = '登陆:' + name + ':' + passwd
        self.send(message)

        # 2018-6-13 增加连接超时提醒
        if self.recv():
            messagebox.showwarning(message='主机未响应，连接超时')

        elif self.message.decode() == 'match':
            self.win.destroy()                  # 关闭登录窗口
            user = main_win.Win(name, self.host)
            user.start()
        else:
            messagebox.showwarning(message='账户名或密码错误')

    def get_host_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return str(ip)

    def send(self, message):
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.connect((self.host, self.port))
        sk.sendall(message.encode())
        sk.close()

    def recv(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 2018-6-3 修改 设置连接等待时间
        self.sk.settimeout(3)
        try:
            self.sk.bind((self.get_host_ip(), 9999))
            message, addr = self.sk.recvfrom(4096)
            self.message = message
            self.sk.close()

        except socket.timeout:
            return True


class Client_tcp(threading.Thread):
    def __init__(self, host):
        super().__init__()
        self.host = host
        self.port = 9997

    def run(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.bind((self.host, self.port))
        sk.listen(1)
        while True:
            conn, addr = sk.accept()


if __name__ == '__main__':
    Login('172.88.13.197')

