#!/usr/bin/env python
import select, socket, sys, threading

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
        
        readables = [self.sock, sys.stdin]
        while self.keep_running:
            readable, writeable, error = select.select(readables, [], [])
            for r in readable:
                if r is sys.stdin:
                    msg = r.readline().strip()
                    if not initialized:
                        nickname = msg
                        readables.remove(sys.stdin)
                    else:
                        print prompt
                    self.sock.write(msg)
                elif r is self.sock:
                    msg = r.readnext()
                    if not initialized and not msg.startswith("ERROR"):
                        prompt = "[%s]> " % nickname
                        initialized = True
                        readables.append(sys.stdin)
                    else:
                        print msg
                else:
                    import ipdb; ipdb.set_trace()
                    raise Exception("I have no idea what this readable socket is.")
        self.sock.close()


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
