#!/usr/bin/env python
import signal, socket, sys, select, time

from mysocket import ReadWriteSocket

MAX_SIZE_DIGITS = 10
    
def sock_msg(sock):
    global MAX_SIZE_DIGITS
    buff_size = int(sock.recv(MAX_SIZE_DIGITS))
    return sock.recv(buff_size)

class ChatServer():
    def __init__(self, port):
        self.clients = {}
        self.port = port
        self.server_socket = ReadWriteSocket()
        self.keep_running = False
    
    def start(self):
        self.server_socket.bind(('', self.port))
        self.server_socket.listen(5)
        print "Listening for connections..."
        self.keep_running = True
        sockets = [self.server_socket]
        nicknames = {}
        while self.keep_running:
            readable, writable, error = select.select(sockets, [], [])
            if len(readable) > 0:
                for sock in readable:
                    if sock is self.server_socket:
                        print "New client accepted."
                        (client_socket, address) = sock.accept()
                        sockets.append(client_socket)
                    else:
                        msg = sock.readnext()
                        if not sock in nicknames.keys():
                            if msg in nicknames.values():
                                sock.write("ERROR: Nickname already in use.")
                            else:
                                nicknames[sock] = msg
                                sock.write("SERVER: Welcome to chat!")
                        elif msg == "":
                            sock.close()
                            sockets.remove(sock)
                            print "Client disconnected."
                        else:
                            for client_socket in sockets:
                                if not client_socket is self.server_socket:
                                    client_socket.write("[%s]> %s" % (nicknames[sock], msg))
                            print msg
        for socket in sockets:
            socket.close()    
    def exit(self):
        self.keep_running = False



if __name__ == "__main__":
 server = ChatServer(8090)
 try:
     server.start()
 except KeyboardInterrupt:
     print "Exiting"
     server.exit()
     sys.exit(0)


