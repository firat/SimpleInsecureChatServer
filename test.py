#! /usr/bin/env python
import socket, select, threading, sys

def test_func():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        select.select([s], [], [], 1)
        print "Hello"

if __name__ == "__main__":
    # threading.Thread(target=test_func).start()
    sys.stdout.write("1")
    sys.stdout.write("\r")
    sys.stdout.write("2\n")