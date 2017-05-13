#!/usr/bin/python3
# -*- coding:utf-8 -*-


import paramiko
import configparser


# 创建SSH连接对象
ssh = paramiko.SSHClient()
# 允许连接不在know_hosts文件中的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname='10.10.7.106', port=16333, username='root', password='Qianqi123')
# 执行命令
stdin, stdout, stderr = ssh.exec_command('ls /data')
# 获取命令结果
result = str(stdout.read(), encoding='utf-8')
print(result)

# 关闭连接
ssh.close()
