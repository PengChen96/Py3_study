
import socket
import base64,hashlib

HANDSHAKE_STR = (
   "HTTP/1.1 101 Switching Protocols\r\n"
   "Upgrade: WebSocket\r\n"
   "Connection: Upgrade\r\n"
   "Sec-WebSocket-Accept: %(token)s\r\n\r\n"
)
GUID_STR = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'

class WebSocket(object):
    def __init__(self,host,port,path="/"):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((host, port))
        self.serversocket.listen(5)
        self.listeners = [self.serversocket]

        self.buffer = ""
        self.path = path

    def handShakeData(self,c_req):
        sec_key = self.parseHeaders(c_req)['Sec-WebSocket-Key']
        key = sec_key.encode("ascii") + GUID_STR.encode("ascii")
        accept_token = base64.b64encode(hashlib.sha1(key).digest()).decode("ascii")
        s_res = HANDSHAKE_STR % {'token': accept_token}
        return s_res

    def parseHeaders(self,msg):
        print(msg)
        headers = {}
        msg = str(msg,encoding="utf-8")
        header,data = msg.split('\r\n\r\n',1)
        for x in header.split("\r\n")[1:]:
            #这里是 “:+space”
            key,value = x.split(": ",1)
            headers[key] = value
        return headers

    def run(self):
        print(self.listeners)
        while True:
            for listen in self.listeners:
                conn,addr = listen.accept()
                c_req = conn.recv(1024)
                handData = self.handShakeData(c_req)
                conn.sendall(str.encode(handData))



websocket = WebSocket("127.0.0.1",8000)
websocket.run()