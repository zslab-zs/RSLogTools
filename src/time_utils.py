# coding=UTF-8
"""
时间处理工具模块
包含与时间相关的各种功能函数
"""

import time
import os

import random

def get_auto_time_data():
    """
    获取当前时间并格式化(包含随机ID)
    返回:
        tuple: (today日期, now_date完整时间_随机ID)
    """
    today = time.strftime("%Y-%m-%d", time.localtime())  # 获取今天的日期
    now_date = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())  # 获取现在的时间(用下划线代替空格)
    random_id = f"{random.randint(0, 99):02d}"  # 生成2位随机数
    return today, f"{now_date}_{random_id}"

def mkdir_log_dir(log_path_value):
    """
    创建日志目录
    参数:
        log_path_value (str): 日志目录路径
    """
    if not os.path.exists(log_path_value):
        os.makedirs(log_path_value)

def get_current_timestamp():
    """
    获取当前精确时间戳(精确到秒)
    返回:
        str: 格式为YYYY-MM-DD_HH.MM.SS的时间字符串
    """
    return time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
