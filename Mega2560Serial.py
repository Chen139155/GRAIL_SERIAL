import serial
import json
import time

class Mega2560Serial:
    def __init__(self, port="COM6", baudrate=2000000, timeout=0.1):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            print(f"[INFO] 连接到 {port}，波特率 {baudrate}")
        except Exception as e:
            print(f"[ERROR] 无法打开串口 {port}: {e}")
            self.ser = None

    def send_command(self, ch, mode, chtype, value=None):
        """ 发送 JSON 命令到 MEGA2560，并打印调试信息 """
        if not self.ser:
            print("[ERROR] 串口未初始化")
            return

        command = {"ch": ch, "mode": mode, "chtype": chtype}
        if value is not None:
            command["value"] = value

        json_data = json.dumps(command) + "\n"
        self.ser.write(json_data.encode())
        print(f"[TX] 发送数据: {json_data.strip()}")

    def read_response(self):
        """ 读取 MEGA2560 反馈数据，并打印调试信息 """
        if not self.ser:
            return None

        try:
            line = self.ser.readline().decode().strip()
            if line:
                print(f"[RX] 接收到数据: {line}")
                return json.loads(line)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON 解析失败: {e}, 原始数据: {line}")
        except Exception as e:
            print(f"[ERROR] 读取数据失败: {e}")
        return None
    
    def read_serial(self):
        """ 读取 MEGA2560 反馈数据，并打印调试信息 """
        if not self.ser:
            return None

        try:
            line = self.ser.readline().decode().strip()
            return line
        except Exception as e:
            print(f"[ERROR] 读取数据失败: {e}")
        return None

    def set_digital(self, ch, state):
        """ 设置数字 IO """
        self.send_command(ch, "write", "digital", state)
        time.sleep(0.001) # 延迟少量时间，确保串口数据，如果有bug 可以修改此处

    def set_analog(self, ch, value):
        """ 设置模拟输出 """
        self.send_command(ch, "write", "analog", value)
        time.sleep(0.005) # 延迟少量时间，确保串口数据，如果有bug 可以修改此处

    def set_digital_8bit(self, ch, value):
        """ 设置 8 位数字 IO """
        self.send_command(ch, "write", "digital_8bit", value)

    def read_digital(self, ch):
        """ 读取数字 IO 状态 """
        self.send_command(ch, "read", "digital")
        return self.read_response()

    def read_analog(self, ch):
        """ 读取模拟输入（ADC） """
        self.send_command(ch, "read", "analog")
        return self.read_response()

    def read_digital_8bit(self, ch):
        """ 读取 8 位数字 IO 状态 """
        self.send_command(ch, "read", "digital_8bit")
        return self.read_response()

# 测试代码
if __name__ == "__main__":
    mega = Mega2560Serial(port = "COM6")
    time.sleep(2)  # 等待串口稳定

    # mega.set_analog(0, 2.0)  # MCP4725_1 输出 2.0V
    while True:
        print("[INFO] 设置 DAC 输出")
        mega.set_analog(0, 3.0)  # MCP4725_1 输出 3.0V        
        mega.set_analog(1, 5.0)  # MCP4725_2 输出 5.0V
        time.sleep(0.01)

        print("[INFO] 修改 DAC 输出")
        mega.set_analog(0, 2.0)  # MCP4725_1 输出 2.0V
        time.sleep(0.01)
        
        mega.set_analog(1, 4.0)  # MCP4725_2 输出 4.0V
        time.sleep(0.2)
        # line = mega.read_serial()
    #     if line :
    #         print("[Arduino 输出]", line)
