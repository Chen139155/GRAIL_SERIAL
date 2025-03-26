# GRAIL_SERIAL
GRAIL通过mega2560与外部传递信号的接口项目
## 1.项目结构
该项目软件部分由Mega2560端程序‘’Serial2IO/Serial2IO.ino‘’与 PC python端脚本 Mega2560Serial.py 组成

Python端调用Mega类方法向串口发送Json指令

Mega2560 解析串口Json指令并设置或读取对应引脚输出输入
