# 导入内置socket库
import socket
from server import Handler
import threading

# 收发消息（和服务端对应，先发送再接收）
if __name__=='__main__':
    # 1. 创建 TCP Socket 对象（和服务端一致，AF_INET+SOCK_STREAM）
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr='127.0.0.1'
    port=8080
    client_addr=(addr,port)
    client_socket.bind(client_addr)
    server,con=client_socket.connect()
    msg=client_socket.recv(1024)
    client_handler=Handler(msg)
    t1=threading.Thread(target=Handler.Receive,args=(msg),daemon=True).start()
    t2=threading.Thread(target=Handler.Send,daemon=True).start()
    while True:
        if client_handler.Receive() == 'exit':
            break
    client_socket.close()
