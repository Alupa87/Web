import socket
import threading
import time

# 1. 创建 TCP Socket 对象（AF_INET=IPv4，SOCK_STREAM=TCP协议）
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定 IP 地址和端口号（元组格式：(IP, 端口)，127.0.0.1=本机，8888=自定义端口）
server_addr = ('127.0.0.1', 8080)
server_socket.bind(server_addr)

# 3. 监听连接（参数5=最大等待连接数，测试时随便写）
server_socket.listen(5)
print(f"服务端已启动，在 {server_addr[0]}:{server_addr[1]} 等待客户端连接...")

# 4. 接受客户端连接（阻塞式，直到有客户端连过来，返回新的通信Socket+客户端地址）
conn, client_addr = server_socket.accept()
print(f"成功连接客户端：{client_addr[0]}:{client_addr[1]}")

class Handler():
    def __init__(self,connection):
        connection=self.connection
    
    def Receive(self,info):
        print(f'Received message:{info.decode('utf-8')}')
        return info

    def Send(self):
        msg=input('Send:')
        msg.encode('utf-8')

if __name__ =='__init__':
    connect=Handler()
    msg=server_socket.recv(1024)
    t1=threading.Thread(target=connect.Send,args=(msg),daemon=True).start()
    t2=threading.Thread(target=connect.Receive,daemon=True).start()
    while True:
        if connect.Receive() == 'exit':
            break

        
                                  