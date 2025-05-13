#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工作流结果汇总生成器
功能：将多个工作流执行结果文件汇总成一个Markdown报告
"""

import os
import glob
import configparser
from datetime import datetime
from pathlib import Path

def load_config():
    """从config.conf加载配置"""
    config = configparser.ConfigParser()
    config.read('config.conf')
    
    try:
        return {
            'workflow_result_dir': config.get('dify_api_filter', 'workflow_result_dir'),
            'summary_file': config.get('dify_api_filter', 'summary_file')
        }
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"配置错误: {str(e)}")
        print("请在config.conf的[dify_api_filter]部分配置以下参数:")
        print("- workflow_result_dir: 工作流结果目录")
        print("- summary_file: 汇总报告文件路径")
        exit(1)

def get_file_metadata(filepath):
    """获取文件元数据"""
    stat = os.stat(filepath)
    return {
        'size': round(stat.st_size/1024, 1),  # KB
        'mtime': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    }

def read_workflow_files(config):
    """读取所有工作流结果文件"""
    pattern = os.path.join(config['workflow_result_dir'], "dify_workflow_*.txt")
    return glob.glob(pattern)

def generate_summary(files):
    """生成Markdown汇总报告"""
    content = [
        "# 工作流执行结果汇总",
        f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**包含文件数**: {len(files)}\n"
    ]
    
    for idx, filepath in enumerate(files, 1):
        filename = os.path.basename(filepath)
        source_file = filename.replace("dify_workflow_", "").replace(".txt", "")
        metadata = get_file_metadata(filepath)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 提取表格部分
        table_start = file_content.find('|')
        table_end = file_content.find('\n\n', table_start)
        table_content = file_content[table_start:table_end] if table_start != -1 else file_content
        
        # 提取表格后的所有内容作为补充信息
        supplement_content = file_content[table_end:].strip() if table_end != -1 else ""
        
        content.extend([
            f"\n---\n\n## 设备检查报告: {source_file}",
            f"**处理时间**: {metadata['mtime']}",
            f"**文件大小**: {metadata['size']} KB\n",
            table_content,
            f"\n\n{supplement_content}" if supplement_content else ""
        ])
    
    return "\n".join(content)

def main():
    """主函数"""
    config = load_config()
    Path(config['workflow_result_dir']).mkdir(parents=True, exist_ok=True)
    
    workflow_files = read_workflow_files(config)
    if not workflow_files:
        print("未找到工作流结果文件")
        return
    
    summary = generate_summary(workflow_files)
    
    with open(config['summary_file'], 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print(f"汇总报告已生成: {config['summary_file']}")

if __name__ == "__main__":
    main()
