# -*- coding: utf-8 -*-
# @Time    : 2023/11/14 21:19
# @Author  : 黄朝阳
# @FileName: test
# @Software: PyCharm

list = [{'uname': 18728421687, 'pwd': 12345678}, {'uname': 15178713870, 'pwd': 12345676}, {'uname': 15608078361, 'pwd': 12345676}]
new_list = []
for i in list:
    new_list.append((str(i['uname']),str(i['pwd'])))
print(new_list)
