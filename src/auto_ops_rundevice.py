# coding=UTF-8
"""
华为设备自动化运维主程序
整合各功能模块实现自动化运维
"""

import os
import time
from concurrent.futures import ThreadPoolExecutor
from netmiko import ConnectHandler
from src.time_utils import get_auto_time_data, mkdir_log_dir
from src.device_utils import get_batch_device_infos, config_option_key_type_value
from src.network_ops import auto_ops_device_command, auto_save_error_log

# 获取配置项
log_path = config_option_key_type_value("log_path")
device_file = config_option_key_type_value("device_file")
config_file = config_option_key_type_value("config_file")

# 创建日志目录
mkdir_log_dir(log_path)

# 获取设备信息
device_infos = get_batch_device_infos(device_file)

def process_device(device_connect_infos, config_file, log_path):
    """处理单个设备的线程函数"""
    # 每个线程获取独立的时间戳
    today, now_date = get_auto_time_data()
    try:
        # 设备连接信息
        huawei = {
            "device_type": "huawei",
            "host": device_connect_infos["ip"],
            "username": device_connect_infos["username"],
            "password": device_connect_infos["password"],
            "secret": device_connect_infos["secret"],
            "port": device_connect_infos["sshport"],
        }
        
        # 连接设备
        connect = ConnectHandler(**huawei)
        
        # 执行设备操作
        auto_ops_device_command(device_connect_infos, connect, today, now_date, config_file)
        
    except Exception as e:
        # 记录错误日志
        error_log = f"设备{device_connect_infos['ip']}操作失败: {str(e)}\n"
        log_file = auto_save_error_log(log_path, today, now_date, error_log)
        print(f"错误日志已保存到: {log_file}")


def auto_ops_rundevice():
    # 并发执行设备操作
    max_workers = int(config_option_key_type_value("max_workers"))  # 从配置读取最大并发线程数
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for device_connect_infos in device_infos:
            future = executor.submit(
                process_device,
                device_connect_infos,
                config_file,
                log_path
            )
            futures.append(future)
        
        # 等待所有任务完成
        for future in futures:
            future.result()

    print("\n所有设备操作完成")


if __name__ == "__main__":  #模块判断是以什么形式运行
    auto_ops_rundevice()
