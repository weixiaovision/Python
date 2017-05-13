#!/usr/bin/python3
# -*- coding:utf-8 -*-


import paramiko
import sys
from time import sleep


transport = paramiko.Transport(('10.10.7.106', 16333))
transport.connect(username='root', password='Qianqi123')

sftp = paramiko.SFTPClient.from_transport(transport)


def progress_bar(transferred, toBeTransferred,  suffix=''):
    # # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
    bar_len = 60
    filled_len = int(round(bar_len * transferred/float(toBeTransferred)))
    percents = round(100.0 * transferred/float(toBeTransferred), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    # sys.stdout.write('%s\%s\r' % (transferred, toBeTransferred))
    sys.stdout.flush()
    sleep(5)
# 上传
try:
    sftp.put('/Users/runehero/Desktop/s-game_out.apk', '/data/s-sdk/bin/s_game_out.apk', callback=progress_bar)
except Exception as e:
    print(e)
finally:
    sftp.close()

transport.close()

# remotepath = '/data/1.txt'
# localpath = '/Users/runehero/Desktop/2.txt'
# # 下载
# sftp.get(remotepath, localpath)

