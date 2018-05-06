import socket
import time


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('db', 3306)


print('block terminal while mysql server is down')
while 1:
    try:
        sock.connect(server_address)
    except socket.error:
        time.sleep(1)
    else:
        print('done')
        break
