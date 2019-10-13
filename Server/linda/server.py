import atexit
import threading

from linda.utils import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from _thread import *
from time import sleep

class ServerThread(Thread):
    def __init__(self, HOST, PORT):
        Thread.__init__(self)
        self.sck = socket(AF_INET, SOCK_STREAM) 
        self.sck.settimeout(None)
        self.sck.bind((HOST, PORT))  #-
        self.conn = None
        self.addr = None
        self.dictionary = {}
        self.locker = threading.Lock()

    def exit_handler():
        print("Servidor encerrado")
        if self.conn:
            self.conn.close()               
        self.join()

    
    def threaded(self,conn):
        while True:
            data = conn.recv(1024)
            if not data: break
            matches = bin_to_tuple(data)
            for match in matches:
                if match[0] == "out":
                    self.response_out((match[1], match[2], match[3]))
                elif match[0] == "rd":
                    self.response_rd(conn,(match[1], match[2], match[3]))
                elif match[0] == "in":
                    self.response_in(conn,(match[1], match[2], match[3]))
        conn.close()
        print("Thread encerrado para cliente\nConexão com o cliente encerrada")

    def run(self):
        atexit.register(self.exit_handler)
        while True:
            self.sck.listen(1)
            (self.conn, self.addr) = self.sck.accept()
            print("Cliente conectado")
            start_new_thread(self.threaded, (self.conn,)) 
            print("Thread criada para o cliente")

    def response_out(self, tuple):
        self.locker.acquire()
        (publisher, topic, content) = tuple
        if topic not in self.dictionary.keys():
            self.dictionary[topic] = []
        self.dictionary[topic].append((publisher, content))
        self.locker.release()

    def response_rd(self, conn,match):
        self.locker.acquire()
        publisher = match[0]
        topic = match[1]
        tuples_to_send = []
        while(True):
            if topic in self.dictionary:
                for tpl in self.dictionary[topic]:
                    if tpl[0] == publisher:
                        tuples_to_send.append((tpl[0],topic,tpl[1]))
            if(len(tuples_to_send) != 0):
                break
            else:
                self.locker.release()
                sleep(5)
                self.locker.acquire()
                
        list_as_bin = list_to_bin(tuples_to_send)
        conn.send(list_as_bin)
        conn.send(".".encode())
        self.locker.release()
    
    def response_in(self, conn,match):
        self.locker.acquire()
        publisher = match[0]
        topic = match[1]
        content = match[2]
        tuples = []
        found = False
        while(not found):
            if topic in self.dictionary:
                topic_vector = self.dictionary[topic]
                for x in range(len(topic_vector)):
                    if topic_vector[x] == (publisher,content):
                        del(topic_vector[x])
                        found = True
                        if(len(topic_vector) == 0):
                            del(self.dictionary[topic])
                        else:
                            self.dictionary[topic]=topic_vector
                        break
            if(not found):
                self.locker.release()
                sleep(6)
                self.locker.acquire()
        self.locker.release()

def create_server(HOST=None, PORT=None):
    print("Servidor iniciado")
    server_thread = ServerThread(HOST=HOST, PORT=PORT)
    server_thread.start()
