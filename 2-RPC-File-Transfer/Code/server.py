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
BUFFER_SIZE = 1024 * 5  # 4KB


class Server:
    def __init__(self, port, host=""):
        self.host = host
        self.port = port
        self.files = {}
        self.connection = []

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def configure(self):
        try:
            self.server.bind((self.host, self.port))
            print("Server binded to port", self.port)
            self.server.listen(5)
            print("Server is listening")
        except Exception as e:
            print(e)

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

    def find(self, filename):
        return self.files[filename]

    def connect(self, sender, reciever):
        file = self.rec_file(sender)
        print(file)
        reciever.sendall(self.encode("FILE({})".format(file)))

    def rec_file(self, sender):
        print("[+] Waiting for file...")
        bytes_read = self.decode(sender.recv(BUFFER_SIZE))
        print("[+] File received.")
        return bytes_read

    def listen(self, client, client_addr):
        while True:
            data = client.recv(BUFFER_SIZE)
            data = self.decode(data)
            message = data[:data.find('(')]
            if(message == "F"):
                file = data[data.find('(')+1:data.find(')')]
                for f in file.split("\n"):
                    print(f)
                    self.files[f] = client
            if message == "REQUEST":
                filename = data[data.find('(')+1:data.find(')')]
                filesize = os.path.getsize(filename)
                sender = self.find(filename)
                sender.send(self.encode("SEND({})".format(filename)))
                _thread.start_new_thread(self.connect, (sender, client))

    def threaded(self, client, client_addr):
        _thread.start_new_thread(self.listen, (client, client_addr))
        while True:
            continue

    def start(self):
        self.configure()
        while True:
            client, client_addr = self.server.accept()
            self.connection.append(client)
            print('Connected to :', client_addr[0], ':', client_addr[1])

            _thread.start_new_thread(
                self.threaded, (client, client_addr[1]))


if __name__ == '__main__':
    server = Server(1237, host="172.28.227.151")
    server.start()
