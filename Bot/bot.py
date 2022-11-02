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

class Bot:
    def __init__(self):
        self.sentence = ''
        self.data_dim = 0
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_data = threading.Thread(target=self.dataScavange)
        self.thread_connection = threading.Thread(target=self.waitForConnection)
        self.thread_data.start()
        self.thread_connection.start()

    def waitForConnection(self):
        while self.clientSocket.connect_ex((MASTER_ADDRESS, PORT)) != 0:
            sleep(2)

        while self.thread_data.is_alive():
            sleep(2)

        self.sendHeaderDim()

        # aspettare che il server risponde con ok della dimensione
        first_response = ''
        while first_response != 'ok':
            first_response = self.clientSocket.recv(1024).decode(FORMAT)

        # inviare i dati raccolti in formato json
        self.sendToServer()

    def dataScavange(self):
        inputSentence = systemRetrieval.SystemInformation()
        self.sentence = json.dumps(inputSentence.data)
        self.data_dim = sys.getsizeof(self.sentence.encode(FORMAT))
        print("thread_data terminated.")

    def sendHeaderDim(self):
        self.clientSocket.send(str(self.data_dim).encode(FORMAT))

    def sendToServer(self):
        print("Data dimension in bytes: ", self.data_dim)
        self.clientSocket.send(self.sentence.encode(FORMAT))
        self.clientSocket.close()


if __name__ == '__main__':
    client = Bot()