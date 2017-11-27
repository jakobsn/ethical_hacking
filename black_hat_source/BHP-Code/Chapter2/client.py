import socket
from time import sleep
target_host = "0.0.0.0"
target_port = 9999
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client
client.connect((target_host, target_port))
sleep(10)
# send some data
client.send("ABCDEF")
# receive some data
response = client.recv(4096)
print response
