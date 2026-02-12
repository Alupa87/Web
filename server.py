import socket
import threading
import time
import sys

class Handler:
    def __init__(self,conn):
        self.conn=conn
        self.running=True

    def Receive(self):
        try:
            while self.running:
                data=self.conn.recv(1024)
                if not data:#data返回空字节时
                    print("客户端已断开")
                    self.running=False
                    break
                if not isinstance(data,bytes):
                    raise TypeError("Received data is not bytes type")
                msg =data.decode('utf-8')
                print(f'{msg}')
                if msg.strip().lower()=='exit':
                    print('client close')
                    self.running=False
                    break
        except(TypeError,UnicodeDecodeError) as e:
            return f"Received message failed{str(e)}"
        finally:
            self.conn.close()
    def Send(self):
        try:
            while self.running:
                msg=input('')
                if msg.strip().lower()=='exit':
                    print('server close')
                    self.running=False
                    break
            self.conn.send(msg.encode('utf-8'))
        except Exception as e:
            print(f'{e}')
        finally:
            self.conn.close()

if __name__ =='__main__':
    # 1. 创建 TCP Socket 对象（AF_INET=IPv4，SOCK_STREAM=TCP协议）
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr='127.0.0.1'
    port=7080
    server_addr=(addr,port)

    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    server_socket.bind(server_addr)
    server_socket.listen(5)
    print(f"端已启动，在 {server_addr[0]}:{server_addr[1]} 等待对方连接...")
    #接受客户端连接（阻塞式，直到有客户端连过来，返回新的通信Socket+客户端地址）
    print(f"成功连接客户端：{server_addr[0]}:{server_addr[1]}")

    try:
        conn,client_addr=server_socket.accept()
        print(f'connected')
        connect=Handler(conn)
        t1=threading.Thread(target=connect.Send,daemon=True).start()
        t2=threading.Thread(target=connect.Receive,daemon=True).start()

        t1.join()
        t2.join()
    except KeyboardInterrupt:
        print('server interrupt manually')
    finally:
        if 'conn' in locals():
            conn.close()
        server_socket.close()
        print("server close")
            
                                  