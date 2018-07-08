#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# coding:utf-8
# Author: Li Xin Hao

"""
主机开启的时候自动开始提同下载的服务端
引入此模块自动开启
"""
import os
import threading


def go():
    os.chdir('datas')
    # os.system('cd ..')
    # print(os.getcwd())
    # # os.system('cd /D E:\\Pycharm_obj\\s\\datas')
    # print(os.getcwd())
    print('下载开启')
    os.system('python -m http.server 3000')
    print('下载关闭')


def main():
    threading.Thread(target=go).start()


main()
