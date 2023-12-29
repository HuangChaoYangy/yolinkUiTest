# -*- coding: utf-8 -*-
# @Time    : 2023/12/29 11:38
# @Author  : 黄朝阳
# @FileName: yolink_web
# @Software: PyCharm

import requests
import time


class yoyowebClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self,):
        self.url = 'https://yolinkcs.quanyou.com.cn'
        self.session = requests.session()

    def bf_request(self, method, url, head=None, data=None, *args, **kwargs):
        '''
        请求方法
        :param method:
        :param url:
        :param head:
        :param data:
        :param args:
        :param kwargs:
        :return:
        '''
        method = method.lower()
        if method == 'get':
            for loop in range(1,4):
                try:
                    b_request = requests.get(url=url, headers=head, params=data, timeout=600)
                    if b_request.status_code != 200:
                        raise AssertionError(f'请求超时:{loop}次,{b_request.json()}')
                    else:
                        return b_request
                except ConnectionError:
                    time.sleep(2)
                    continue
                except Exception as e:
                    raise AssertionError(f'当前接口接口调用失败，请求检查接口,失败信息：{e}')

        elif method == 'post':
            for loop in range(1,4):
                try:
                    b_request = requests.post(url=url, headers=head, json=data, timeout=600)
                    if b_request.status_code != 200:
                        raise AssertionError(f'请求超时:{loop}次,{b_request.json()}')
                    else:
                        return b_request
                except ConnectionError:
                    time.sleep(2)
                    continue
                except Exception as e:
                    raise AssertionError(f'当前接口接口调用失败，请求检查接口,失败信息：{e}')

    def login_client(self, uname='huangchaoyang3', password='12345678a.', appcode='im-web-api', *args, **kwargs):
        '''
        登录web客户端
        :param uname:
        :param password:
        :param appcode:
        :param args:
        :param kwargs:
        :return:
        '''
        url = self.url + '/gw/qu-platform-auth-api/auth/tokenWithAD'
        head = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "78",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        data = {"userName": uname, "password": password, "appCode": appcode}
        for loop in range(4):
            try:
                rsp = self.session.post(url, headers=head, json=data).json()
                if rsp['message'] == '域账号或密码错误！':
                    print("登录失败,原因：" + rsp['message'])
                elif rsp['message'] != "success":
                    raise AssertionError("登录失败,原因：" + rsp["message"])
                else:
                    self.Authorization = rsp['data']['token']
                    return self.Authorization

            except ConnectionError:
                time.sleep(2)
                continue

    def login_background(self, uname, password, appcode, *args, **kwargs):
        '''
        登录后台
        :param uname:
        :param password:
        :param appcode:
        :param args:
        :param kwargs:
        :return:
        '''
        url = self.url + '/gw/qu-platform-auth-api/auth/tokenWithAD'
        head = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "78",
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        data = {"userName": uname, "password": password, "appCode": appcode}
        for loop in range(4):
            try:
                rsp = self.session.post(url, headers=head, json=data).json()
                if rsp['message'] == '域账号或密码错误！':
                    print("登录失败,原因：" + rsp['message'])
                elif rsp['message'] != "success":
                    raise AssertionError("登录失败,原因：" + rsp["message"])
                else:
                    self.Authorization = rsp['data']['token']
                    return self.Authorization

            except ConnectionError:
                time.sleep(2)
                continue

    def user_manager(self, nickName="",employeeNo="",workStatus='',orgId=1, pageNum=1, pageSize=30, *args, **kwargs):
        '''
        人员管理查询
        :param nickName:
        :param employeeNo:
        :param workStatus:
        :param orgId:
        :param pageNum:
        :param pageSize:
        :param args:
        :param kwargs:
        :return:
        '''
        token = self.login_background(uname='huangchaoyang3', password='12345678a.', appcode='yoyo-manager')
        url = self.url + '/gw/yoyo-manager/user/pageList'
        head = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Content-Length": "78",
            "Authorization": token,
            "Content-Type": "application/json;charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}
        data = {"pageNum":pageNum,"pageSize":pageSize,"workStatus":workStatus,
                "orgId":orgId,"nickName":nickName,"employeeNo":employeeNo}
        rsp = self.session.post(url, headers=head, json=data).json()
        # print(rsp)
        if rsp['message'] != 'success':
            raise AssertionError("接口查询失败,原因：" + rsp["message"])
        elif rsp['data']['list'] == []:
            print('查询接口为空')
        else:
            user_list = rsp['data']['list']
            # print(user_list)
            user_info = []
            for userInfo in user_list:
                if 'workJobs' not in userInfo:
                    workJobs = ""
                else:
                    workJobs = userInfo['workJobs']
                imOrgId = userInfo['imOrgId']
                user_info.append({'userId':userInfo['userId'],'nickName':userInfo['nickName'],'employeeNo':userInfo['employeeNo'],'orgPath':userInfo['orgPath'],'workJobs':workJobs,
                                  'workStatus':userInfo['workStatus'],'disabled':userInfo['employeeNo'],'isOpenVideo':userInfo['employeeNo'],'isOpenVoice':userInfo['isOpenVoice'],
                                  'maxTime':userInfo['maxTime'],'usedTime':userInfo['usedTime'],'fullPathList':userInfo['fullPathList']})
            return user_info



if __name__ == "__main__":

    yoyo = yoyowebClient()            # 创建对象
    # token= yoyo.login_client(uname='huangchaoyang3', password='12345678a.', appcode='im-web-api')
    # token = yoyo.login_background(uname='huangchaoyang3', password='12345678a.', appcode='yoyo-manager')
    user= yoyo.user_manager(nickName="",employeeNo="QY-00002809",workStatus='')
    print(user)