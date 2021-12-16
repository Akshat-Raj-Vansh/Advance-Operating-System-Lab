import socket
import json
import _thread
import time
import random
import os
import tqdm
import threading
import os
import subprocess

BUFFER_SIZE = 5120
SEPARATOR = "<SEPARATOR>"


class Error:
    commandInputError = Exception("Please enter correct command")
    portInputError = Exception("Please enter correct port number")
    controllerError = Exception("Controller Error. Try After Sometime")
    createRoomError = Exception("Error in creating the room")


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.fileName = ""
        self.weight = ""

    def createSocket(self, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, port))
        return client

    def decode(self, value):
        return value.decode('ascii')

    def encode(self, value):
        return value.encode('ascii')

    def rec_file(self, file,):
        filesize = BUFFER_SIZE
        progress = tqdm.tqdm(range(
            filesize), f"Receiving {self.fileName}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(self.fileName, "wb") as f:
            f.write(self.encode(file))

        # update the progrclient, client_address bar
        # for i in range(filesize):
        #     progress.update(i)
        progress.update(filesize)

    def listen(self, client):
        while True:
            data = client.recv(BUFFER_SIZE)
            data = self.decode(data)
            message = data[:data.find('(')]
            if(message == "SEND"):
                fileName = data[data.find('(')+1:data.find(')')]
                print(fileName)
                self.send_file(fileName, client)
            if(message == "FILE"):
                file = data[data.find('(')+1:data.find(')')]
                print(file)
                self.rec_file(file)

        client.close()
        exit(0)

    def send_file(self, filename, client):
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        # start sending the file
        progress = tqdm.tqdm(range(
            filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                client.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    def send(self, client):
        while True:
            message = input("")
            if(message[:message.find("(")] == "REQUEST"):
                self.fileName = message[message.find("(")+1:message.find(")")]
                client.send(self.encode(message))

        client.send(self.encode(message))
        client.close()
        exit(0)

    def start(self):
        client = self.createSocket(self.port)
        cmd = subprocess.Popen("ls",
                               shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte, "utf-8")
        currentWD = os.getcwd() + "> "
        client.send(self.encode("F({})".format(output_str + currentWD)))
    # _thread.start_new_thread(self.send, (client,))
        _thread.start_new_thread(self.send, (client,))
        _thread.start_new_thread(self.listen, (client,))
        while True:
            continue


if __name__ == '__main__':
    client = Client('192.168.77.151', 1234)
    client.start()
