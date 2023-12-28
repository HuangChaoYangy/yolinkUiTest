# -*- coding: utf-8 -*-
# @Time    : 2023/12/28 11:07
# @Author  : 黄朝阳
# @FileName: yolink_sendMsg
# @Software: PyCharm

import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

from yolink_message import Session


def start_yolink(args):
    k = Session()
    k.send_texta(args[0], args[1], args[2])



if __name__ == '__main__':
    poess = [(10000000, 'fengjing', '12345678a.'),(10000000, 'huangchaoyang3', '12345678a.')]
    # proes = []
    # pp = multiprocessing.Pool(4), (10000000, 'zhaoxiaolong', 'hs1991127'),
    #              (10000000, 'fuguangsong', 'hs1991127'),(10000000, 'qinchuan1', '12345678a')

    # for i in range(4):
    #     print(poess[i][0], poess[i][1], poess[i][2])
    #     time.sleep(6)
    #     se = multiprocessing.Process(target=start_yolink, args=(poess[i][0], poess[i][1], poess[i][2]))
    #     proes.append(se)
    #     se.start()
    # for i in proes:
    #     i.join()
    # pp.apply_async(func=start_yolink, args=(poess[i][0], poess[i][1], poess[i][2]))

    with multiprocessing.Pool(processes=2) as pool:
        pool.map(start_yolink, poess)
    # try:
    #     with multiprocessing.Pool(processes=4) as pool:
    #         pool.map(start_yolink,poess)
    # except:
    #     print('运行出错')

    # finally:
        pool.close()
        pool.join()
