import socket
import json
import _thread
import time
import random
import os
import tqdm
import threading

BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

class Error:
    commandInputError = Exception("Please enter correct command")
    portInputError = Exception("Please enter correct port number")
    controllerError = Exception("Controller Error. Try After Sometime")
    createRoomError = Exception("Error in creating the room")


class Client:
    def __init__(self, host, port, id):
        self.id = id
        self.host = host
        self.port = port
        self.connections = []
        self.weight = ""

    def createSocket(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, port))
        return client

    def decode(self, value):
        return value.decode('ascii')

    def encode(self, value):
        return value.encode('ascii')
    
    def rec_file(self, client):
        received = client.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer
        filesize = int(filesize)
        # start receiving the file from the socket
        # and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
            # write to the file the bytes we just received
            f.write(bytes_read)
            # update the progress bar
        progress.update(len(bytes_read))

    def listen(self, client):
        while True:
            data = client.recv(1024)
            data = self.decode(data)
            message = data[:data.find('(')]
            if(message == "B"):
                self.weight = data[data.find('(')+1:data.find(')')]
                print("Assigned Weight to Process {} is: {}".format(
                    self.id, self.weight))
                time.sleep(random.randint(1, 20))
                client.send(self.encode("C({})".format(self.weight)))
        client.close()
        exit(0)

    def start(self):
        client = self.createSocket(self.port)
    # _thread.start_new_thread(self.send, (client,))
        _thread.start_new_thread(self.listen, (client,))
        while True:
            continue
