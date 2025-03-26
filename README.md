# GRAIL_SERIAL

GRAIL 通过 Mega2560 进行信号传输的串口通信项目。

## 1. 项目简介
本项目基于 **Arduino Mega2560** 和 **Python**，用于通过串口传输 **JSON** 指令，实现对 **数字/模拟信号** 的读写操作。  

- **Mega2560** 解析串口 **JSON** 指令，控制或读取相应的 **IO** 引脚。  
- **Python 端** 通过 `Mega2560Serial.py` 发送和接收指令。  

## 2. 目录结构
```
├── LICENSE                # 许可证文件
├── README.md              # 项目说明文档
├── Mega2560Serial.py      # Python 端串口通信脚本
├── example/MegaExample.py  # 示例文件
└── Serial2IO/Serial2IO.ino # Arduino Mega2560 端代码
```

## 3. Python 端使用说明
### 3.1 安装依赖
请确保已安装 `pyserial`：
```bash
pip install pyserial
```

### 3.2 示例代码
见 `example/MegaExample.py`

## 4. Mega2560 端说明
Arduino 端代码 `Serial2IO.ino` 需要上传到 Mega2560 开发板，实现对 Python 端 **JSON** 指令的解析和执行。
## 5. Quick Start
1. 连接Grail与数据采集板8/8/8的数据线，并为8/8/8插上直流电源
2. 编译并上传 `Serial2IO.ino` 到 Mega2560 开发板（对认知小组本团队同学，最新版的ino已经烧录，并已接好线路）
3. 将mega2560通过串口连接到电脑，注意COM端口号是否一致，默认COM6
4. 在Dflow使用Phidgets模块选择interface kit，确保Dflow已连接数据采集板。
## 6. 许可证
本项目遵循 **MIT License**，详细信息见 `LICENSE` 文件。

