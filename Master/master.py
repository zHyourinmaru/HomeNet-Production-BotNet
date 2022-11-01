# Questo file rappresenta il server, il BotMaster.
import json
import socket
import pprint
pp = pprint.PrettyPrinter(indent=4)

PORT = 14000
SERVER = socket.gethostbyname(socket.gethostname())
HEADER = 2048 # Messaggio di 1024 byte.
FORMAT = 'utf-8'

class BotMaster:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM -> socket TCP.
        self.start()

    def __del__(self):
        self.serverSocket.close()

    def start(self):
        self.serverSocket.bind(('', PORT))
        self.serverSocket.listen()
        print('The server is ready to receive!')
        self.waitForClient()

    def waitForClient(self):
        while True:
            connection, addr = self.serverSocket.accept()
            print('The connection has been accepted! Client ip address: ', addr[0])
            sentence = connection.recv(HEADER).decode(FORMAT)
            dict = json.loads(sentence)
            pp.pprint(dict)

            with open('data.json','w') as fp:
                json.dump(dict, fp)

            connection.close()


if __name__ == '__main__':
    server = BotMaster()