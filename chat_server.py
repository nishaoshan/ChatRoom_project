"""
author : Nishaoshan
email:790016602@qq.com
time:2020-6-21
env : Python3
socket,Thread,聊天室服务端
"""
from socket import *
from threading import Thread


class Server:
    def __init__(self, host="0.0.0.0", port=9999):
        self.ADDR = (host, port)
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(self.ADDR)
        self.name_dict = {}

    def start(self):
        while True:
            msg, addr = self.sock.recvfrom(1024)
            head_msg = msg.decode().split(" ", 2)[0]
            name = msg.decode().split(" ", 2)[1]
            if head_msg == "L":
                if name in self.name_dict:
                    self.sock.sendto(b"no", addr)
                    continue
                for address in self.name_dict.values():
                    self.sock.sendto(f"欢迎{name}进入聊天室".encode(), address)
                self.name_dict[name] = addr
                self.sock.sendto(b"ok", addr)
            elif head_msg == "C":
                content = msg.decode().split(" ", 2)[2]
                for n, a in self.name_dict.items():
                    if n != name:
                        self.sock.sendto(f"{name}:{content}".encode(), a)
            elif head_msg == "q":
                del self.name_dict[name]
                for address in self.name_dict.values():
                    self.sock.sendto(f"{name}已退出聊天室".encode(), address)


if __name__ == '__main__':
    Server().start()
