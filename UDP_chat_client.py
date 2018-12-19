# CLIENT
from socket import *
from threading import Thread
from random import randint

clientHost = gethostbyname(gethostname())
clientPort = randint(5001, 10000)
clientAddress = (clientHost, clientPort)
socket = socket(AF_INET, SOCK_DGRAM)
socket.bind(clientAddress)
server_address = (str(clientHost), 5000)


def listenForServer(msg_socket):
    while True:
        try:
            msg, user = msg_socket.recvfrom(4096)
            print(msg.decode('utf-8'))
        except:
            pass


t = Thread(target=listenForServer, args=(socket, ))
t.start()

socket.sendto("!join".encode('utf-8'), server_address)
print('Welcome to the chat!' + '( '+str(clientHost)+' Port: '+str(clientPort)+ ')')

while True:
    msg = input()
    if msg == '!quit':
        socket.sendto(msg.encode('utf-8'), server_address)
        break
    elif msg == '':
        continue
    else:
        msg = str(clientAddress)+ ': ' + msg
        socket.sendto(msg.encode('utf-8'), server_address)

socket.close()

