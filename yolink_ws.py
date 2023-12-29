# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 9:34
# @Author  : 黄朝阳
# @FileName: yolink_ws
# @Software: PyCharm

import time
import json
from faker import Faker
from websocket import create_connection
from yolink_web import yoyowebClient

class wsConnect:

    def __init__(self):
        self.fk = Faker('zh_CN')
        self.timestamp = time.time()
        self.milliseconds = round(self.timestamp * 1000)
        self.token = yoyowebClient().login_client()

    def send_ws_request(self, loop, chatType=1, msgType=1):
        '''
        建立连接，发送ws请求
        :param loop: 循环次数
        :param chatType: 会话类型,可用值:0:系统号,1:私聊,2:群聊
        :param msgType: 消息类型,0:系统消息, 1:文本,2:图片,3:文件,4.语音,5.视频,6.实时语音,7.实时视频
        :return:
        '''
        token =self.token
        client = "yoyoLink-windows-2.0.0"
        device = "web_device00001"
        self.ws_connect = create_connection(f"wss://yolinkcs.quanyou.com.cn/ws?token={token}&client={client}&device={device}")
        # 获取连接状态
        # print("获取连接状态：", self.ws_connect.getstatus())

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

        # 获取返回结果
        result = self.ws_connect.recv()
        # print("接收结果：", result)

    def close_ws(self):
        # 关闭ws连接
        self.ws_connect.close()


if __name__ == '__main__':

    ws_object = wsConnect()
    ws_object.send_ws_request(loop=10)