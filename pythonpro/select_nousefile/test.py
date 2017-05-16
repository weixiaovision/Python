import codecs
import os
import re
import sys
import json
import threading
import math
import time


def select_file(path_tuple, text_tuple):
    file_list = []
    for path in path_tuple:
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] in text_tuple:
                    file_list.append(os.path.join(root, file))
    return file_list


def check(filelist1, filelist2):
    unuse_list = []
    for file1 in filelist1:
        isuse = False
        for file2 in filelist2:
            try:
                fo = codecs.open(file2, 'r', 'utf-8')
                text = fo.read()
            except Exception as e:
                fo = codecs.open(file2, 'r', 'gb2312')
                text = fo.read()
            # print(os.path.split(file1)[1])
            # print(re.search(os.path.split(file1)[1], text))
            if re.search(os.path.split(file1)[1], text):
                isuse = True
                break
            fo.close()
        if not isuse:
            print(file1)
            unuse_list.append(file1)
    return unuse_list
startime = time.time()
filelist1 = select_file(('/Users/runehero/Documents/s-game/s-game/res',), ('.png', '.jpg'))
filelist2 = select_file(('/Users/runehero/Documents/s-game/s-game/res',), ('.lua', '.csd', '.plist', '.json'))

print(len(filelist1))
treads = []
for i in range(1000
               ):
    t = threading.Thread(target=check, args=(('test.png',), filelist2))
    treads.append(t)
for tread in treads:
    tread.start()
for thr in treads:
    if thr.isAlive():
        thr.join()
# check(('test.png',), filelist2)
print(time.time()-startime)

def chunks(arr, m):
    n = int(math.ceil(len(arr) / float(m)))
    return [arr[i:i + n] for i in range(0, len(arr), n)]



# treads = []
# # for i in range(len(filelist)):
# #     t = threading.Thread(target=output, args=(filelist[i],))
# #     treads.append(t)
# # for tread in treads:
# #     tread.start()
# # for thr in treads:
# #     if thr.isAlive():
# #         thr.join()


