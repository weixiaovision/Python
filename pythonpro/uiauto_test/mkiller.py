coding:gbk

import os, sys, time, re, csv
import log
import util
from uiautomator import Device
import traceback
import log, logging
import multiprocessing

optpath = os.getcwd()  # 获取当前操作目录
imgpath = os.path.join(optpath, 'img')  # 截图目录


def cleanEnv():
    os.system('adb kill-server')
    needClean = ['log.log', 'img', 'rst']
    pwd = os.getcwd()
    for i in needClean:
        delpath = os.path.join(pwd, i)
        if os.path.isfile(delpath):
            cmd = 'del /f/s/q "%s"' % delpath
            os.system(cmd)
        elif os.path.isdir(delpath):
            cmd = 'rd /s/q "%s"' % delpath
            os.system(cmd)
    if not os.path.isdir('rst'):
        os.mkdir('rst')


def runwatch(d, data):
    times = 120
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()
        times -= 1
        if times == 0:
            break
        else:
            time.sleep(0.5)


def installapk(apklist, d, device):
    sucapp = []
    errapp = []
    # d = Device(device)
    # 初始化一个结果文件
    d.screen.on()
    rstlogger = log.Logger('rst/%s.log' % device, clevel=logging.DEBUG, Flevel=logging.INFO)
    # 先安装mkiller
    mkillerpath = os.path.join(os.getcwd(), 'MKiller_1001.apk')
    cmd = 'adb -s %s install -r %s' % (device, mkillerpath)
    util.exccmd(cmd)

    def checkcancel(d, sucapp, errapp):
        times = 10
        while (times):
            if d(textContains=u'取消安装').count:
                print
                d(textContains=u'取消安装', className='android.widget.Button').info['text']
                d(textContains=u'取消安装', className='android.widget.Button').click()
                rstlogger.info(device + '测试成功，有弹出取消安装对话框')
                break
            else:
                time.sleep(1)
                times -= 1
                if times == 0:
                    rstlogger.error(device + '测试失败，没有弹出取消安装对话框')

    try:
        d.watcher('allowroot').when(text=u'允许').click(text=u'允许')
        d.watcher('install').when(text=u'安装').when(textContains=u'是否要安装该应用程序').click(text=u'安装',
                                                                                     className='android.widget.Button')  # 专门为小米弹出的安装拦截
        d.watcher('cancel').when(text=u'取消').when(textContains=u'超强防护能够极大提高').click(text=u'取消')
        d.watcher('confirm').when(text=u'确认').when(textContains=u'应用程序许可').click(text=u'确认')
        d.watcher('agree').when(text=u'同意并使用').click(text=u'同意并使用')
        d.watcher('weishiuninstall').when(textContains=u'暂不处理').click(textContains=u'暂不处理')
        # d.watchers.run()
        data = 0
        util.doInThread(runwatch, d, data, t_setDaemon=True)
        # 启动急救箱并退出急救箱
        cmd = 'adb -s %s shell am start com.qihoo.mkiller/com.qihoo.mkiller.ui.index.AppEnterActivity' % device
        util.exccmd(cmd)
        time.sleep(5)
        times = 3
        while (times):
            d.press.back()
            if d(text=u'确认').count:
                d(text=u'确认').click()
                break
            else:
                time.sleep(1)
                times -= 1

        for item in apklist:
            apkpath = item
            if not os.path.exists(apkpath):
                logger.error('%s的应用不存在，请检查' % apkpath)
                continue
            if not device:
                cmd = 'adb install -r "%s"' % apkpath
            else:
                cmd = 'adb -s %s install -r "%s"' % (device, apkpath)
            util.doInThread(checkcancel, d, sucapp, errapp)
            rst = util.exccmd(cmd)
    except Exception, e:
        logger.error(traceback.format_exc())
        data = 1
    data = 1
    return sucapp


def finddevices():
    rst = util.exccmd('adb devices')
    devices = re.findall(r'(.*?)\s+device', rst)
    if len(devices) > 1:
        deviceIds = devices[1:]
        logger.info('共找到%s个手机' % str(len(devices) - 1))
        for i in deviceIds:
            logger.info('ID为%s' % i)
        return deviceIds
    else:
        logger.error('没有找到手机，请检查')
        return

        # needcount:需要安装的apk数量，默认为0，既安所有


# deviceids:手机的列表
# apklist:apk应用程序的列表
def doInstall(deviceids, apklist):
    count = len(deviceids)
    port_list = range(5555, 5555 + count)
    for i in range(len(deviceids)):
        d = Device(deviceids[i], port_list[i])
        util.doInThread(installapk, apklist, d, deviceids[i])


# 结束应用
def uninstall(deviceid, packname, timeout=20):
    cmd = 'adb -s %s uninstall %s' % (deviceid, packname)
    ft = util.doInThread(os.system, cmd, t_setDaemon=True)
    while True:
        if ft.isFinished():
            return True
        else:
            time.sleep(1)
            timeout -= 1
            if timeout == 0:
                return False


# 需要配置好adb 环境变量
# 1.先确定有几台手机
# 2.再确定有多少个应用
# 3.先安装mkiller,启动mkiller
# 4.再安装测试的样本
# 5.检查是否有取消安装的按钮出现，出现说明测试通过，没出现说明测试失败


if __name__ == "__main__":
    cleanEnv()
    logger = util.logger
    devicelist = finddevices()
    if devicelist:
        apkpath = os.path.join(os.getcwd(), 'apk')