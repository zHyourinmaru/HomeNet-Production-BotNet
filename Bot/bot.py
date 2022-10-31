import socket
import systemRetrieval

PORT = 12000
CLIENT = socket.gethostbyname(socket.gethostname())
HEADER = 1024 # Messaggio di 1024 byte.
FORMAT = 'utf-8'
MASTER_ADDRESS = 'localhost'

class Bot:
    def __init__(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect((MASTER_ADDRESS, PORT))
        self.requestToServer()

    def requestToServer(self):

        inputSentence = systemRetrieval.systemInformation()
        #sentence = inputSentence._generalInformation
        sentence = inputSentence._bootInformation
        self.clientSocket.send(sentence.encode(FORMAT))

        #print('Data received from server: ', modifiedSentence.decode(FORMAT))
        #print('\n')
        #print(sentence)
        #print('\n')

        self.clientSocket.close()


if __name__ == '__main__':
    client = Bot()