import requests
import json
import os

def upload_file(_ApiUploadUrl, _ApiKey, _LogFilePath, _ApiUser):
    upload_url = f"{_ApiUploadUrl}"
    headers = {
        "Authorization": f"Bearer {_ApiKey}",
    }
    
    try:
        print("上传文件中...")
        with open(_LogFilePath, 'rb') as file:
            files = {
                'file': (os.path.basename(_LogFilePath), file, 'text/plain')
            }
            data = {
                "user": _ApiUser,
                "type": "TXT"
            }
            
            response = requests.post(upload_url, headers=headers, files=files, data=data)
            if response.status_code == 201:
                print("文件上传成功")
                return response.json().get("id")
            else:
                print(f"文件名 {_LogFilePath}")
                print(f"文件上传失败，状态码: {response.status_code}")
                print(f"响应内容: {response.text}")
                print(f"请求URL: {upload_url}")
                print(f"请求头: {headers}")
                return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def run_workflow(file_id, _ApiRunWorkflowUrl, _ApiKey, _ApiUser, response_mode="blocking"):
    workflow_url = f"{_ApiRunWorkflowUrl}"
    headers = {
        "Authorization": f"Bearer {_ApiKey}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": {
            "RouteSwitchLogFile": {
                "transfer_method": "local_file",
                "upload_file_id": file_id,
                "type": "document"
            }
        },
        "response_mode": response_mode,
        "user": _ApiUser
    }

    try:
        print("运行工作流...")
        response = requests.post(workflow_url, headers=headers, json=data)
        if response.status_code == 200:
            print("工作流执行成功")
            return response.json()
        else:
            print(f"工作流执行失败，状态码: {response.status_code}")
            return {"status": "error", "message": f"Failed to execute workflow, status code: {response.status_code}"}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {"status": "error", "message": str(e)}

def save_workflow_result(log_file_path, workflow_result):
    """保存工作流结果到文件"""
    try:
        import configparser
        config = configparser.ConfigParser()
        config.read('config.conf')
        result_dir = config.get('dify_api_filter', 'workflow_result_dir')
        
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)
        
        base_name = os.path.basename(log_file_path)
        output_file = f"{result_dir}/dify_workflow_{base_name}"
        
        if workflow_result and 'data' in workflow_result and 'outputs' in workflow_result['data']:
            content = workflow_result['data']['outputs']['files']
            # 处理特殊字符和编码问题
            if isinstance(content, str):
                content = content.replace('\x08', '')  # 移除退格字符
                content = content.encode('utf-8', errors='ignore').decode('utf-8')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"工作流结果已保存到: {output_file}")
            return True
        return False
    except Exception as e:
        print(f"保存工作流结果失败: {str(e)}")
        return False

def dify_auto_log(_ApiUploadUrl, _ApiRunWorkflowUrl, _ApiKey, _LogFilePath, _ApiUser):
    file_id = upload_file(_ApiUploadUrl, _ApiKey, _LogFilePath, _ApiUser)
    if file_id:
        result = run_workflow(file_id, _ApiRunWorkflowUrl, _ApiKey, _ApiUser)
        if result.get('status') == 'error':
            raise Exception(f"工作流执行失败: {result.get('message')}")
        if not save_workflow_result(_LogFilePath, result):
            raise Exception("保存工作流结果失败")
        return True
    else:
        raise Exception("文件上传失败，无法执行工作流")
