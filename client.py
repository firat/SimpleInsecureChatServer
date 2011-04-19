#!/usr/bin/env python
import select, socket, sys, threading, time

from mysocket import ReadWriteSocket


class ChatClient():
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.keep_running = False
        self.sock = None
        
    def connect(self):
        self.sock = ReadWriteSocket()
        self.sock.connect((self.server, self.port))
        self.keep_running = True
        initialized = False
        prompt = "Enter a nickname: "
        nickname = None
        print prompt
        
        while self.keep_running and nickname is None:
            nickname = sys.stdin.readline().strip()
            self.sock.write(nickname)
            reply = self.sock.readnext()
            print reply
            if not reply.startswith("ERROR"):
                break
        
        threading.Thread(target=self.server_handler).start()
        while self.keep_running:
            sys.stdout.write(">")
            msg = sys.stdin.readline().strip()
            if msg != "":
                self.sock.write(msg)

    def server_handler(self):
        while self.keep_running:
            readables, writables, error = select.select([self.sock], [], [], 1)
            for s in readables:
                print s.readnext()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: client.py <hostname> <port>"
        exit(1)
    else:
        cc = ChatClient(sys.argv[1], int(sys.argv[2]))
        try:
            cc.connect()
        except KeyboardInterrupt:
            print 4
            cc.keep_running = False
