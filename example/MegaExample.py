import time
import threading
from Mega2560Serial import Mega2560Serial  # 确保 `Mega2560Serial` 在同一目录下

def menu():
    print("\n=== MEGA2560 测试菜单 ===")
    print("1. 设置数字 IO（高/低）")
    print("2. 设置模拟输出（PWM/DAC）")
    print("3. 设置 8 位数字 IO")
    print("4. 读取数字 IO")
    print("5. 读取模拟输入（ADC）")
    print("6. 读取 8 位数字 IO")
    print("7. 退出")
    print("========================")

def user_input_thread(mega):
    while True:
        menu()
        choice = input("请输入选项 (1-7): ")

        if choice == "1":
            ch = int(input("通道号 (0-7): "))
            state = int(input("状态 (0=低, 1=高): "))
            mega.set_digital(ch, state)

        elif choice == "2":
            ch = int(input("通道号 (0-1): "))
            value = float(input("输入模拟值 (0-5V): "))
            mega.set_analog(ch, value)

        elif choice == "3":
            ch = int(input("通道号 (0-1): "))
            value = int(input("8 位数值 (0-255): "))
            mega.set_digital_8bit(ch, value)

        elif choice == "4":
            ch = int(input("通道号 (0-7): "))
            response = mega.read_digital(ch)
            print(f"通道 {ch} 读取值: {response}")

        elif choice == "5":
            ch = int(input("通道号 (0-7): "))
            response = mega.read_analog(ch)
            print(f"通道 {ch} 模拟值: {response}")

        elif choice == "6":
            ch = int(input("通道号 (0-1): "))
            response = mega.read_digital_8bit(ch)
            print(f"通道 {ch} 8 位数据: {response}")

        elif choice == "7":
            print("[INFO] 退出程序")
            break

        else:
            print("[ERROR] 请输入有效选项!")

if __name__ == "__main__":
    mega = Mega2560Serial(port="COM6")
    time.sleep(2)  # 等待串口稳定

    # 创建线程运行用户输入，以避免阻塞
    user_thread = threading.Thread(target=user_input_thread, args=(mega,))
    user_thread.start()
