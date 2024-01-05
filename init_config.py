# -*- coding: utf-8 -*-
# @Time    : 2024/1/4 21:09
# @Author  : 黄朝阳
# @FileName: conftest
# @Software: PyCharm

import os
import sys
import configparser
import logging
from configparser import ConfigParser

# def initalize():
#     #读取配置文件
#     config = configparser.ConfigParser()
#     config.read('config.ini')
#     #设置环境变量
#     os.environ['ENVIRONMENT'] = config.get('general', 'enviroment')
#     #配置日志
#     log_level = config.get('general', 'log_level')
#     logging.basicConfig(level=log_level, format='%(asctime)s - %(leveltime)s - %(message)s')
#     #连接数据库等其它初始化操作


class ReadConfigFile(object):
    def read_config(self):
        conn = ConfigParser()
        file_path = os.path.join(os.path.abspath('.'),'config_test.ini')
        if not os.path.exists(file_path):
            raise FileNotFoundError("文件不存在")

        conn.read(file_path)
        url = conn.get('api','url')
        method = conn.get('api','method')
        header = conn.get('api','header')
        data = conn.get('api','data')
        resp_code = conn.get('api','resp_code')
        resp_json = conn.get('api','resp_code')

        return [url,method,header,data,resp_code,resp_json]


if __name__ == "__main__":
    rc = ReadConfigFile()
    print(rc.read_config())