# 导入Python内置socket库，无需安装
import socket

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

# 5. 收发消息（简单单次通信，入门够用）
try:
    while True:
        recv_msg=conn.recv(1024)
        print(f"收到客户端消息：{recv_msg.decode('utf-8')}")

        if recv_msg.decode('utf-8') == 'quit':
            print('server exit')
            break
        msg_data=input("请输入发送内容：")
        conn.send(msg_data.encode('utf-8'))
        
finally:
    conn.close()
    server_socket.close()
    print("服务端连接已关闭")