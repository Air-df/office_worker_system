#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# coding:utf-8
# Author: Li Xin Hao

"""
此模块提供客户端上传

过程
    １．通过文件路径　确定上传文件数量n
    ２．创建一个套接字，开启n个进程等待服务器来连接
    ３．连接成功后，开始上传

需要参数：
    服务器的addr ,  和 udpsock
"""

# 需要的包
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
from socket import *
from multiprocessing import *
from threading import *
import traceback, signal
import time, sys

'''
获取文件路径
'''


# path = askdirectory()  #　单个文件夹
# path = askopenfilename()　 #单个文件
# 获取文件们的路径(tuple)　和　文件名(list)


def get_filespaths_and_filesnames():
    # 　获取文件的路径的元祖
    paths_tuple = askopenfilenames()
    # 获取文件名
    filenames_list = [i.split('/')[-1] for i in paths_tuple]
    # print(type(paths_tuple),paths_tuple)
    # print(type(filenames_list),filenames_list)
    return paths_tuple, filenames_list


'''
开启进程　等待服务器来链接
'''


def open_transmit_process(targetaddr, tcpsock, pf):
    print('in open')
    # 等待赋值目标套接字
    targetsock = ''
    # 一直等待服务器链接
    while True:
        # 出错关闭套接字
        try:
            server, addr = tcpsock.accept()
        except:
            server.close()
        print(addr[0], targetaddr)
        if addr[0] == targetaddr[0]:
            targetsock = server
            break
        else:
            server.close()
    # 第一次发送文件名字
    targetsock.send(pf[1].encode())
    print('<<<', pf[1])
    # 等待服务器回发确认链接
    msg = targetsock.recv(1024).decode()
    print('>>>', msg)
    # 打开文件夹　开始发送文件流
    # 出错，或者传输完成都关闭套接字
    time.sleep(1)
    try:
        with open(pf[0], 'rb') as f:
            how = 0
            print('开始发送')
            while True:
                data = f.read(200000)
                targetsock.send(data)
                how += len(data)
                # 如果读取为空先发送，然后结束循环
                if not data:
                    break
            print('发送结束', how)
    finally:
        server.close()
        print('发送线程结束')
        # signal.signal(os.getpid(),signal.SIGKILL)


'''
　　　创建套接字，等待服务器来连接
'''


# 获取本机IP
def get_host_ip():
    try:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return str(ip)


# udpsock
def create_tcpsock_wait_server_connect(addr, udpsock):
    try:
        # 得到文件的　路径元祖　和　文件　名字
        paths_tuple, filenames_list = get_filespaths_and_filesnames()
        # 创建tcp套接字
        HOST = get_host_ip()
        PORT = 3349
        # 绑定ADDR
        ADDR = (HOST, PORT)
        # 创建套接字
        sock = socket()
        # 设置重用
        sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        sock.bind(ADDR)
        sock.listen(5)
        # 根据文件的数量开启相应个数的进程
        p_list = []  # 存放进程
        print(paths_tuple, filenames_list)
        for i in zip(paths_tuple, filenames_list):
            print(i)
            # 开启线程
            p = Thread(target=open_transmit_process, args=(addr, sock, i))
            p.start()
            p_list.append(p)
        # 告诉UDPsock 可以链接了,　以列表字符串发送，让其判断开几个线程收
        udpsock.sendto(('upload@@@' + str(filenames_list) + '@u@' + str(ADDR)).encode(), addr)
        # sys.exit()
        # 设置阻塞回收进程
        for i in p_list:
            i.join()
            print('线程回收')
        print('000000000000000000000000000000')
        sock.close()
    except Exception:
        traceback.print_exc()
        # signal.signal(os.getpid(),signal.SIGKILL)


def main(addr, udpsock):
    # Thread(target = create_tcpsock_wait_server_connect,args=(addr, udpsock)).start()
    # a = Thread(target = create_tcpsock_wait_server_connect,args=(addr, udpsock))
    # a.start()
    # a.join()
    create_tcpsock_wait_server_connect(addr, udpsock)
