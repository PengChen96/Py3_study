import socket

sk = socket.socket()
sk.bind(("127.0.0.1",8888))
sk.listen(5)    # 设置监听，最多可有5个客户端进行排队

while True:
    conn,addr = sk.accept()     # 阻塞状态，被动等待客户端的连接
    print(conn)
    print(addr)
    while True:
        accept_data_b = conn.recv(1024)   # conn.recv()接收客户端的内容，接收到的是bytes类型数据，
        accept_data_u = str(accept_data_b,encoding="utf-8")
        print("".join(("接收内容：", accept_data_u, "    客户端口：", str(addr[1]))))
        if accept_data_u == "q":
            break
        send_data = input("输入的内容：")
        # 发送内容必须为bytes类型数据，bytes(data, encoding="utf8")用“utf8”格式进行编码
        conn.sendall(bytes(send_data,encoding="utf-8"))
    conn.close()