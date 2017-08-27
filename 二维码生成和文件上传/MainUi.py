#!/usr/bin/python3
# -*- coding: utf-8 -*-


from tkinter import *
from tkinter.filedialog import askopenfilename
import os
import tkinter.messagebox
import qrcode.image
from PIL import Image
import paramiko
import time
from time import sleep


class MainWindow:
    def __init__(self):
        self.frame = Tk()
        self.frame.title('一键二维码')
        self.frame.geometry('400x300')

        self.path1 = StringVar()
        self.path2 = StringVar()

        self.label1 = Label(self.frame, text='APK目录')
        self.text1 = Entry(self.frame, textvariable=self.path1)
        self.button1 = Button(self.frame, text='选择', command=self.select_file1)

        self.label2 = Label(self.frame, text='LOGO目录')
        self.text2 = Entry(self.frame, textvariable=self.path2)
        self.button2 = Button(self.frame, text='选择', command=self.select_file2)

        self.button3 = Button(self.frame, text='开始', command=self.run)

        self.label1.grid(row=0, column=1)
        self.text1.grid(row=0, column=2)
        self.button1.grid(row=0, column=3)

        self.label2.grid(row=1, column=1)
        self.text2.grid(row=1, column=2)
        self.button2.grid(row=1, column=3)

        self.button3.grid(row=2, column=2)

        self.frame.mainloop()

    # apk路径选择
    def select_file1(self):
        apk_path = askopenfilename()
        if len(apk_path) > 0 and os.path.exists(apk_path):
            self.path1.set(apk_path)

    # 图片路径选择
    def select_file2(self):
        apk_path = askopenfilename()
        if len(apk_path) > 0 and os.path.exists(apk_path):
            self.path2.set(apk_path)

    def run(self):
        self.test_apkpath()
        self.test_picpath()
        self.upload_download(self.path1.get())
        self.erweima(os.path.join('http://10.10.7.106:20001/', os.path.split(self.path1.get())[1]), self.path2.get())
        print(os.path.join('http://10.10.7.106:20001/', os.path.split(self.path1.get())[1]))

    # apk 目录检测
    def test_apkpath(self):
        path = self.path1.get()
        if not os.path.isfile(path):
            tkinter.messagebox.askokcancel('目录选择错误', '请重新输入')
            return
        elif path[-3:] != 'apk':
            tkinter.messagebox.askokcancel('不是apk', '请选择APK文件')
            return
        print('APK目录正确')
        sleep(1)

    # png 目录检测
    def test_picpath(self):
        path = self.path2.get()
        if len(path) == 0:
            self.path2.set(os.getcwd() + '/qiroad.png')
        elif os.path.isfile(path):
            tkinter.messagebox.askokcancel('不存在此文件', '请重新选择')
            return
        elif path[-3:] not in ('png', 'jpg'):
            tkinter.messagebox.askokcancel('不是图片', '请重新选择图片')
            return
        print('图片目录正确')
        sleep(1)

    # 二维码生成
    def erweima(self, apk_path, logo_path):
        print('开始生成二维码')
        img = qrcode.make(apk_path).convert('RGBA')
        icon = Image.open(logo_path)
        img_w, img_h = img.size
        factor = 5
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)

        img.save('./' + os.path.split(apk_path)[1].split('.')[0] + '.png')
        print(os.path.split(apk_path)[1].split('.')[0])
        tkinter.messagebox.showinfo('二维码生成成功', '保存目录为：' + os.getcwd())
        print('二维码生成成功')

    # 进度条
    def progress_bar(self, transferred, toBeTransferred, suffix=''):
        # print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)
        bar_len = 60
        filled_len = int(round(bar_len * transferred / float(toBeTransferred)))
        percents = round(100.0 * transferred / float(toBeTransferred), 1)
        bar = '=' * filled_len + ' ' * (bar_len - filled_len)
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()
        # sleep(5)

    # 开启新的线程
    # def thread_upload_download(self, apk_path):
    #     t = Thread(target=self.upload_download, args=(apk_path,))
    #     print('开启上传线程')
    #     t.start()

    # apk上传
    def upload_download(self, apk_path):
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
        print('开始上传')
        t1 = time.time()
        try:
            sftp.put(apk_path, '/data/s-sdk/bin/' + os.path.split(apk_path)[1], callback=self.progress_bar)
            print('上传完毕')
        except Exception as e:
            print(e)
            print('上传失败')
        finally:
            sftp.close()
        tran.close()
        t2 = time.time()
        print('上传共花费：' + str(t2-t1))


if __name__ == '__main__':
    MainWindow()
