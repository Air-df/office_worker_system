#!/usr/bin/python3
# -*- coding:UTF-8 -*-
# coding:utf-8
# Author: Li Xin Hao

import threading
import webbrowser as web  # 对导入的库进行重命名
import os, traceback, signal


# 主机地址
# _url = '172.88.13.138:8000'
# 使用浏览器名字
# _name = 'firefox'


# 获取浏览器地址
# def _getpath(filename):
#     shellcommand = 'whereis %s > %s'%(filename,filename*3)
#     os.system(shellcommand)
#     path=''
#     with open(filename*3) as f:
#         path = f.read().split(' ')[1]
#     os.remove('./'+filename*3)
#     return path

# path = getpath('firefox')

# firefox浏览器
# def _use_firefox_open_url(url):
#     browser_path=_getpath(_name)
#     #这里的‘firefox’只是一个浏览器的代号，可以命名为自己认识的名字，只要浏览器路径正确
#     web.register(_name, web.Mozilla('mozilla'), web.BackgroundBrowser(browser_path))
#     #web.get('firefox').open(url,new=1,autoraise=True)
#     web.get(_name).open_new_tab(url)
#     print ('use_%s_open_url  open url ending ....'%_name)


# def down_load(target_url=_url):
#     try:
#         _use_firefox_open_url(target_url)
#     except Exception as e:
#         traceback.print_exc()
#         pid = os.getpid()
#         os.kill(pid,signal.SIGKILL)
#
# down_load()


# 谷歌浏览器
def use_chrome_open_url(url):
    browser_path = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
    web.register('chrome', None, web.BackgroundBrowser(browser_path))
    web.get('chrome').open_new_tab(url)
    print('use_chrome_open_url  open url ending ....')


def down_load_from(url):
    t = threading.Thread(target=use_chrome_open_url, args=('%s:3000' % url,))
    t.start()
    print('打开浏览器下载')


if __name__ == '__main__':
    down_load_from('127.0.0.1')