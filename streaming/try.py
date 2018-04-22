import socket
import time

server = 'localhost'
port = 40123
message = 'This is a test data.'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))
s.listen(1)

try:
    while True:
        conn, addr = s.accept()
        try:
            i = 0
            while i<100:
                conn.send(b'100')
                print('one data sent')
                i += 1
                time.sleep(2)
            conn.close()
        except socket.error:
            print("socket error")
            pass
        conn.close()
finally:
    s.close()