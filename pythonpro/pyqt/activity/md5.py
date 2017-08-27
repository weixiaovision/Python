import os
from hashlib import md5


def generate_file_md5value(fpath):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    m = md5()
    # 需要使用二进制格式读取文件内容
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()

for root, dirs, files in os.walk('.'):
    for file in files:
        if file in ('config.conf', 'customize_gm.xml', 'jumplist.conf', 'server.conf', 'sql.xml.bank', 'update.xml', 'gmtools.exe'):
            print(file + '__' + generate_file_md5value(os.path.join(root, file)))
