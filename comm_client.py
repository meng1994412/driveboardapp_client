import socket
import time
from data import *

path = "{}".format(path)
print(type(path))

# PORT
PORT = 65434

# create TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
# ip_address = socket.gethostbyname(local_hostname)

# using ethernet address for connection
ip_address = "192.168.1.49"
# ip_address = "127.0.0.1"

# bind the socket to the port 65431
server_address = (ip_address, PORT)
s.connect(server_address)
print("connecting to {} ({}) with {}".format(local_hostname, local_fqdn, ip_address))

# send data to server
# s.sendall(path.encode("utf-8"))
s.send(path.encode("utf-8"))

# wait for two seconds
time.sleep(2)

# close connection
s.close()
