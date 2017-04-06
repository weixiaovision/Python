coding:gbk

import os, sys, time, re, csv
import log
import util
from uiautomator import Device
import traceback
import log, logging
import multiprocessing

optpath = os.getcwd()  # ��ȡ��ǰ����Ŀ¼
imgpath = os.path.join(optpath, 'img')  # ��ͼĿ¼


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
    # ��ʼ��һ������ļ�
    d.screen.on()
    rstlogger = log.Logger('rst/%s.log' % device, clevel=logging.DEBUG, Flevel=logging.INFO)
    # �Ȱ�װmkiller
    mkillerpath = os.path.join(os.getcwd(), 'MKiller_1001.apk')
    cmd = 'adb -s %s install -r %s' % (device, mkillerpath)
    util.exccmd(cmd)

    def checkcancel(d, sucapp, errapp):
        times = 10
        while (times):
            if d(textContains=u'ȡ����װ').count:
                print
                d(textContains=u'ȡ����װ', className='android.widget.Button').info['text']
                d(textContains=u'ȡ����װ', className='android.widget.Button').click()
                rstlogger.info(device + '���Գɹ����е���ȡ����װ�Ի���')
                break
            else:
                time.sleep(1)
                times -= 1
                if times == 0:
                    rstlogger.error(device + '����ʧ�ܣ�û�е���ȡ����װ�Ի���')

    try:
        d.watcher('allowroot').when(text=u'����').click(text=u'����')
        d.watcher('install').when(text=u'��װ').when(textContains=u'�Ƿ�Ҫ��װ��Ӧ�ó���').click(text=u'��װ',
                                                                                     className='android.widget.Button')  # ר��ΪС�׵����İ�װ����
        d.watcher('cancel').when(text=u'ȡ��').when(textContains=u'��ǿ�����ܹ��������').click(text=u'ȡ��')
        d.watcher('confirm').when(text=u'ȷ��').when(textContains=u'Ӧ�ó������').click(text=u'ȷ��')
        d.watcher('agree').when(text=u'ͬ�Ⲣʹ��').click(text=u'ͬ�Ⲣʹ��')
        d.watcher('weishiuninstall').when(textContains=u'�ݲ�����').click(textContains=u'�ݲ�����')
        # d.watchers.run()
        data = 0
        util.doInThread(runwatch, d, data, t_setDaemon=True)
        # ���������䲢�˳�������
        cmd = 'adb -s %s shell am start com.qihoo.mkiller/com.qihoo.mkiller.ui.index.AppEnterActivity' % device
        util.exccmd(cmd)
        time.sleep(5)
        times = 3
        while (times):
            d.press.back()
            if d(text=u'ȷ��').count:
                d(text=u'ȷ��').click()
                break
            else:
                time.sleep(1)
                times -= 1

        for item in apklist:
            apkpath = item
            if not os.path.exists(apkpath):
                logger.error('%s��Ӧ�ò����ڣ�����' % apkpath)
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
        logger.info('���ҵ�%s���ֻ�' % str(len(devices) - 1))
        for i in deviceIds:
            logger.info('IDΪ%s' % i)
        return deviceIds
    else:
        logger.error('û���ҵ��ֻ�������')
        return

        # needcount:��Ҫ��װ��apk������Ĭ��Ϊ0���Ȱ�����


# deviceids:�ֻ����б�
# apklist:apkӦ�ó�����б�
def doInstall(deviceids, apklist):
    count = len(deviceids)
    port_list = range(5555, 5555 + count)
    for i in range(len(deviceids)):
        d = Device(deviceids[i], port_list[i])
        util.doInThread(installapk, apklist, d, deviceids[i])


# ����Ӧ��
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


# ��Ҫ���ú�adb ��������
# 1.��ȷ���м�̨�ֻ�
# 2.��ȷ���ж��ٸ�Ӧ��
# 3.�Ȱ�װmkiller,����mkiller
# 4.�ٰ�װ���Ե�����
# 5.����Ƿ���ȡ����װ�İ�ť���֣�����˵������ͨ����û����˵������ʧ��


if __name__ == "__main__":
    cleanEnv()
    logger = util.logger
    devicelist = finddevices()
    if devicelist:
        apkpath = os.path.join(os.getcwd(), 'apk')