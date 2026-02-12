import socket
import threading

class ClientHandler:
    def __init__(self, client_socket):
        self.conn = client_socket  # 客户端的通信socket（唯一的socket）
        self.running = True        # 控制收发循环的开关

    def receive_loop(self):
        """客户端接收服务器消息的循环（独立线程）"""
        try:
            while self.running:
                # 阻塞等待接收服务器数据
                data = self.conn.recv(1024)
                if not data:  # 服务器断开连接
                    print("服务器已断开连接")
                    self.running = False
                    break
                # 解码并打印消息
                msg = data.decode('utf-8')
                print(f"\n收到服务器消息：{msg}")
                # 收到exit则退出
                if msg.strip().lower() == 'exit':
                    print("服务器发送退出指令，准备关闭客户端")
                    self.running = False
                    break
        except (UnicodeDecodeError, OSError) as e:
            if self.running:  # 排除主动退出导致的异常
                print(f"接收消息失败：{str(e)}")
        finally:
            self.conn.close()

    def send_loop(self):
        """客户端手动输入消息发送给服务器的循环（独立线程）"""
        try:
            while self.running:
                # 输入要发送的消息（加提示，避免和接收消息混在一起）
                msg = input("请输入要发送的消息（输入exit退出）：")
                if not self.running:  # 若已触发退出，直接结束
                    break
                # 输入exit则触发退出
                if msg.strip().lower() == 'exit':
                    print("客户端主动退出")
                    self.running = False
                    # 最后给服务器发一次exit，通知服务器
                    self.conn.send(msg.encode('utf-8'))
                    break
                # 发送消息给服务器
                self.conn.send(msg.encode('utf-8'))
        except OSError as e:
            print(f"发送消息失败：{str(e)}")
        finally:
            self.conn.close()

if __name__ == '__main__':
    # 1. 创建客户端TCP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = ('127.0.0.1', 7080)  # 服务器的IP和端口（必须和服务器一致）

    try:
        # 2. 连接服务器（客户端核心步骤，替代服务器的bind/listen/accept）
        client_socket.connect(server_addr)
        print(f"成功连接到服务器：{server_addr[0]}:{server_addr[1]}")

        # 3. 初始化Handler，传入客户端的通信socket
        handler = ClientHandler(client_socket)

        # 4. 创建并启动收发线程（调用Handler的收发方法）
        receive_thread = threading.Thread(target=handler.receive_loop, daemon=True)
        send_thread = threading.Thread(target=handler.send_loop, daemon=True)
        receive_thread.start()
        send_thread.start()

        # 5. 等待线程结束（主线程阻塞，直到退出）
        send_thread.join()
        receive_thread.join()

    except ConnectionRefusedError:
        print(f"连接失败：服务器 {server_addr[0]}:{server_addr[1]} 未启动或不可达")
    except KeyboardInterrupt:
        print("\n客户端被手动中断")
        handler.running = False  # 触发所有线程退出
    finally:
        # 确保socket关闭
        client_socket.close()
        print("客户端已关闭")