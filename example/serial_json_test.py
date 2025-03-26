import serial
import json
import time

class Mega2560Serial:
    def __init__(self, port="COM6", baudrate=2000000, timeout=1):
        """初始化串口"""
        self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def send_command(self, ch, mode, chtype, value=None):
        """发送 JSON 指令到 MEGA2560"""
        command = {"ch": ch, "mode": mode, "chtype": chtype}
        if value is not None:
            command["value"] = value
        json_data = json.dumps(command) + "\n"

        print("[发送] ->", json_data.strip())  # 打印发送的 JSON 指令
        self.ser.write(json_data.encode())  # 发送数据

    def read_response(self):
        """读取 MEGA2560 返回的数据"""
        while True:
            try:
                line = self.ser.readline().decode().strip()  # 读取串口数据
                if line:
                    print("[接收] <-", line)  # 打印收到的 JSON 数据
                    return json.loads(line)  # 解析 JSON
            except Exception as e:
                print("[错误] JSON 解析失败:", e)
                return None

# **测试代码**
if __name__ == "__main__":
    mega = Mega2560Serial(port="COM6")  # 请修改 COM 端口号

    time.sleep(2)  # 等待串口稳定

    # 发送指令: 让通道 2 输出 2.5V 模拟信号
    mega.send_command(ch=0, mode="write", chtype="analog", value=2.5)
    
    # 读取 Arduino 反馈
    response = mega.read_response()
    print("[最终输出] ", response)
