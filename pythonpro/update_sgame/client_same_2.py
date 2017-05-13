#!/usr/bin/pyton3
# -*- coding: utf-8 -*-


import hashlib
import os
import shutil
import time
import configparser
import sys
import codecs


starttime = time.time()

# 读取配置文件
abs_path = os.path.join(os.path.dirname(sys.argv[0]), 'test.conf')
print('开始读取配置文件')
cf = configparser.ConfigParser()
cf.readfp(codecs.open(abs_path, "r", "utf-8"))
develop_path = cf.get('updatedir', 'develop_path')
test_path = cf.get('updatedir', 'test_path')
new_version = cf.get('version', 'new_version')
old_version = cf.get('version', 'old_version')
log = cf.get('log', 'log')
print(log)
print('更新来源目录：%s,更新目标目录：%s' % (develop_path, test_path))
print('起始版本号：%s,目标版本号：%s' % (old_version, new_version))

print('开始更新开发服')
os.system('svn update %s' % develop_path)
print('开始更新测试服')
os.system('svn update %s' % test_path)
r1 = os.popen('svn log -l 1 %s' % develop_path)
update_version = r1.readlines()[1].split()[0][1:]
print(update_version)
add_list = []
delete_list = []
mod_list = []

# 获得版本差异
print('开始获得版本差变动文件列表：')
r = os.popen('svn diff -r %s:%s --summarize %s' % (old_version, new_version, develop_path))
text1 = r.readlines()
for line in text1:
    linesplitlist = line.split()
    if linesplitlist[0] == 'A':
        add_list.append(linesplitlist[1].replace('\\', '/'))
    elif linesplitlist[0] == 'D':
        delete_list.append(linesplitlist[1].replace('\\', '/'))
    else:
        mod_list.append(linesplitlist[1].replace('\\', '/'))
print('文件列表获取完成')

# 删除差异项
if len(delete_list) == 0:
    print('没有需要删除的文件')
else:
    print('开始删除差异文件,总共：%d' % len(delete_list))
    for path in delete_list:
        if os.path.exists(path.replace(develop_path, test_path)):
            if os.path.isfile(path.replace(develop_path, test_path)):
                os.remove(path.replace(develop_path, test_path))
            if os.path.isdir(path.replace(develop_path, test_path)):
                os.rmdir(path.replace(develop_path, test_path))

# 拷贝修改项
if len(mod_list) == 0:
    print('没有需要修改的文件')
else:
    print('开始拷贝修改的文件,总共：%d' % len(mod_list))
    for path in mod_list:
        if not os.path.exists(os.path.split(path.replace(develop_path, test_path))[0]):
            os.makedirs(os.path.split(path.replace(develop_path, test_path))[0])
        shutil.copy2(path, path.replace(develop_path, test_path))

# 拷贝新增项
if len(add_list) == 0:
    print('没有需要新增的文件')
else:
    print('开始拷贝新增文件，总共：%d' % len(add_list))
    for path in add_list:
        if not os.path.exists(os.path.split(path.replace(develop_path, test_path))[0]):
            os.makedirs(os.path.split(path.replace(develop_path, test_path))[0])
        if os.path.isfile(path):
            shutil.copy2(path, path.replace(develop_path, test_path))

# 提交修改项
print('准备提交文件')
r = os.popen("svn status %s" % test_path)
text = r.readlines()
for line in text:
    linesplitlist = line.split()
    if linesplitlist[0] == '!':
        os.system('svn delete %s' % linesplitlist[1])
    elif linesplitlist[0] == '?':
        os.system('svn add %s' % linesplitlist[1])
    else:
        pass

os.system('svn commit -m "%s" %s' % (log, test_path))
print('上传成功')
if new_version == 'HEAD':
    print('修改配置')
    cf.set('version', 'old_version', update_version)
else:
    print('修改配置')
    cf.set('version', 'old_version', new_version)
    cf.set('version', 'new_version', 'HEAD')
cf.write(open(abs_path, 'w'))
print("总共花费时间%ds" % (time.time()-starttime))

os.system(exit())

## 计算文件MD5值
# def md5sum(filename):
#     if not os.path.isfile(filename):
#         print("%s不是文件" % filename)
#     myhash = hashlib.md5()
#     f = open(filename, 'rb')
#     while True:
#         b = f.read(8096)
#         if not b:
#             break
#         myhash.update(b)
#     f.close()
#     return myhash.hexdigest()

# # print(md5sum('/Users/runehero/Desktop/test.py'))

# # 输出文件夹中所有文件


# def getfilelist(path):
#     print('开始获取文件列表：%s' % path)
#     file_list = []
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             file_list.append(os.path.join(root, file))
#     print('文件列表生成完成')
#     return file_list

# # print(getfilelist('/Users/runehero/Desktop/xmind'))


# # 生成MD5、文件名字典
# def get_md5dict(path):
#     file_list = getfilelist(path)
#     print('开始生成文件列表MD5值:%s' % path)
#     file_md5 = {}
#     for file in file_list:
#         md5 = md5sum(file)
#         file_md5[md5] = file
#     print('MD5生成完成')
#     return file_md5


# # 输出修改项，删除项
# def update_file(newpath, oldpath):
#     file_list_update = []
#     file_list_remove = []
#     newpath_md5dict = get_md5dict(newpath)
#     oldpath_md5dict = get_md5dict(oldpath)
#     newpath_md5set = set(newpath_md5dict.keys())
#     oldpath_md5set = set(oldpath_md5dict.keys())
#     print("开始获取修改MD5值")
#     update_file_set = newpath_md5set.difference(oldpath_md5dict)
#     print('开始获取删除项MD5值')
#     remove_file_set = oldpath_md5set.difference(newpath_md5dict)
#     for md5 in update_file_set:
#         file_list_update.append(newpath_md5dict[md5])
#     for md5 in remove_file_set:
#         file_list_remove.append(oldpath_md5dict[md5])
#     return file_list_update, file_list_remove

# develop_path = 'E:/sengine/client/trunk/s-game/res'
# test_path = 'E:/sengine/client/trunk/s-game-test/res'
# print('开始更新开发服')
# os.system('svn update %s' % develop_path)
# print('开始更新测试服')
# os.system('svn update %s' % test_path)
# file_list_update, file_list_remove = update_file(develop_path, test_path)
# # print(file_list_update, file_list_remove)

# # 删除已不存在文件
# print('开始删除已被修改项，总共%d条' % len(file_list_remove))
# j = 0
# for file in file_list_remove:
#     if os.path.isfile(file):
#         os.remove(file)
#         j += 1
#         print(j)

# # 拷贝修改项
# print('开始拷贝修改项,总共%d条' % len(file_list_update))
# i = 0
# for file in file_list_update:
#     if os.path.isfile(file):
#         if not os.path.exists(os.path.split(file.replace('s-game', 's-game-test'))[0]):
#             os.makedirs(os.path.split(file.replace('s-game', 's-game-test'))[0])
#         shutil.copy2(file, file.replace('s-game', 's-game-test', 1))
#         i += 1
#         print(i)