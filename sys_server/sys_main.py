import socket
import threading
import pymysql
import traceback
import time

# 导入提供客户端下载模块
from office_worker_system.sys_server import module_down_load_server
# 导入提供客户端上传模块
from office_worker_system.sys_server.module_up_load_server import exce_request_str_to_list
# 导入共享服务器桌面模块
from office_worker_system.sys_server import make

# 创建字典 存放 昵称，ip地址信息，tcp线程
conn_dict = {}


def recv():
    global conn_dict

    # 广播
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = ''
    port = 9999
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 固定端口信号
    sk.bind((host, port))

    while True:
        try:
            message, addr = sk.recvfrom(4096)
            message = message.decode()
            title = addr[0]
            print('客户端消息内容', [message])
            print('IP 地址：', title)
            # 发送来的信息解码　分割为列表　并分别赋值
            request = ''
            if '@@@' in message:
                request, data = message.split('@@@')
                print(request)

            if '注册' in message or '登陆' in message:
                name = message.split(':')[1]
                passwd = message.split(':')[2]
                result = save(name=name, passwd=passwd)
                if title not in conn_dict:
                    # 开启一个tcp线程连接客户端
                    th = Server_tcp(name, title)
                    print('tcp线程开启')
                    th.setDaemon(True)
                    th.start()
                    # 字典中添加内容
                    conn_dict[name] = (title, port)
                    print('线程开启后', conn_dict)

                sk.sendto(result, (title, port))
                continue
            elif 'upload' in request:
                print("server,upload")
                exce_request_str_to_list(data)
            elif 'see' in request:
                print(request, addr)
                make.main(addr[0])
            else:
                for i in conn_dict:
                    send(conn_dict[i][0], message)
        except (KeyboardInterrupt, SyntaxError):
            raise
        except Exception as e:
            traceback.print_exc()


def send(host, message):
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 9998
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.connect((host, port))
    sk.sendall(message.encode())
    sk.close()


# 数据库操作
def save(name, passwd=None):
    connect = pymysql.connect('localhost', 'root', '123456', charset='utf8')
    cursor = connect.cursor()
    excute = cursor.execute
    try:
        excute('use feiq')
    except:
        excute('create database feiq')
        excute('use feiq')
    try:
        excute('select name from feiq')  # 查看已有用户名
        result = cursor.fetchall()
        if (name,) not in result:  # 判断用户名是否已存在
            excute('insert into feiq(name, passwd) values("%s", "%s");' % (name, passwd))
            return str('ok').encode()
        else:
            excute('select name,passwd from feiq')  # 查看已有用户名、密码
            result = cursor.fetchall()
            if (name, passwd) in result:  # 判断登陆的账户名与密码是否匹配
                print('match')
                return str('match').encode()
            else:
                print('failed')
                return 'failed'.encode()
    except:
        excute('create table feiq(id int primary key auto_increment, name char(20), passwd char(20))')
        excute('insert into feiq(name, passwd) values("%s", "%s");' % (name, passwd))
        return str('ok').encode()
    finally:
        connect.commit()
        cursor.close()
        connect.close()


def check(name, passwd):
    connect = pymysql.connect('localhost', 'root', '123456', charset='utf8')
    cursor = connect.cursor()
    excute = cursor.execute
    excute('use feiq')
    excute('select name, passwd from feiq')
    result = cursor.fetchall()
    try:
        if (name, passwd) in result:
            return str(True).encode()
        else:
            return str(False).encode()
    finally:
        print(result)
        connect.commit()
        cursor.close()
        connect.close()


# tcp线程类--连接客户端
class Server_tcp(threading.Thread):
    def __init__(self, name, host):
        super().__init__()
        self.host = host
        self.name = name
        self.port = 9997

    def run(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.connect((self.host, self.port))
        while True:
            try:
                content = sk.recvfrom(4096)
            except:
                print('退出登陆')
                # 删除退出的用户
                conn_dict.pop(self.name)
                print('tcp线程结束', conn_dict)
                break
        sk.close()


# 定时将在线人列表 发送给每个客户端
def send_person_list():
    while True:
        # 在线列表刷新时间
        time.sleep(1)

        for i in conn_dict:
            ip = conn_dict[i][0]
            msg = '@@@' + str(conn_dict)
            send(ip, msg)


if __name__ == '__main__':
    th1 = threading.Thread(target=recv)
    th1.start()
    th2 = threading.Thread(target=send_person_list)
    th2.start()
