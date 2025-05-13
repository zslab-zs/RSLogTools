import os
import time
import configparser
from src.dify_api_workflow import dify_auto_log

def load_config():
    """加载配置文件"""
    config = configparser.ConfigParser()
    config.read('config.conf')
    return {
        'upload_url': config.get('dify_api_filter', 'upload_url'),
        'run_workflow_url': config.get('dify_api_filter', 'run_workflow_url'),
        'api_key': config.get('dify_api_filter', 'api_key'),
        'api_user': config.get('dify_api_filter', 'api_user'),
        'log_path_dir': config.get('dify_api_filter', 'log_path_dir'),
        'workflow_result_dir': config.get('dify_api_filter', 'workflow_result_dir')
    }

def process_files():
    """处理目录下所有txt文件并生成详细结果报告"""
    config = load_config()
    log_dir = config['log_path_dir']
    result_dir = config['workflow_result_dir']
    
    # 获取所有txt文件
    txt_files = [f for f in os.listdir(log_dir) 
                if f.endswith('.txt') and os.path.isfile(os.path.join(log_dir, f))]
    
    total = len(txt_files)
    success = 0
    failed = 0
    start_time = time.time()
    file_results = []
    
    print(f"发现 {total} 个待处理文件")
    
    for i, filename in enumerate(txt_files, 1):
        file_start = time.time()
        filepath = os.path.join(log_dir, filename)
        print(f"[{i}/{total}] 正在处理 {filename}...", end='\n', flush=True)
        
        try:
            # 执行工作流
            dify_auto_log(
                config['upload_url'],
                config['run_workflow_url'],
                config['api_key'],
                filepath,
                config['api_user']
            )
            
            # 检查结果文件是否生成
            result_path = f"{result_dir}/dify_workflow_{filename}"
            if not os.path.exists(result_path):
                raise Exception(f"结果文件未生成: {result_path}")
            
            # 检查结果文件内容是否有效
            with open(result_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    raise Exception("结果文件内容为空")
                
            print(f"成功，结果保存到: {result_path}")
            success += 1
            file_results.append({
                'filename': filename,
                'status': '成功',
                'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_start)),
                'elapsed': time.time() - file_start,
                'result_path': result_path
            })
        except Exception as e:
            print(f"失败: {str(e)}")
            failed += 1
            file_results.append({
                'filename': filename,
                'status': '失败',
                'start_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_start)),
                'elapsed': time.time() - file_start,
                'error': str(e)
            })
    
    elapsed = time.time() - start_time
    print(f"\n处理完成: 成功{success}个，失败{failed}个")
    print(f"总耗时: {elapsed:.1f}秒")
    
    # 生成详细结果报告
    with open(f"{result_dir}/result_dify_api_run.txt", 'w', encoding='utf-8') as f:
        f.write(f"[处理结果统计]\n")
        f.write(f"处理时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}\n")
        f.write(f"总文件数: {total}\n")
        f.write(f"成功: {success}\n")
        f.write(f"失败: {failed}\n")
        f.write(f"总耗时: {elapsed:.1f}秒\n\n")
        
        f.write(f"[详细结果]\n")
        for i, res in enumerate(file_results, 1):
            f.write(f"{i}. 文件: {res['filename']}\n")
            f.write(f"   状态: {res['status']}\n")
            f.write(f"   开始时间: {res['start_time']}\n")
            f.write(f"   耗时: {res['elapsed']:.1f}秒\n")
            if res['status'] == '成功':
                f.write(f"   结果文件: {res['result_path']}\n")
            else:
                f.write(f"   错误信息: {res['error']}\n")
            f.write("\n")

if __name__ == "__main__":
    process_files()
