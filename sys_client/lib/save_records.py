# !/user/bin/python3
# -*- coding: utf-8 -*-
# Author: Hou Xiao Feng
# Email: 409771377@qq.com

from tkinter import filedialog
from tkinter import messagebox
import os
import datetime

"""
用户选择路径，保存内容
"""


def func(data):
    path = filedialog.askdirectory()                                            # 存储路径选择
    file_name = str(datetime.datetime.now()).split()[0] + '.txt'             # 文件名
    file_path = path + '/' + file_name                                          # 完整路径
    # 判断是否选择路径
    if path != '':
        if os.path.isfile(file_path):                                               # 判断文件是否已存在
            error = messagebox.askyesno('提醒', '文件已存在，是否替换')                # 给出窗口提醒
            if error == True:
                with open(file_path, 'w') as file:
                    file.write(data)
                messagebox.showinfo('提醒', '保存成功！')                             # 保存成功提醒
        else:
            with open(file_path, 'w') as file:
                file.write(data)
                messagebox.showinfo('提醒', '保存成功！')


if __name__ == '__main__':
    func('123')