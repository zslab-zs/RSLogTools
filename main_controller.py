#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络设备巡检系统主控制器
功能：
1. 执行设备巡检（auto_ops_rundevvice.py）
2. 处理日志文件（dify_batch_processor.py）
3. 生成汇总报告（dify_workflow_summary_generator.py）
"""

import os
import sys
import subprocess
import time

from pathlib import Path
from src.auto_ops_rundevice import auto_ops_rundevice as auto_ops_rundevice
from src.dify_batch_processor import process_files as dify_batch_processor
from src.dify_workflow_summary_generator import main as dify_workflow_summary_generator

# 颜色定义
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """清屏函数"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印标题"""
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("====================================")
    print("     网络设备巡检工具主控程序")
    print("本工具github地址：https://github.com/zslab-zs/RSLogTools")
    print("本工具gitee地址：https://gitee.com/zslab/RSLogTools")
    print("====================================")
    print(f"{Colors.ENDC}")

def run_with_status(module_name, command, is_function=False):
    """带状态显示执行任务"""
    print(f"\n{Colors.OKBLUE}▶ 正在执行 {module_name}...{Colors.ENDC}")
    start_time = time.time()
    
    try:
        if is_function:
            result = command()
            elapsed = time.time() - start_time
            print(f"{Colors.OKGREEN}✓ 完成 ({elapsed:.1f}s){Colors.ENDC}")
            if result is not None:
                print(str(result))
            return True
        else:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding='gbk'
            )
            elapsed = time.time() - start_time
            print(f"{Colors.OKGREEN}✓ 完成 ({elapsed:.1f}s){Colors.ENDC}")
            print(result.stdout)
            return True
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"{Colors.FAIL}✗ 失败 ({elapsed:.1f}s){Colors.ENDC}")
        print(f"错误输出:\n{str(e)}")
        return False

def run_device_inspection():
    """执行设备巡检"""
    print("开始执行设备巡检...") 
    result = run_with_status(
        "设备巡检",
        auto_ops_rundevice,
        is_function=True
    )
    print(result)
    return result

def process_logs():
    """处理日志文件"""
    return run_with_status(
        "日志处理",
        dify_batch_processor,
        is_function=True
    )

def generate_report():
    """生成汇总报告"""
    return run_with_status(
        "报告生成",
        dify_workflow_summary_generator,
        is_function=True
    )

def show_menu():
    """显示主菜单"""
    print_header()
    print(f"{Colors.BOLD}请选择操作:{Colors.ENDC}")
    print("1. 执行设备巡检")
    print("2. 处理日志文件") 
    print("3. 生成汇总报告")
    print("q. 退出工具")
    print("------------------------------------")

def main():
    while True:
        show_menu()
        choice = input("请输入选项 (1-3): ").strip()
        
        if choice == "1":
            run_device_inspection()
        elif choice == "2":
            process_logs()
        elif choice == "3":
            generate_report()
        elif choice == "q":
            print(f"\n{Colors.OKBLUE}感谢使用，再见！{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"{Colors.WARNING}无效输入，请重新选择{Colors.ENDC}")
        
        input("\n按Enter键返回主菜单...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}用户中断，程序退出{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}发生未捕获异常: {str(e)}{Colors.ENDC}")
        sys.exit(1)
