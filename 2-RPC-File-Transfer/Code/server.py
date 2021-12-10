import socket as socket
import _thread
import threading
import random
import os
import tqdm
from time import sleep
import time
from client import Client


SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024 * 4  # 4KB


class Server:
    def __init__(self, port, n, host=""):
        self.host = host
        self.port = port
        self.connection = []
        self.clients = []
        self.weight = 1

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # loop through n times
        for i in range(n):
            self.clients.append(Client('127.0.0.1', self.port, i+1))

    def configure(self):
        try:
            self.server.bind((self.host, self.port))
            print("Server binded to port", self.port)
            self.server.listen(5)
            print("Server is listening")
        except Exception as e:
            print(e)

    def connect_clients(self):
        time.sleep(3)
        for i in range(len(self.clients)):
            print("Connecting to client {}".format(i+1))
            _thread.start_new_thread(self.clients[i].start, ())

    def decode(self, value):
        return value.decode('ascii')

    def encode(self, value):
        return value.encode('ascii')

    def send_file(filename, host, port):
        # get the file size
        filesize = os.path.getsize(filename)
        # create the client socket
        s = socket.socket()
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")

        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

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
                s.sendall(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

        # close the socket
        s.close()

    def listen(self, client, i):
        while True:
            data = client.recv(1024)
            data = self.decode(data)
            message = data[:data.find('(')]
            if(message == "C"):
                self.weight += float(data[data.find('(')+1:data.find(')')])
                print("{} Weight released by process {}".format(
                    data[data.find('(')+1:data.find(')')], i),)
                print("Process {} terminated".format(i))

    def threaded(self, client, client_addr):
        while True:
            if(self.weight > .2):
                i = random.randint(0, len(self.clients)-1)
                # print i and len of self.connection
                if(i < len(self.connection) and client == self.connection[i]):
                    rweight = random.random() * (self.weight-.1)
                    client.send(self.encode("B({})".format(str(rweight))))
                    self.weight -= rweight
                    _thread.start_new_thread(self.listen, (client, i))
                else:
                    time.sleep(1)
        client.close()

    def start(self):
        self.configure()
        _thread.start_new_thread(self.connect_clients, ())
        while True:
            client, client_addr = self.server.accept()
            self.connection.append(client)
            print('Connected to :', client_addr[0], ':', client_addr[1])

            _thread.start_new_thread(
                self.threaded, (client, client_addr))


if __name__ == '__main__':
    server = Server(1237, 10)
    server.start()
