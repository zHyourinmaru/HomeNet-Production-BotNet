
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
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM indica l'utilizzo di una socket TCP.
        self.start()

    def __del__(self):
        self.serverSocket.close()

    def start(self):
        """
        Procedura tramite la quale il server, una volta attivato, resta in attesa di connessione con il client.
        :return: None
        """
        self.serverSocket.bind(('', PORT))
        self.serverSocket.listen()
        print('The server is ready to receive!')
        self.waitForClient()

    def waitForClient(self):
        """
        Procedura tramite la quale il server accetta la richiesta di connessione del client e salva i dati ricevuti in un file .json.
        :return: None
        """
        while True:
            connection, addr = self.serverSocket.accept()
            print('The connection has been accepted! Client ip address: ', addr[0])

            # Il client invia al server la dimensione dei dati raccolti ( da sostituire poi al parametro HEADER per la recv() ).
            data_dim = 0
            while data_dim == 0:
                data_dim = int(connection.recv(1024).decode(FORMAT))

            # Il server manderà una riposta del tipo 'ok' al client per confermare la corretta ricevuta della dimensione dei dati.
            message_received = 'ok'
            # Comunica direttamente sulla socket del client e non tramite la sua.
            connection.send(message_received.encode(FORMAT))

            print("Header dimension received: ", data_dim)

            data = connection.recv(data_dim).decode(FORMAT)
            dict = json.loads(data)
            pp.pprint(dict) # Stampa di ciò che verrà riportato nel file .json

            with open('data.json', 'w') as fp:
                json.dump(dict, fp, indent=4)

            connection.close()


if __name__ == '__main__':
    server = BotMaster()
