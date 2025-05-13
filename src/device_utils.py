# coding=UTF-8
"""
设备配置处理模块
包含设备信息读取、配置文件处理等功能
"""

import pandas as pd
import configparser
from src.time_utils import get_auto_time_data, mkdir_log_dir

def get_batch_device_infos(filename="devices.csv"):
    """
    从设备信息文件读取数据(支持Excel和CSV格式)
    参数:
        filename (str): 文件路径，默认devices.csv
    返回:
        list: 设备信息字典列表
    """
    if filename.endswith('.xlsx'):
        data = pd.read_excel(filename)
    elif filename.endswith('.csv'):
        data = pd.read_csv(filename)
    else:
        raise ValueError("不支持的文件格式，请使用.xlsx或.csv文件")
        
    items = data.to_dict(orient="records")
    device_infos = []
    for device_data in items:
        device_infos.append(device_data)
    return device_infos

def read_global_config_huawei(type=""):
    """
    读取全局配置文件
    参数:
        type (str): 配置项类型
    返回:
        str: 配置项值
    """
    try:
        config = configparser.ConfigParser()
        config.read("config.conf", encoding="utf-8")
        # 读取config.conf里面的auto_ops_huawei字段的内容
        return config.get("auto_ops_huawei", type)
    except configparser.NoSectionError as e:
        raise Exception(f"配置错误: {str(e)} - 请检查配置文件")
    except configparser.NoOptionError as e:
        raise Exception(f"配置错误: {str(e)} - 请检查配置文件")
    except Exception as e:
        raise Exception(f"读取配置文件出错: {str(e)}")

def config_option_key_type_value(config_type):
    """
    获取指定类型的配置值
    参数:
        config_type (str): 配置类型
    返回:
        str: 配置值
    """
    value = read_global_config_huawei(type=config_type)
    if not value:
        raise Exception(f"{config_type} 配置项不能为空")
    return value
