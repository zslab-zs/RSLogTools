# coding=UTF-8
"""
网络设备操作模块
包含设备连接、命令执行、日志记录等功能
"""

from netmiko import ConnectHandler
import time
import os
import configparser
from src.time_utils import get_auto_time_data

def get_log_path():
    """从config.conf读取日志路径配置"""
    config = configparser.ConfigParser()
    config.read('config.conf')
    return config.get('auto_ops_huawei', 'log_path', fallback='Log')

def send_config_auto_ops_save_log(device_connect_infos, connect, today, now_date, config_file):
    """
    发送配置并保存日志
    参数:
        device_connect_infos (dict): 设备连接信息
        connect: netmiko连接对象
        today (str): 当前日期
        now_date (str): 当前时间
        config_file (str): 配置文件路径
    """
    output = connect.send_config_from_file(config_file)
    # print(output)
    time.sleep(1)
    connect.disconnect()

    # 使用传入的now_date参数(已包含随机ID)
    log_file_name = f"{now_date}_{device_connect_infos['ip']}.txt"
    log_path = get_log_path()
    log_file_path = os.path.join(log_path, log_file_name)
    
    # 确保目录存在
    os.makedirs(log_path, exist_ok=True)
    with open(log_file_path, "w", encoding="utf-8") as save_log:
        save_log.write(output)
        print(f"\n-----------------设备{device_connect_infos['ip']}保存成功-------------------")
        # print(f"设备{device_connect_infos['ip']}保存成功")

def device_super_run_commands(device_connect_infos, connect, today, now_date, config_file):
    """
    设备提权并执行命令
    参数:
        device_connect_infos (dict): 设备连接信息
        connect: netmiko连接对象
        today (str): 当前日期
        now_date (str): 当前时间
        config_file (str): 配置文件路径
    """
    connect.send_command_timing("super\n")
    try:
        connect.send_command_timing(device_connect_infos["secret"])
        connect.send_command_timing("sys")
        connect.send_command_timing("quit")
        print("提权成功")
        send_config_auto_ops_save_log(device_connect_infos, connect, today, now_date, config_file)
    except Exception:
        connect.disconnect()
        print("提权失败请检查")

def auto_ops_device_command(device_connect_infos, connect, today, now_date, config_file):
    """
    自动执行设备操作
    参数:
        device_connect_infos (dict): 设备连接信息
        connect: netmiko连接对象
        today (str): 当前日期
        now_date (str): 当前时间
        config_file (str): 配置文件路径
    """
    print(f"\n-----------------成功登录到设备{device_connect_infos['ip']}-----------------")
    try:
        send_config_auto_ops_save_log(device_connect_infos, connect, today, now_date, config_file)
    except ValueError:
        print("无法执行命令发送，尝试提权")
        device_super_run_commands(device_connect_infos, connect, today, now_date, config_file)

def auto_save_error_log(log_path, today, now_date, error_log):
    """
    保存错误日志(每个错误单独文件)
    参数:
        log_path (str): 日志路径
        today (str): 当前日期
        now_date (str): 当前时间(含随机ID)
        error_log (str): 错误信息
    返回:
        str: 日志文件完整路径
    """
    error_file = f"{log_path}/{now_date}_error.txt"
    with open(error_file, "w", encoding="utf-8") as f:
        f.write(f"{now_date} {error_log}")
        print(f"错误日志已保存到单独文件: {error_file}\n")
    return error_file
