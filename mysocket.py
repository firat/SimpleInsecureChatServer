import socket

MSG_LEN_DIGITS = 10

class ReadWriteSocket(object):
    def __init__(self, the_socket=None):
        if the_socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        else:
            self._socket = the_socket
    
    def __getattr__(self, name):
        return self._socket.__getattribute__(name)
    
    def write(self, msg):
        global MSG_LEN_DIGITS
        self._socket.send(("0" * (MSG_LEN_DIGITS - len(str(len(msg))))) + str(len(msg)))
        self._socket.send(msg)
    
    def readnext(self):
        global MSG_LEN_DIGIT
        l = self._socket.recv(MSG_LEN_DIGITS)
        if l == "":
            return ""
        return self._socket.recv(int(l))
        
    def accept(self, *args, **kwargs):
        s, a = self._socket.accept(*args, **kwargs)
        return (ReadWriteSocket(s), a)