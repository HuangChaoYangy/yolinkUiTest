# -*- coding: utf-8 -*-
# @Time    : 2024/1/5 13:31
# @Author  : 黄朝阳
# @FileName: CommonFunc
# @Software: PyCharm

import datetime
import arrow
import calendar
import time
import requests
import base64
# from tzlocal import get_localzone
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.schedulers.background import BackgroundScheduler
# fropandasm Crypto.PublicKey import RSA
import hashlib
import xlsxwriter as xw
import pandas as pd
import openpyxl as op
from itertools import combinations
from functools import reduce
from operator import itemgetter
from itertools import groupby
from common.yamlControl import Yaml_data
from base_dir import *

# try:
#     from Decorators import add_doc
# except Exception:
#     from .Decorators import add_doc


class CommonFunc(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, *args, **kwargs):
        self.pub_key = "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL1XuLmIZttk13hmAGVuXiKSfQggfVck" \
                       "p+iNr9jBIxkmBBfmygJ9D5A7lhUbhBEY1SqyGNIHI1DsNLfxfRvW2EcCAwEAAQ==\n-----END PUBLIC KEY-----"

    # def rsa_encrypt(self, data):
    #     '''
    #     RSA加密（encrypt）
    #     :param data:
    #     :return:
    #     '''
    #     msg = data.encode('utf-8')
    #     rsa_key = RSA.importKey(self.pub_key)
    #     cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    #     cipher_text = base64.b64encode(cipher.encrypt(msg)).decode("utf-8")
    #     return cipher_text

    def get_md5(self, data):
        '''
        md5加密
        :param data:
        :return:
        '''
        # 创建md5对象
        md5 = hashlib.md5()
        # 调用加密方法直接直接加密,此处必须声明encode,否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
        md5.update(data.encode(encoding='utf-8'))

        return md5.hexdigest()

    def base64_encode(self, agrs):
        '''
        # base64加密
        : param agrs:
        '''
        agrs = str(agrs).encode("utf-8")
        # base64加密
        base64_value = base64.b64encode(agrs).decode(encoding="utf-8")
        return base64_value

    def get_random_num(self, length):
        '''
        #随机数
        : param length:
        '''
        return str(int(time.time()))[:length]


    def get_md_search_time(self, diff=0):
        """
        对应客户端的今日早盘滚球的搜索，获取美东的一天对应的UTC的开始和结束时间
        :param diff:
        :return:start_time, end_time
        """
        now_date = self.get_md_date_by_now(diff=diff)
        next_date = self.get_md_date_by_now(diff=diff + 1)
        start_date_list = now_date.split("-")
        end_date_list = next_date.split("-")
        start_time = datetime.datetime(int(start_date_list[0]), int(start_date_list[1]),
                                       int(start_date_list[2]), 4, 00, 00)
        end_time = datetime.datetime(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]), 4, 00, 00)
        return start_time, end_time

    def get_month_day_num(self, diff=0):
        now = self.get_current_time("shanghai")
        now = now.shift(days=int(diff))
        days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
        return days

    def get_md_month_day_num(self, diff=0):
        now = self.get_current_time("shanghai")
        diff = self.get_md_diff_unit(diff)
        now = now.shift(days=int(diff))
        days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
        return days

    def get_md_diff_unit(self, diff_unit=0):
        """
        获取美东日期偏移值
        :return:
        """
        now = self.get_current_time("shanghai")
        now_time = now.strftime("%H")
        if int(now_time) < 12:
            diff_unit -= 1
        return diff_unit

    @staticmethod
    def get_relative_time(day='0', hour='0', minute='0', second='0', now=""):
        """
        获取相对日期
        :param now: 指定时间则以指定的时间为准，否则以当前时间
        :param day: 之后传正值，之前传负值
        :param hour: 之后传正值，之前传负值
        :param minute: 之后传正值，之前传负值
        :param second: 之后传正值，之前传负值
        :return:
        """
        now = now if now else datetime.datetime.now()
        now = now + datetime.timedelta(days=float(day), hours=float(hour), minutes=float(minute), seconds=float(second))
        return now.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_current_time(timezone="utc"):
        """
        根据时区返回当前时间
        :param timezone: (default)shanghai|UTC
        :return:
        """
        if timezone == "utc":
            now = arrow.utcnow()
        else:
            now = arrow.now("Asia/Shanghai")
        return now

    def get_date_by_now(self, date_type="日", diff=-1, timezone="utc"):
        """
        获取当前日期前的时间，不包含小时分钟秒
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :param timezone: shanghai|UTC(default)
        :return:
        """
        now = self.get_current_time(timezone)
        if date_type in ("日", "今日"):
            return now.shift(days=int(diff)).strftime("%Y-%m-%d")
        elif date_type in ("月", "本月"):
            return now.shift(days=int(diff)).strftime("%Y-%m")
        elif date_type == "年":
            return now.shift(days=int(diff)).strftime("%Y")
        else:
            raise AssertionError("类型只能为年月日，实际传参为： %s" % date_type)

    def get_md_date_by_now(self, date_type="日", diff=0):
        """
        获取美东时区的当前日期前的时间，不包含小时分钟秒
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :return:
        """
        diff = self.get_md_diff_unit(int(diff))
        return self.get_date_by_now(date_type, int(diff), "shanghai")

    @staticmethod
    def get_current_time_for_client(time_type="now", day_diff=0):
        now = arrow.now().shift(days=+day_diff)               # 当日 + -
        now_week = arrow.now().shift(weeks=+day_diff)         # 当周 + -
        now_month = arrow.now().shift(months=+day_diff)       # 当月 + -
        now_year = arrow.now().shift(years=+day_diff)         # 当年 + -
        if time_type == "now":
            return now.strftime("%Y-%m-%dT%H:%M:%S+07:00")
        elif time_type == "begin":
            return now.strftime("%Y-%m-%dT00:00:00+07:00")
        elif time_type == "end":
            return now.strftime("%Y-%m-%dT23:59:59+07:00")
        elif time_type == "start_time":
            return now.strftime("%Y-%m-%d 00:00:00")
        elif time_type == "end_time":
            return now.strftime("%Y-%m-%d 23:59:59")
        elif time_type == "ctime":
            return now.strftime("%Y-%m-%d")
        elif time_type == "currenttime":
            return now.strftime("%Y-%m-%d %H:%M:%S")
        elif time_type == "now_month_start":      # 当月第一天
            year = now.year
            month = now.month
            now_month_start = datetime.date(year, month, 1).strftime("%Y-%m-%d")
            return now_month_start
        elif time_type == "now_month_end":        # 当月最后一天
            year = now.year
            month = now.month
            last_day = calendar.monthrange(year, month)[1]
            now_month_end = datetime.date(year, month, last_day).strftime("%Y-%m-%d")
            return now_month_end
        elif time_type == "now_month_day":        # 根据day_diff指定查询当月某一天
            year = now.year
            month = now.month
            nnow_month_day = datetime.date(year, month, day=day_diff).strftime("%Y-%m-%d")
            return nnow_month_day
        elif time_type == "month_day":        # Python获取指定月份的所有天数
            today =datetime.datetime.today()
            monthRange = calendar.monthrange(today.year, today.month)[1]
            return monthRange
        elif time_type == "month_days":        # Python获取指定月份的所有日期
            today =datetime.datetime.today()
            year = now.year
            month = now.month
            monthRange = range(calendar.monthrange(year, month)[1]+1)[1:]
            return monthRange
        elif time_type == "week":
            return now_week.strftime("%Y-%m-%d")
        elif time_type == "month":
            return now_month.strftime("%Y-%m")
        elif time_type == "year":
            return now_year.strftime("%Y")
        else:
            raise AssertionError("【ERR】传参错误")

    def getMonthFirstDayAndLastDay(self, year=None, month=None):
        if year:
            year = int(year)
        else:
            year = datetime.date.today().year

    def get_day_range(self, date_type="月", diff=0, timezone="UTC"):
        """
        获取年、月的起始和结束日期，不含小时分钟秒
        :param date_type: 年|月|周，默认为月
        :param diff:之后传正值，之前传负值
        :param timezone: (default)shanghai|UTC
        :return: 该月起始及最后一天
        """
        now = self.get_current_time(timezone)
        new_date = now.shift(days=int(diff))
        if date_type == "月":
            month = new_date.month
            year = new_date.year
            max_day = calendar.monthlen(year, month)
            start = new_date.replace(day=1).strftime("%Y-%m-%d")
            end = new_date.replace(day=max_day).strftime("%Y-%m-%d")
        elif date_type == "周":
            start = new_date - datetime.timedelta(days=new_date.weekday())
            start = start.strftime("%Y-%m-%d")
            end = new_date + datetime.timedelta(days=6 - new_date.weekday())
            end = end.strftime("%Y-%m-%d")
        elif date_type == "年":
            year = new_date.year
            start = new_date.replace(year=year, month=1, day=1).strftime("%Y-%m-%d")
            end = new_date.replace(year=year, month=12, day=31).strftime("%Y-%m-%d")
        else:
            raise AssertionError("类型只能为年月，实际传参为： %s" % date_type)
        return start, end

    def get_md_day_range(self, date_type="月", diff=-1, timezone="US/Eastern"):
        """
        获取美东时区的年、月的起始和结束日期，不含小时分钟秒
        :param date_type: 年|月|周，默认为月
        :param diff:之后传正值，之前传负值
        :param timezone: (default)US/Eastern|UTC
        :return: 该月起始及最后一天
        """
        diff = self.get_md_diff_unit(diff)
        now = self.get_current_time(timezone)
        new_date = now.shift(days=int(diff))
        if date_type == "月":
            month = new_date.month
            year = new_date.year
            max_day = calendar.monthlen(year, month)
            start = new_date.replace(day=1).strftime("%Y-%m-%d")
            end = new_date.replace(day=max_day).strftime("%Y-%m-%d")
        elif date_type == "周":
            start = new_date - datetime.timedelta(days=new_date.weekday())
            start = start.strftime("%Y-%m-%d")
            end = new_date + datetime.timedelta(days=6 - new_date.weekday())
            end = end.strftime("%Y-%m-%d")
        elif date_type == "年":
            year = new_date.year
            start = new_date.replace(year=year, month=1, day=1).strftime("%Y-%m-%d")
            end = new_date.replace(year=year, month=12, day=31).strftime("%Y-%m-%d")
        else:
            raise AssertionError("类型只能为年月，实际传参为： %s" % date_type)
        return start, end

    # @staticmethod
    # def get_time_area():
    #     data = get_localzone()
    #     if "Asia/Bangkok" in data:
    #         return 1
    #     else:
    #         return 2

    @staticmethod
    def convert_to_percent(number):
        return int(number * 10000) / 100

    @staticmethod
    def two_list_should_be_equal(data1, data2, if_sort="是"):
        """
        断言两个列表值相同,abandon
        :param data1:
        :param data2:
        :param if_sort: 是否对列表中的元素进行排序:   是|否，默认为是
        :return:
        """
        data1 = list(data1)
        data2 = list(data2)
        # print("=====================")
        # print(data1)
        # print(data2)
        if len(data1) != len(data2):
            raise AssertionError("两个列表长度不一致！")
        if if_sort == "是":
            data1.sort()
            data2.sort()
        for i in range(len(data1)):
            item_1 = data1[i] if data1[i] else 0
            item_2 = data2[i] if data2[i] else 0
            if item_1 == item_2:
                continue
            if (type(item_1) in (float, int)) or (type(item_2) in (int, float)):
                item_1 = float(round(float(item_1), 3))
                item_2 = float(round(float(item_2), 3))
            if item_1 != item_2:
                try:
                    if float(item_1) == float(item_2):
                        pass
                    else:
                        raise AssertionError(f"两个列表数据不一致！第{i}项,分别为{data1[i]}和{data2[i]}")
                except ValueError:
                    try:
                        if float(item_1) != float(item_2):
                            pass
                    except ValueError:
                        raise AssertionError(f"两个列表数据不一致！第{i}项,分别为{data1[i]}和{data2[i]}")

    @staticmethod
    def convert_none_to_zero_in_list(list_obj):
        list_obj = list(list_obj)
        for index, item in enumerate(list_obj):
            if not item:
                list_obj[index] = 0
        return list_obj

    @staticmethod
    def str_to_timestamp(time_str):
        """
        将字符串转为时间戳
        :param time_str:
        :return:
        """
        return int(time.mktime(time.strptime(time_str, "%Y/%m/%d %H:%M:%S"))) * 1000

    def get_timestamp(self, day='0', hour='0', minute='0', second='0', now=""):
        """
        获取距当前多久时间的时间戳
        :param day:
        :param hour:
        :param minute:
        :param second:
        :param now:
        :return:
        """
        return self.str_to_timestamp(self.get_relative_time(day, hour, minute, second, now))


    def list_data_should_be_equal(self, data_list_1, data_list_2):
        """
        列表数据校验
        :param data_list_1:
        :param data_list_2:
        :return:
        """
        assert len(data_list_1) == len(data_list_2), f"两列表长度不一致: {len(data_list_1)} : {len(data_list_2)}"

        for index in range(len(data_list_1)):
            data_1 = data_list_1[index]
            data_2 = data_list_2[index]
            if not data_1:
                data_1 = 0
            if not data_2:
                data_2 = 0
            if type(data_list_1[index]) in (list,tuple):
                self.list_data_should_be_equal(data_1, data_2)
            else:
                if (type(data_1) not in (int, float) or type(data_1) not in (int, float)) \
                        and not data_1:
                    if data_2:
                        raise AssertionError("数据不一致,第%d-%d项，后台为：%s, 数据库为：%s"
                                             % (index, index, data_1, data_2))
                elif (type(data_1) in (int, float)) or (type(data_2) in (int, float)):
                    data_1 = float(data_1)
                    data_2 = float(data_2) if data_2 else 0
                    if data_1 == data_2:
                        continue
                    else:
                        if float(data_2) not in ((int(data_1 * 100) + 1) / 100, (int(data_1 * 100) - 1) / 100,
                                                 int(data_1 * 100) / 100, (int(data_1 * 100) + 2) / 100,
                                                 (int(data_1 * 100) - 2) / 100):
                            raise AssertionError(f"数据不一致,第{index}项，data1为：{data_1}, data2为：{data_2}")
                elif type(data_1) == str:
                    data_1 = data_1.upper().strip()
                    data_2 = data_2.upper().strip()
                    assert data_1 == data_2, f"数据不一致,第{index}项，data1为：{data_1}, data2为：{data_2}"

    def check_live_bet_report_new(self, int_data, sql_data, com_index=0):
        """
        双层列表,指定索引进行关联
        :param int_data:
        :param sql_data:
        :param com_index: 以第几项作为关联项
        :return:
        """
        int_data = list(int_data)
        # print(int_data)
        sql_data = list(sql_data)
        # print(sql_data)
        assert len(int_data) == len(sql_data), f"接口查询的结果与数据库查询长度不一致!接口为{len(int_data)},sql为{len(sql_data)}"
        if int_data == sql_data:
            return
        for index in range(len(int_data) - 1, -1, -1):
            for item in sql_data:
                temp_data1 = 0 if not item[com_index] else item[com_index]
                temp_data2 = 0 if not int_data[index][com_index] else int_data[index][com_index]
                if temp_data1 == temp_data2:
                    self.two_list_should_be_equal(int_data[index], item, "否")
                    break
            else:
                raise AssertionError(f"数据未找到:{int_data[index]}")


    def write_to_local_file(self, content, file_name, mode='w'):
        '''
        写入txt文件
        :param content:
        :param file_name:
        :param mode: w模式打开文件，如果而文件中有数据，再次写入内容，会把原来的覆盖掉  a向文件追加   a+可读可追加
        :param file_type:
        :return:
        '''
        txt_file = open(f'{file_name}', mode=mode)
        txt_file.write(f'{content}')
        txt_file.close()

        return txt_file

    def xw_toExcel(self, data, filename):
        '''
        xlsxwriter库储存数据到excel,不支持读取、修改、XLS文件、透视表（Pivot Table）
        :param data:
        :param filename:
        :return:
        '''
        workbook = xw.Workbook(filename)         # 创建工作簿
        worksheet1 = workbook.add_worksheet("sheet1")   # 创建子表
        worksheet1.activate()         # 激活表
        title = ['序号', '酒店', '价格']   # 设置表头
        worksheet1.write_row('A1', title)   # 从A1单元格开始写入表头
        i = 2
        for j in range(len(data)):
            insertData = [data[j]["id"], data[j]["name"], data[j]["price"]]
            row = 'A' + str(i)
            worksheet1.write_row(row, insertData)
            i += 1
        workbook.close()   # 关闭表

        return worksheet1

    def pd_toExcel(self, data, filename):
        '''
        pandas库储存数据到excel
        :param data:
        :param filename:
        :return:
        '''
        ids = []
        names = []
        prices = []
        for i in range(len(data)):
            ids.append(data[i]["id"])
            names.append(data[i]["name"])
            prices.append(data[i]["price"])

        dfData = {'序号': ids, '酒店': names, '价格': prices}     # 字典设置DataFrame所需数据
        df = pd.DataFrame(dfData)      # 创建DataFrame
        df.to_excel(filename, index=False)   # 存表,去除原始索引列（0,1,2...）

        return df

    def op_toExcel(self, data, filename):
        '''
        openpyxl库储存数据到excel
        :param data:
        :param filename:
        :return:
        '''
        wb = op.Workbook()       # 创建工作簿对象
        ws = wb['sheet']         # 创建子表
        ws.append(['序号','酒店','价格'])      # 添加表头
        for i in range(len(data[0])):
            d = data[i]["id"], data[i]["name"], data[i]["price"]
            ws.append(d)   # 每次写入一行
        wb.save(filename)

        return wb

    def get_cut_float_length(self, value, length):
        '''
        浮点数截取两位小数
        :param value:
        :param n:
        :return:
        '''
        str_num = str(value)
        a,b,c = str_num.partition('.')
        c = (c+'0'*length)[:length]

        return ".".join([a,c])

    def job(self, text):
        t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print('{} --- {}'.format(text, t))

    def timer_APScheduler(self,function, trigger='date',stime='', etime='',args=[], scheduler_type='Blocking', **kwargs):
        '''
        创建一个定时任务：http://www.cppcns.com/jiaoben/python/273434.html
        :param trigger:  date:特定的时间点触发，只执行一次       interval：固定时间间隔触发       触发器cron：在特定时间周期性地触发
        :param stime:
        :param etime:
        :param args:
        :param scheduler_type: BlockingScheduler: 调用start函数后会阻塞当前线程        BackgroundScheduler: 调用start后主线程不会阻塞
        :return:
        使用APScheduler机制时，向job传递参数的代码示例
        scheduler.add_job(job1, 'interval', seconds=20,args=['para1','para2','para3'])
        scheduler.add_job(job2, 'interval', seconds=20,kwargs={'para1':'3','para2':'2','para3':'1'})
        '''
        scheduler = BlockingScheduler()
        backscheduler = BackgroundScheduler()
        if scheduler_type == 'Blocking':
            if trigger=='date':
                if stime:
                    time = f'{stime}'
                    scheduler.add_job(func=function, trigger=f'{trigger}', run_date=time, args=args)
                    try:
                        scheduler.start()
                    except (KeyboardInterrupt, SystemExit):
                        scheduler.shutdown(wait=False)
                        print('Errors!')
            elif trigger=='interval':
                if stime:
                    start_time = stime
                    end_time = etime
                else:
                    raise AssertionError('ERROR,时间参数不能为空')
                scheduler.add_job(func=function, trigger=f'{trigger}', minutes=30, start_date=start_time,
                          end_date=end_time, args=args)
                try:
                    scheduler.start()
                except (KeyboardInterrupt, SystemExit):
                    scheduler.shutdown(wait=False)
                    print('Errors!')
            elif trigger=='cron':
                if stime:
                    start_time = stime
                    end_time = etime
                else:
                    raise AssertionError('ERROR,时间参数不能为空')
                scheduler.add_job(func=function, trigger=f'{trigger}', start_date=start_time,
                          end_date=end_time, args=args)
                scheduler.start()
                try:
                    scheduler.start()
                except (KeyboardInterrupt, SystemExit):
                    scheduler.shutdown(wait=False)
                    print('Errors!')
            else:
                raise AssertionError('ERROR,暂无支持该参数')

        elif scheduler_type == 'Background':
            if trigger=='date':
                if stime:
                    time = f'{stime}'
                    backscheduler.add_job(func=function, trigger=f'{trigger}', run_date=time, args=args)
                    try:
                        backscheduler.start()
                    except (KeyboardInterrupt, SystemExit):
                        backscheduler.shutdown(wait=False)
                        print('Errors!')
            elif trigger=='interval':
                if stime:
                    start_time = stime
                    end_time = etime
                else:
                    raise AssertionError('ERROR,时间参数不能为空')
                backscheduler.add_job(func=function, trigger=f'{trigger}', seconds=10, start_date=start_time,
                          end_date=end_time, args=args)
                try:
                    backscheduler.start()
                except (KeyboardInterrupt, SystemExit):
                    backscheduler.shutdown(wait=False)
                    print('Errors!')
            elif trigger=='cron':
                if stime:
                    start_time = stime
                    end_time = etime
                else:
                    raise AssertionError('ERROR,时间参数不能为空')
                backscheduler.add_job(func=function, trigger=f'{trigger}', start_date=start_time,
                          end_date=end_time, args=args)
                backscheduler.start()
                try:
                    backscheduler.start()
                except (KeyboardInterrupt, SystemExit):
                    backscheduler.shutdown(wait=False)
                    print('Errors!')
            else:
                raise AssertionError('ERROR,暂无支持该参数')
        else:
            raise AssertionError('ERROR,暂无支持该参数')

    def check_two_list(self,actualResult, expectResult):
        '''
        根据列表第一个元素校验列表数据
        :param actualResult:
        :param expectResult:
        :return:
        '''
        if actualResult != [] or expectResult != []:
            for index1, item1 in enumerate(actualResult):
                for index2, item2 in enumerate(expectResult):
                    if item1[0] == item2[0]:
                        new_item1 = []
                        new_item2 = []
                        for aip_data in item1[1:]:
                            if aip_data == None or aip_data == 0:
                                api_result = 0
                            else:
                                api_result = float(aip_data)
                            new_item1.append(api_result)
                        for sql_data in item2[1:]:
                            if sql_data == None or sql_data == 0:
                                sql_result = 0
                            else:
                                sql_result = float(sql_data)
                            new_item2.append(sql_result)

                        if new_item1 != new_item2:
                            raise AssertionError(f"两个列表数据不一致！实际结果：{new_item1}  期待结果：{new_item2}")
                        else:
                            pass
        else:
            pass


    def tuple_to_list(self, tuple_in, *agrs): #  *agrs指的是输入的数据类型为元组
        '''
        嵌套的列表转元组，[('XHBWcd8LzVE7', 3, '3_4_1', 1, '1.220'), ('XHBWcd8LzVE7', 3, '3_4_1', 2, '1.220'), ('XHBWcd8LzVE7', 3, '3_4_1', 1, '1.100')]
        简洁写法：b = [list(item) for item in a_list]
        :param tuple_in:
        :param agrs:
        :return:
        '''
        list_out = []
        for item in tuple_in:
            lt = list(item)              #把元组类型全部变成列表类型
            list_out.append(lt)        #把输出填充到列表list_out中

        return list_out


    def request_type(self, method, url, head=None, data=None, *args, **kwargs):
        '''
        获取请求返回响应数据，循环3次
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


    def get_dataBase_environment_config(self):
        '''
        获取数据库环境配置
        :return:
        '''
        configure = Yaml_data().get_yaml_data(fileDir=db_config, isAll=True)
        oracle_info = []
        if configure[0]['environment'] == "testing" and configure[0]['project'] == "yolink":
            oarcle_dic = configure[1]['yolink_testing']
            oracle_info.extend([oarcle_dic['host'], oarcle_dic['user'], oarcle_dic['password'], oarcle_dic['port']])
        elif configure[0]['environment'] == "testing" and configure[0]['project'] == "kaoqin":
            oarcle_dic = configure[1]['kaoqin_testing']
            oracle_info.extend([oarcle_dic['host'], oarcle_dic['user'], oarcle_dic['password'], oarcle_dic['port']])
        elif configure[0]['environment'] == "testing" and configure[0]['project'] == "common":
            oarcle_dic = configure[1]['common_testing']
            oracle_info.extend([oarcle_dic['host'], oarcle_dic['user'], oarcle_dic['password'], oarcle_dic['port']])
        elif configure[0]['environment'] == "production" and configure[0]['project'] == "yolink":
            oarcle_dic = configure[1]['yolink_production']
            oracle_info.extend([oarcle_dic['host'], oarcle_dic['user'], oarcle_dic['password'], oarcle_dic['port']])
        elif configure[0]['environment'] == "production" and configure[0]['project'] == "common":
            oarcle_dic = configure[1]['common_production']
            oracle_info.extend([oarcle_dic['host'], oarcle_dic['user'], oarcle_dic['password'], oarcle_dic['port']])
        else:
            raise AssertionError('ERROR,this environment is not available')

        return oracle_info

    def get_BaseUrl_environment_config(self):
        '''
        获取基础IP路径配置
        :return:
        '''
        configure = Yaml_data().get_yaml_data(fileDir=base_url_config, isAll=True)
        if configure[0]['environment'] == "testing":
            base_url = configure[0]['testing_url']['url']
        elif configure[0]['environment'] == "production":
            base_url = configure[0]['production_url']['url']
        else:
            raise AssertionError('ERROR,this environment is not available')

        return base_url


class round(object):

    #返回浮点数类型的值
    def roundFloat(self, value, digit):
        '''
        保留小数四舍五入,遇六进一进行四舍五入
        :param value:
        :param digit:
        '''
        result = str(value)
        if (float(value) < 0):
            result = result[1:]
            if (result != ''):
                indexDec = result.find('.')
                if (indexDec > 0):
                    decimal = result[indexDec + 1:]
                    decimalCount = len(decimal)
                    if (decimalCount > digit):
                        xiaoshu = result[indexDec + digit + 1]  # 第digit+1位小数
                        if (int(xiaoshu) > 4):
                            result = str(float(value) * -1 + pow(10, digit * -1))
                            # 存在进位的可能，小数点会移位
                            indexDec = result.find('.')
                            result = result[:indexDec + digit + 1]
                        else:
                            result = result[:indexDec + digit + 1]
                    else:
                        lens = digit - len(result[indexDec:]) + 1
                        for i in range(lens):
                            result += '0'
            result = float(result) * -1
            return result
        else:
            if (result != ''):
                indexDec = result.find('.')
                if (indexDec > 0):
                    decimal = result[indexDec + 1:]
                    decimalCount = len(decimal)
                    if (decimalCount > digit):
                        xiaoshu = result[indexDec + digit + 1]  # 第digit+1位小数
                        if (int(xiaoshu) > 4):
                            result = str(float(value) + pow(10, digit * -1))
                            # 存在进位的可能，小数点会移位
                            indexDec = result.find('.')
                            result = result[:indexDec + digit + 1]
                        else:
                            result = result[:indexDec + digit + 1]
                    else:
                        lens = digit - len(result[indexDec:]) + 1
                        for i in range(lens):
                            result += '0'
            return float(result)

    #返回字符串类型的值
    def roundStr(self,value, digit):
        '''
        保留小数四舍五入,遇六进一进行四舍五入
        :param value:
        :param digit:
        '''
        result = str(value)
        if (float(value) < 0):
            result = result[1:]
            if (result != ''):

                indexDec = result.find('.')
                if (indexDec > 0):
                    decimal = result[indexDec + 1:]
                    decimalCount = len(decimal)
                    if (decimalCount > digit):
                        xiaoshu = result[indexDec + digit + 1]  # 第digit+1位小数
                        if (int(xiaoshu) > 4):
                            result = str(float(value) * -1 + pow(10, digit * -1))
                            # 存在进位的可能，小数点会移位
                            indexDec = result.find('.')
                            result = result[:indexDec + digit + 1]
                        else:
                            result = result[:indexDec + digit + 1]
                    else:
                        lens = digit - len(result[indexDec:]) + 1
                        for i in range(lens):
                            result += '0'
            # result = float(result) * -1
            return '-'+result
        else:
            if (result != ''):
                indexDec = result.find('.')
                if (indexDec > 0):
                    decimal = result[indexDec + 1:]
                    decimalCount = len(decimal)
                    if (decimalCount > digit):
                        xiaoshu = result[indexDec + digit + 1]  # 第digit+1位小数
                        if (int(xiaoshu) > 4):
                            dg=pow(10, digit * -1)
                            result = str(float(value) +dg )
                            # 存在进位的可能，小数点会移位
                            indexDec = result.find('.')
                            result = result[:indexDec + digit + 1]
                        else:
                            result = result[:indexDec + digit + 1]
                    else:
                        lens = digit - len(result[indexDec:]) + 1
                        for i in range(lens):
                            result += '0'
            return result


    def up_rounding(self, num):
        """
        小数向上取整
        :param num:
        :return:
        """
        if '.' in str(num):
            return int(str(num).split('.')[0]) + 1
        else:
            return int(num)

    def get_float_length(self, num, query_type='float'):
        '''
        获取浮点数小数位后长度, 先将浮点数转化为字符串，然后截取小数点右边的字符，在使用len函数。
        :param num:
        :param query_type:  float/int/total 获取小数位/整数位/总长度
        :return:
        '''
        if query_type == 'float':
            length = len(str(num).split(".")[1])
            # length = len(str(num)) - str(num).find(".")
        elif query_type == 'int':
            length = str(num).find(".")
        elif query_type == 'total':
            length = len(str(num))
        else:
            raise AssertionError('ERROR,暂不支持此参数类型')

        return length

    def new_round(self, num):
        '''
        保留整数四舍五入,遇六进一进行四舍五入
        :param num:
        :return:
        '''
        if '.' in str(num):
            n_list = str(num).split('.')
            print(n_list)
            if int(n_list[1][0]) >= 5:
                return int(n_list[0]) + 1
            else:
                return int(n_list[0])
        else:
            return int(num)



if __name__ == "__main__":

    cf = CommonFunc()
    # number = cf.new_round(num=2346.23602)
    # number = round().roundStr(2346.23602, 2)
    # print(number)

    # ra = cf.get_random_num(length=2)
    # print(ra)
    oracle_info = cf.get_dataBase_environment_config()
    # oracle_info = cf.get_BaseUrl_environment_config()
    # print(oracle_info)



