from collections import deque

send = deque()
send.append(("a","b"))
print(send)
send.append(("b","ba"))
print(send)
print(send[0])
print(send[0][1])
print(send[1].count("b"))
x = send.popleft()
print(x,send)
print(len(send))