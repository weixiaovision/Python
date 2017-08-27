#!/usr/bin/python3
# -*- coding: utf-8 -*-


import os
import paramiko
import xml.etree.ElementTree as ET
import sys
from hashlib import md5


def progress_bar(transferred, toBeTransferred, suffix=''):
    # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    bar_len = 60
    filled_len = int(round(bar_len * transferred / float(toBeTransferred)))
    percents = round(100.0 * transferred / float(toBeTransferred), 1)
    bar = '=' * filled_len + ' ' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


def generate_file_md5value(fpath):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    m = md5()
    # 需要使用二进制格式读取文件内容
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()


def upload_download(remotename, localname):
    tran = paramiko.Transport(('10.10.7.106', 16333))
    try:
        print('开始连接服务器')
        tran.connect(username='root', password='Qianqi123')
    except Exception as e:
        print('连接服务器失败')
        print(e)
        return
    else:
        print('成功连接服务器')
    sftp = paramiko.SFTPClient.from_transport(tran)
    print('开始下载')
    try:
        sftp.get(os.path.join('/data/s-sdk/bin/gmtools/', remotename), localname)
        print('下载完毕:', remotename)
    except Exception as e:
        print(e)
        print('下载失败:', remotename)
    finally:
        if sftp:
            sftp.close()
        tran.close()


def download_exe(file):
    name = file.split('_')[0]
    oldmd5 = file.split('_')[1]
    if oldmd5 != generate_file_md5value(os.path.join('.', name)):
        upload_download(file, name)
        sys.exit()


def download_main():
    if os.path.exists('update.xml'):
        root = ET.parse('update.xml').getroot()
        for child in root[0]:
            # 判断自动更新是否开启
            if child.text:
                upload_download('update.xml', 'update.xml')
                upload_download('update.md', 'update.md')
                # 读取新值
                root = ET.parse('update.xml').getroot()
                # 本地如果存在配置文件不会更新，想更新配置文件可以删除旧的
                for child in root[1]:
                    if not os.path.exists(os.path.join('.', child.text)):
                        upload_download(child.text, child.text)
                for child in root[2]:
                    download_exe(child.text)
    else:
        upload_download('update.xml', 'update.xml')
        upload_download('update.md', 'update.md')
        root = ET.parse('update.xml').getroot()
        for child in root[0]:
            if child.text:
                upload_download('update.xml', 'update.xml')
                for child in root[1]:
                    if not os.path.exists(os.path.join('.', child.text)):
                        upload_download(child.text, child.text)
                for child in root[2]:
                    download_exe(child.text)

if __name__ == '__main__':
    upload_download('gmtools.py_a9cf20b596b959dad8253861db589440', 'gmtools.py')
