# Questo file rappresenta il server, il BotMaster.
import json
import socket
import pprint

pp = pprint.PrettyPrinter(indent=4)

PORT = 14000
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'


class BotMaster:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM -> socket TCP.
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
            data_dim = 0
            while data_dim == 0:
                data_dim = int(connection.recv(1024).decode(FORMAT))

            # il server ora deve dire ok al client della ricevuta della dimensione
            message_received = 'ok'
            connection.send(message_received.encode(FORMAT)) # il server comunica direttamente sulla socket del client e non tramite la sua

            print("Header dimension received: ", data_dim)

            data = connection.recv(data_dim).decode(FORMAT)
            dict = json.loads(data)
            pp.pprint(dict)

            with open('data.json', 'w') as fp:
                json.dump(dict, fp, indent=4)

            connection.close()


if __name__ == '__main__':
    server = BotMaster()
