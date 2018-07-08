"""
功能：服务器链接客户端上传文件到服务器

过程：
    １．通过udp协议通知这个模块起作用
    ２．通过传过来的列表判断开启几个线程
    ３．创建n个tcp套接字connect客户端
    ４．链接成功开始下载

需要参数：
    客户端addr　
"""
print('module_up_load_server导入')

# 模块　获取文件路径
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames
import os, sys, traceback, signal
import time, datetime
from socket import *
from multiprocessing import *
from threading import *
import zipfile

'''
获取当前路径
'''
# def where_we_are():
#     return os.getcwd()

'''
获取当前的时间
'''


# 获取当日
def get_today():
    return str(datetime.date.today())


# 获取此时事件
def get_now():
    return time.strftime('%H-%M-%S')


def get_time():
    """年-月-日-十-分-秒"""
    newtime = get_today() + '-' + get_now()
    return newtime


'''
   获取存放文件夹路径
'''


def get_path_of_dir():
    dirname = 'datas/' + get_today() + 'files/'
    folder = os.path.exists(dirname)
    if not folder:
        os.makedirs(dirname)
    return dirname


# print(get_path_of_dir())
# help(os.mkdir)

'''
压缩文件
'''


def zip_dir(filename):
    # filelist = []
    # if os.path.isfile(dirname):
    #     filelist.append(dirname)
    # else :
    #     for root, dirs, files in os.walk(dirname):
    #         for dir in dirs:
    #             filelist.append(os.path.join(root,dir))
    #         for name in files:
    #             filelist.append(os.path.join(root, name))
    #
    # zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    # for tar in filelist:
    #     arcname = tar[len(dirname):]
    #     #print arcname
    #     zf.write(tar,arcname)
    with zipfile.ZipFile(filename + '.zip', mode='w') as zipf:
        zipf.write(filename)

    zipf = zipfile.ZipFile(filename + '.zip')

    # j = zipfile.is_zipfile(filename)
    print('压缩结束')


'''
   相对路径创建文件　　需要参数　filename ,和套接字
'''


def touch_file_write_all(filename, tcpsock):
    # 创建文件的姓名子　例如'2018-05-18-17-29-38pycharm.exe'
    newname = get_time() + filename
    # 得到创建文件的相对路径
    path = get_path_of_dir() + newname
    # 写入文件
    try:
        with open(path, 'wb') as f:
            while True:
                # 直接二进制写入
                datas = tcpsock.recv(100000)
                f.write(datas)
                if not datas:
                    break
            print('写入成功')
    except Exception:
        traceback.print_exc()
        # 如果失败删除下载的不完整文件
        # os.system('rm %s'%path) #linux
        # os.system('WinRAR m -r -ep1 压缩包保存路径 被压缩的文件（夹）路径')
        # tcpsock.close()
        # signal.signal(os.getpid(),signal.SIGKILL)
        return
    # 压缩文件
    # os.system('tar -czvf {0}.tar.gz {0}'.format(path)) #linux
    # os.system('WinRAR m -r -ep1 {}.rar {}'.fomat(path))
    zip_dir(path)
    # 　删除原来文件
    os.remove(path)
    tcpsock.close()
    # signal.signal(os.getpid(),signal.SIGKILL)


'''
　　创建tcp套接字　链接客户端
    需要参数 targetaddr
'''


def create_tcp_sock_to_connect(addr):
    '''
    创建套接字，链接客户端，接受文件名子，回发文件名字
    然后开始写文件
    '''
    print('准备链接', addr)
    sock = socket()
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        # time.sleep(1)
        sock.connect(addr)
        filename = sock.recv(1024).decode()
        print('connect ', filename)
        print(filename)
        if not filename:
            sock.close()
            print('上传失败')
            return
        else:
            sock.send(filename.encode())
            touch_file_write_all(filename, sock)
    except Exception:
        traceback.print_exc()
    finally:
        sock.close()


'''
接受字符串，解析为文件名列表，根据长度开启相应线程
需要参数　文件名的列表字字符串
'''


def exce_request_str_to_list(st):
    names, addr = st.split('@u@')
    # 解析
    filenames_list = eval(names)
    addr = eval(addr)
    print(filenames_list, type(filenames_list))
    # 存放进程列表
    p_list = []
    # 创建进程　并且放入列表
    for i in filenames_list:
        p = Thread(target=create_tcp_sock_to_connect, args=(addr,))
        p.start()
        p_list.append(p)

    for i in p_list:
        i.join()
