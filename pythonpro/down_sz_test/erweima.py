#!/usr/bin/python3
# -*- coding:utf-8 -*-


import sys
import time


def view_bar(num, total):
  rate = num / total
  rate_num = int(rate * 100)
  r = '\r[%s%s]%d%%' % ("="*num, " "*(100-num), rate_num, )
  sys.stdout.write(r)
  sys.stdout.flush()


# import hashlib
#
# a = "a test string"
# print(hashlib.md5(a).hexdigest())
# print(hashlib.sha1(a).hexdigest())
# print(hashlib.sha224(a).hexdigest())
# print(hashlib.sha256(a).hexdigest())
# print(hashlib.sha384(a).hexdigest())
# print(hashlib.sha512(a).hexdigest()

if __name__ == '__main__':
  for i in range(0, 101):
    time.sleep(0.1)
    view_bar(i, 100)