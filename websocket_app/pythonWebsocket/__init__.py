
import socket
import base64,hashlib
import threading
import struct
import time

HANDSHAKE_STR = (
   "HTTP/1.1 101 Switching Protocols\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Accept: %(token)s\r\n\r\n"
)
GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

g_header_length = 0
g_code_length = 0

class WebSocket(threading.Thread):
    def __init__(self,conn,addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.buffer = bytes("",encoding="utf-8")
        self.buffer_utf8 = ""
        self.length_buffer = 0

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
    # 得到数据长度
    def getMsglen(self,msg):
        print(len(msg))
        print(msg[0])
        print(msg[1])
        g_code_length = msg[1] & 127
        received_length = 0;
        if g_code_length == 126:
            # g_code_length = msg[2:4]
            # g_code_length = (ord(msg[2])<<8) + (ord(msg[3]))
            g_code_length = struct.unpack('!H', msg[2:4])[0]
            g_header_length = 8
        elif g_code_length == 127:
            # g_code_length = msg[2:10]
            g_code_length = struct.unpack('!Q', msg[2:10])[0]
            g_header_length = 14
        else:
            g_header_length = 6
        g_code_length = int(g_code_length)
        return g_code_length
    # 解析数据
    def parseData(self,msg):
        g_code_length = msg[1] & 127
        received_length = 0;
        if g_code_length == 126:
            m = msg[2:4]
            print(m)
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
        raw_str = ''

        for d in data:
            raw_str += chr(d ^ masks[i % 4])
            i += 1

        print(u"总长度是：%d" % int(g_code_length))
        return raw_str
    # 发送消息
    def sendMessage(self,conn,message):
        payload = bytearray()
        b1 = 0x80 | 0x1    #  0x81  129
        b2 = 0
        payload.append(b1)

        message_utf_8 = message.encode('utf-8')
        msg_len = len(message_utf_8)
        # print(msg_len)

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
            print(u'太长了')
        print(payload)

        if msg_len > 0:
            payload.extend(message_utf_8)
        if payload != None and len(payload) > 0:
            # print(payload)
            # 格式大概这样：bytearray(b'\x81\x0cHello World!')   '\x0c'是发送的数据长度
            conn.send(payload)

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
                g_code_length = 0
            else:
                message = self.conn.recv(128)
                print(type(message))
                self.buffer += message
                self.buffer_utf8 = self.parseData(self.buffer)          #str
                self.sendMessage(self.conn,self.buffer_utf8)
                print(message)
                self.buffer = bytes("",encoding="utf-8")


class websocketServer(object):
    def __init__(self,host, port):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)

    def server(self):
        print(self.serversocket)
        while True:
            conn,addr = self.serversocket.accept()
            # print(conn)
            # print(addr)
            # 新建线程
            newSocket = WebSocket(conn,addr)
            # 开始线程,执行run函数
            newSocket.start()


websocketServer = websocketServer("127.0.0.1",8000)
websocketServer.server()