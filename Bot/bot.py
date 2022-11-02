import socket
import systemRetrieval
from time import sleep
import json


PORT = 14000
CLIENT = socket.gethostbyname(socket.gethostname())
HEADER = 2048 # Messaggio di 1024 byte.
FORMAT = 'utf-8'
MASTER_ADDRESS = 'localhost'

class Bot:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.clientSocket.connect((MASTER_ADDRESS, PORT))
        while self.clientSocket.connect_ex((MASTER_ADDRESS, PORT)) != 0:
            sleep(10)
        self.requestToServer()

    def requestToServer(self):
        inputSentence = systemRetrieval.SystemInformation()
        print(inputSentence.data)
        sentence = json.dumps(inputSentence.data)
        self.clientSocket.send(sentence.encode(FORMAT))

        self.clientSocket.close()


if __name__ == '__main__':
    client = Bot()