# SERVER
from socket import *
from threading import Thread
from queue import Queue

serverHost = gethostbyname(gethostname())
serverPort = 5000
serverAddress = (serverHost, serverPort)
socket = socket(AF_INET, SOCK_DGRAM)
socket.bind(serverAddress)


def listenForClient(msg_socket, msgQ): # (socket, message queue)
    while True:
        msg, clientAdd = msg_socket.recvfrom(4096)
        msgQ.put((msg, clientAdd))


print('Server IP: '+ str(serverHost))
clients = set()
msgQ = Queue()

print('Server Ready')

t = Thread(target=listenForClient, args=(socket, msgQ))
t.start()

while True:
    while not msgQ.empty():
        msg, clientAdd = msgQ.get()
        if clientAdd not in clients:
            clients.add(clientAdd)
            joinMsg = (str(clientAdd) + ' has joined the chat')
            for client in clients:
                if client != clientAdd:
                    socket.sendto(joinMsg.encode('utf-8'), client)
            continue
        clients.add(clientAdd)
        msg = msg.decode('utf-8')
        if msg.endswith('!quit'):
            for client in clients:
                if client != clientAdd:
                    socket.sendto( (str(clientAdd) + " left the chat").encode('utf-8'), client)
            clients.remove(clientAdd)
            continue
        print(msg)
        for client in clients:
            if client != clientAdd:
                socket.sendto(msg.encode('utf-8'), client)
socket.close()
