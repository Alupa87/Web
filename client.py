# 导入内置socket库
import socket

# 1. 创建 TCP Socket 对象（和服务端一致，AF_INET+SOCK_STREAM）
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 连接服务端（参数=服务端的IP+端口，必须和服务端bind的一致！）
server_addr = ('127.0.0.1', 8080)
client_socket.connect(server_addr)
print(f"成功连接服务端：{server_addr[0]}:{server_addr[1]}")

# 3. 收发消息（和服务端对应，先发送再接收）
try:
    while True:
        send_msg=input("请输入发送内容：")
        client_socket.send(send_msg.encode('utf-8'))
        if send_msg == 'quit':
            print('client exit')
            break
        msg_data=client_socket.recv(1024)
        print(f"收到服务端回复：{msg_data.decode('utf-8')}")

finally:
    # 4. 关闭连接
    client_socket.close()
    print("客户端连接已关闭")