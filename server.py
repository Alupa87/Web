import socket
import threading
import time

class Handler:
    def __init__(self,info):
        self.info=info

    def Receive(self):
        try:
            if not isinstance(self.info,bytes):
                raise f"self.info should be bytes type"
            print(f"Received message:{self.info.decode('utf-8')}")
            return self.info.decode('utf-8')
        except(TypeError,UnicodeDecodeError) as e:
            return f"Received message failed{str(e)}"

    def Send(self):
        msg=input('Send:')
        return msg.encode('utf-8')

if __name__ =='__main__':
    # 1. 创建 TCP Socket 对象（AF_INET=IPv4，SOCK_STREAM=TCP协议）
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr='127.0.0.1'
    port=8080
    server_addr=(addr,port)
    server_socket.bind(server_addr)
    server_socket.listen(5)
    print(f"端已启动，在 {server_addr[0]}:{server_addr[1]} 等待对方连接...")
    #接受客户端连接（阻塞式，直到有客户端连过来，返回新的通信Socket+客户端地址）
    conn, client_addr = server_socket.accept()
    print(f"成功连接客户端：{client_addr[0]}:{client_addr[1]}")

    info=server_socket.recv(1024)
    connect=Handler(info)
    t1=threading.Thread(target=connect.Send,args=(info),daemon=True).start()
    t2=threading.Thread(target=connect.Receive,daemon=True).start()
    while True:
        if connect.Receive() == 'exit':
            break

        
                                  