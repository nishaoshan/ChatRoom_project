"""
author : Nishaoshan
email:790016602@qq.com
time:2020-6-21
env : Python3
socket,Thread,聊天室客户端
"""
import sys
from socket import *
from threading import Thread


class Client:
    def __init__(self, host="127.0.0.1", port=9999):
        self.host = host
        self.port = port
        self.ADDR = (self.host, self.port)
        self.name = ""
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.connect((self.host, self.port))

    def start(self):
        self.login()
        t = Thread(target=self.recv_msg)
        t.daemon = True
        t.start()
        self.send_msg()
        self.quit()

    def login(self):
        while True:
            try:
                name = input("请输入用户名：")
            except KeyboardInterrupt:
                sys.exit("您已退出")
            if not name:
                print("输入有误，请重新输入：")
            self.name = name
            msg = "L " + name
            self.sock.sendto(msg.encode(), self.ADDR)
            msg, addr = self.sock.recvfrom(1024)
            if msg == b"ok":
                print("进入聊天室")
                return
            else:
                print("用户名已存在")

    def recv_msg(self):
        while True:
            msg, addr = self.sock.recvfrom(1024)
            print("\n%s\n" % msg.decode())

    def send_msg(self):
        while True:
            try:
                msg = input("发言：")
            except KeyboardInterrupt:
                self.sock.sendto(f"q {self.name}".encode(), self.ADDR)
                return
            if not msg:
                self.sock.sendto(f"q {self.name}".encode(), self.ADDR)
                return
            message = "C " + self.name + " " + msg
            self.sock.sendto(message.encode(), self.ADDR)

    def quit(self):
        self.sock.close()


if __name__ == '__main__':
    Client().start()
