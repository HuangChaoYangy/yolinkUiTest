# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 9:34
# @Author  : 黄朝阳
# @FileName: yolink_ws
# @Software: PyCharm

import time
import json
import random
import requests
import multiprocessing
from faker import Faker
from websocket import create_connection
from yolink_web import yoyowebClient

class wsConnect():

    def __init__(self, *kwargs):
        self.fk = Faker('zh_CN')
        self.timestamp = time.time()
        self.milliseconds = round(self.timestamp * 1000)
        # self.token = yoyowebClient().login_client(uname=kwargs[0], password=kwargs[1])
        self.yoyoweb = yoyowebClient()
        self.session = requests.session()
        self.base_url = 'https://yolinkcs.quanyou.com.cn'

    def get_user_chatlist_ID(self, uname, password):
        '''
        查询聊天列表中的会话ID
        :param uname:
        :param password:
        :return:
        '''
        url = self.base_url + '/gw/yoyo-server/chatList'
        token = self.yoyoweb.login_client(uname=uname, password=password)
        head = {"lang": "ZH",
                "accessCode": token,
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Connection": "keep-alive",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/85.0.4183.102 Safari/537.36"}
        param = {}
        rsp = self.session.get(url, headers=head, params=param).json()
        print(rsp['data']['lastUserMsg']['unionId'])
        return rsp['data']['lastUserMsg']['unionId']


    def send_ws_request(self, loop, uname, password, chatType=1, msgType=1):
        '''
        建立连接，发送ws请求
        :param loop: 循环次数
        :param chatType: 会话类型,可用值:0:系统号,1:私聊,2:群聊
        :param msgType: 消息类型,0:系统消息, 1:文本,2:图片,3:文件,4.语音,5.视频,6.实时语音,7.实时视频
        :return:
        '''
        token = self.yoyoweb.login_client(uname=uname, password=password)
        client = "yoyoLink-windows-2.0.0"
        device = "web_device00001"
        self.ws_connect = create_connection(f"wss://yolinkcs.quanyou.com.cn/ws?token={token}&client={client}&device={device}")
        # 获取连接状态
        # print("获取连接状态：", self.ws_connect.getstatus())
        element_list = ['0D87CE938606D874E0656FAF8EF401EA', '0D8BDF413D761337E0656FAF8EF401EA',
                        '0D8859F20683E053E0656FAF8EF401EA']
        random_value = random.choice(element_list)

        if chatType==1:
            from_user_info = yoyowebClient().user_manager(nickName="",employeeNo="QY-00312917",workStatus='')
            from_userId = from_user_info[0]['userId']
            from_nickName = from_user_info[0]['nickName']
            to_user_info = yoyowebClient().user_manager(nickName="",employeeNo="QY-00002809",workStatus='')
            to_userId = to_user_info[0]['userId']
            if from_userId > to_userId:
                unionId = str(to_userId) + 'and' + str(from_userId)
            else:
                unionId = str(from_userId) + 'and' + str(to_userId)
            print(unionId)
            for i in range(loop):
                content = f'编号【{i}】 ' + self.fk.text()
                params = {"cmd":3,"chatType":chatType,"toUser":to_userId,"msgType":msgType,"content":content,"unionId":unionId,"atUser":""}
                self.ws_connect.send(json.dumps(params))
        elif chatType==2:
            for i in range(loop):
                content = f'编号【{i}】 ' + self.fk.text()
                params = {"cmd": 3, "chatType": chatType, "msgType": msgType, "content": content,
                          "unionId": random_value, "atUser": ""}
                self.ws_connect.send(json.dumps(params))
        else:
            raise AssertionError('ERROR,暂不支持该类型')

        # 获取返回结果
        result = self.ws_connect.recv()
        # print("接收结果：", result)

    def close_ws(self):
        # 关闭ws连接
        self.ws_connect.close()

    def multi_send_message(self, kwargs):
        '''
        多进程发送消息
        :param kwargs:
        :return:
        '''
        self.send_ws_request(kwargs[0], kwargs[1], kwargs[2], kwargs[3], kwargs[4])


if __name__ == '__main__':

    ws_object = wsConnect()
    # ws_object.send_ws_request(loop=5,uname='fengjing', password='12345678a.',chatType=2)

    process = [(5, 'fengjing', '12345678a.',2,1), (5, 'caizhaoteng', '12345678a.',2,1)]
    process_num = len(process)
    with multiprocessing.Pool(processes=process_num) as pool:
        pool.map(ws_object.multi_send_message, process)
        pool.close()
        pool.join()
