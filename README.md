# RSLogTools网络设备日志自动处理工具

## 项目结构
```
RSLogTools/
├── main_controller.py     # 主控制程序
├── config.conf            # 配置文件
├── devices.csv           # 设备信息CSV文件
├── huawei_commands.txt   # 发送到华为设备的命令
├── requirements.txt      # 依赖包列表
└── src/                  # 源代码模块
    ├── auto_ops_rundevice.py         # 设备巡检模块
    ├── device_utils.py               # 设备工具
    ├── dify_api_workflow.py          # API工作流
    ├── dify_batch_processor.py       # 批量处理器
    ├── dify_workflow.py              # 工作流引擎
    ├── dify_workflow_summary_generator.py # 报告生成器
    ├── network_ops.py                # 网络设备操作
    └── time_utils.py                 # 时间工具
```

## 功能说明
1. **设备巡检**：自动执行设备状态检查
2. **日志处理**：批量处理设备日志文件
3. **报告生成**：自动生成巡检报告
4. **工作流引擎**：支持自定义工作流程
5. **批量操作**：支持多设备并发操作

## 使用方法
1. 配置config.conf文件：
2. 准备设备信息CSV文件(devices.csv)
2. 编辑发送命令txt
2. 运行主程序：

```bash
python main_controller.py
```

详见：[https://blog.zslab.cn/content/tag/rslogtools/](https://blog.misausr.top/RSLogTools/)

## 菜单选项

1. 执行设备巡检
2. 处理日志文件
3. 生成汇总报告

## 依赖安装
```bash
pip install -r requirements.txt
```

## 注意事项
1. 确保Python 3.6+环境
2. 配置文件使用UTF-8编码
3. 日志目录会自动创建
4. 支持Windows/Linux环境
5. 已生成windows的便携工具
6. 工作流引擎注意上下文长度

## 版本更新
- v0.0.1:
  - 支持主控制程序
  - 新增工作流引擎
  - 优化日志处理
  - 改进报告生成功能
