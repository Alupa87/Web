# 导入内置socket库
import socket
from test import Handler
import threading
# 1. 创建 TCP Socket 对象（和服务端一致，AF_INET+SOCK_STREAM）
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务端（参数=服务端的IP+端口，必须和服务端bind的一致！）
server_addr = ('127.0.0.1', 8080)
client_socket.connect(server_addr)
print(f"成功连接服务端：{server_addr[0]}:{server_addr[1]}")

# 3. 收发消息（和服务端对应，先发送再接收）
if __name__=='__init__':
    client_handler=Handler()
    msg=client_socket.recv(1024)
    t1=threading.Thread(target=Handler.Receive,args=(msg),daemon=True)
    t2=threading.Thread(target=Handler.Send,daemon=True)
    
