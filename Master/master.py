# Questo file rappresenta il server, il BotMaster.

import socket

PORT = 13000
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 1024 # Messaggio di 1024 byte.
FORMAT = 'utf-8'

class BotMaster:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> socket TCP.
        self.start()

    def __del__(self):
        print("BOTMASTER destructed")
        self.serverSocket.close()

    def start(self):
        self.serverSocket.bind(('', PORT))
        self.serverSocket.listen()
        print('The server is ready to receive!')
        self.waitForClient()

    def waitForClient(self):
        while True:
            connection, addr = self.serverSocket.accept()
            print('The connection has been accepted! \nClient ip address: ', addr[0])
            sentence = connection.recv(HEADER).decode(FORMAT)
            print('\n')
            print(sentence)
            print('\n')
            #capitalizedSentence = sentence.upper()
            #connection.send(capitalizedSentence.encode(FORMAT))
            connection.close()


if __name__ == '__main__':
    server = BotMaster()