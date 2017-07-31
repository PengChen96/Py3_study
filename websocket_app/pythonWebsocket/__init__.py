
import socket
import base64,hashlib
import threading
import struct
from collections import deque

HANDSHAKE_STR = (
   "HTTP/1.1 101 Switching Protocols\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Accept: %(token)s\r\n\r\n"
)
GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
STREAM = 0x0
TEXT = 0x1
BINARY = 0x2
CLOSE = 0x8
PING = 0x9
PONG = 0xA


class WebSocket(threading.Thread):
    def __init__(self,conn,addr,index):
        threading.Thread.__init__(self)
        self.index = index
        self.conn = conn
        self.addr = addr
        #发送的数据缓存
        self.buffer = bytearray()
        self.sendToClientData = deque()

    # 组装header 获取‘Sec-WebSocket-Key’
    def parseHeaders(self, msg):
        # print(msg)
        headers = {}
        msg = str(msg, encoding="utf-8")
        header, data = msg.split('\r\n\r\n', 1)
        for x in header.split("\r\n")[1:]:
            # 这里是 “:+space”
            key, value = x.split(": ", 1)
            headers[key] = value
        return headers
    # 握手数据
    def handShakeData(self,c_req):
        sec_key = self.parseHeaders(c_req)['Sec-WebSocket-Key']
        key = sec_key.encode("ascii") + GUID_STR.encode("ascii")
        accept_token = base64.b64encode(hashlib.sha1(key).digest()).decode("ascii")
        s_res = HANDSHAKE_STR % {'token': accept_token}
        return s_res
    # 得到数据长度 （包含描述字节）
    def getMsglen(self,msg):
        g_code_length = msg[1] & 127
        if g_code_length == 126:
            g_code_length = struct.unpack('!H', msg[2:4])[0]
            g_code_length += 8
        elif g_code_length == 127:
            g_code_length = struct.unpack('!Q', msg[2:10])[0]
            g_code_length += 14
        else:
            g_code_length += 6
        g_code_length = int(g_code_length)
        print(g_code_length)
        return g_code_length
    # 解析数据
    def parseData(self,msg):
        g_code_length = msg[1] & 127
        if g_code_length == 126:
            g_code_length = struct.unpack('!H', msg[2:4])[0]
            masks = msg[4:8]
            data = msg[8:]
        elif g_code_length == 127:
            g_code_length = struct.unpack('!Q', msg[2:10])[0]
            masks = msg[10:14]
            data = msg[14:]
        else:
            masks = msg[2:6]
            data = msg[6:]

        i = 0
        raw_by = bytearray()
        for d in data:
            raw_by.append( int(d) ^ int(masks[i % 4]) )
            i += 1
        print(raw_by)
        print(u"总长度是：%d" % int(g_code_length))
        raw_str = raw_by.decode()
        # raw_str = str(raw_by)
        return raw_str
    # 发送消息
    def sendMessage(self,message):
        # 遍历连接上的列表
        for conn in connections.values():
            # 发送消息到client （除了自己）
            if conn != self.conn:
                self._sendMessage(False,TEXT,message)
                while self.sendToClientData:
                    data = self.sendToClientData.popleft()
                    conn.send(data[1])

    # FIN 后面是否还有数据；opcode 传输的数据包类型；message 传输的数据
    def _sendMessage(self,FIN,opcode,message):
        payload = bytearray()
        b1 = 0
        b2 = 0
        if FIN is False:
            b1 |= 0x80
        b1 |= opcode        # 若opcode=TEXT    b'0x81'

        payload.append(b1)      #
        msg_utf = message.encode('utf-8')
        msg_len = len(msg_utf)

        if msg_len <= 125:
            b2 |= msg_len

            payload.append(b2)
        elif msg_len >= 126 and msg_len <= 65535:
            b2 |= 126
            payload.append(b2)
            payload.extend(struct.pack("!H", msg_len))
        elif msg_len <= (2 ^ 64 - 1):
            b2 |= 127
            payload.append(b2)
            payload.extend(struct.pack("!Q", msg_len))
        else:
            print("传输的数据太长了! ——(_sendMessage)")
        # 拼接上需要发送的数据
        # 格式大概这样：bytearray(b'\x81\x0cHello World!')   '\x0c'是发送的数据长度
        if msg_len > 0:
            payload.extend(msg_utf)

        self.sendToClientData.append((opcode,payload))

    # 端开连接
    def _disConnected(self):
        self.conn.close()
        print("断开的连接conn%s" % (self.index))
        print(connections)
        del connections['conn%s' % (self.index)]
        print(connections)
    # 线程
    def run(self):
        # print(self.listeners)
        self.isHandShake = False
        while True:
            if self.isHandShake == False:
                print("start handshake %s" % (self.addr[0]))
                # 接收客户端内容
                c_req = self.conn.recv(1024)
                # print(c_req)
                handData = self.handShakeData(c_req)
                self.conn.sendall(str.encode(handData))
                self.isHandShake = True
            else:
                message = self.conn.recv(16384)    # 16 * 1024   16384   # bytes
                print(message)
                # 断开连接
                if message[0]&127 == CLOSE:    # 0x88   136
                    self._disConnected()
                    return
                self.buffer.extend(message)  # bytes
                code_length = self.getMsglen(self.buffer)  # 数据中带的 数据长度（包含描述字节）
                # 数据完整就发送
                if code_length == len(self.buffer):
                    buffer_utf = self.parseData(self.buffer)      # str
                    self.sendMessage(buffer_utf)
                    print(message)
                    self.buffer = bytearray()

connections = {}
class websocketServer(object):
    def __init__(self,host, port):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)

    def server(self):
        print(self.serversocket)
        index =0
        while True:
            conn,addr = self.serversocket.accept()
            print(conn)
            print(addr)
            # 新建线程
            newSocket = WebSocket(conn,addr,index)
            # 开始线程,执行run函数
            newSocket.start()
            connections['conn%s'% (index)] = conn
            index += 1
            print(connections)


websocketServer = websocketServer("127.0.0.1",8000)
websocketServer.server()