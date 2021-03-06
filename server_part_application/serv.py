#!/usr/bin/env python

import select
import socket
import sys
import threading
import signal
import random
from time import sleep

PORT = 59481
HOST = '127.0.0.1'
BACKLOG = 5
BUFF = 2048


class Server:
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.conn = (self.host, self.port)
        self.backlog = BACKLOG
        self.server = None
        self.threads = []
        self.clients = []

    def register_signals(self):
        signal.signal(signal.SIGHUP, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGQUIT, self.signal_handler)

    def open_socket(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(self.conn)
            self.server.listen(self.backlog)
            print("Started server: " + str(self.host) + " on port: " + str(self.port))
            print("Listening for incoming connections...")
        except socket.error as message:
            if self.server:
                self.server.close()
            print >> sys.stderr, "Could not open socket: " + str(message)
            sys.exit(1)
        self.register_signals()

    def signal_handler(self, signum, frame):
        print("Caught signal: ", signum)
        print("Closing the socket and cleaning up the mess...")
        self.server_shutdown()

    def server_shutdown(self):
        self.running = 0
        for c in self.threads:
            try:
                c.join()
            except RuntimeError:
                pass
        if self.server:
            self.server.close()
        sys.exit(1)

    def run(self):
        self.open_socket()
        inputs = [self.server, sys.stdin]
        self.running = 1
        while self.running:
            try:
                iready, oready, eready = select.select(inputs, [], [])
            except :
                self.running = 0
                pass
            for s in iready:
                if s == self.server:
                    try:
                        c = Client(self, self.server.accept())
                        c.start()
                        self.threads.append(c)
                    except :
                        pass

                elif s == sys.stdin:
                    junk = sys.stdin.readline()
                    self.running = 0

                else:
                    self.running = 0

        # close all threads
        print('Closing....')
        for c in self.threads:
            c.join()
        self.server_shutdown()


class Client(threading.Thread):
    def __init__(self, server, client, address):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.server = server

    def run(self):
        print
        "Incoming connection from : " + str(self.address)
        running = 1
        while running:
            data = self.client.recv(BUFF)
            if data:
                if data == 'Hello':
                    self.client.send("Hello back")

                elif data == 'Test':
                    num_1 = str(random.randint(1, 99999))
                    num_2 = str(random.randint(1, 99)).rjust(2, '0')
                    unit = random.choice(['mW', 'W', 'KW', 'MW']);
                    full = "|".join([num_1, num_2, unit])
                    self.client.send(full)

                elif data == 'get':
                    # full = "empty";
                    # self.client.send(full)
                    readings = [];

                    for x in range(0, 40):
                        num_1_voltage = str(random.randint(1, 99999))
                        num_2_voltage = str(random.randint(1, 99)).rjust(2, '0')
                        unit_voltage = random.choice(['mV', 'V', 'KV', 'MV'])
                        full_voltage = ",".join([num_1_voltage, num_2_voltage, unit_voltage])

                        num_1_current = str(random.randint(1, 99999))
                        num_2_current = str(random.randint(1, 99)).rjust(2, '0')
                        unit_current = random.choice(['mA', 'A', 'KA', 'MA'])
                        full_current = ",".join([num_1_current, num_2_current, unit_current])

                        num_1_power = str(random.randint(1, 99999))
                        num_2_power = str(random.randint(1, 99)).rjust(2, '0')
                        unit_power = random.choice(['mW', 'W', 'KW', 'MW'])
                        full_power = ",".join([num_1_power, num_2_power, unit_power])

                        full_reading = "&".join([full_voltage, full_current, full_power])
                        readings.append(full_reading)

                    full_readings = "~".join(readings)
                    full = str(len(readings)) + "|" + full_readings;
                    self.client.send(full)

                elif data == 'Done':
                    self.server.server_shutdown()
                    running = 0
            else:
                running = 0

        self.client.close()

    def __repr__(self):
        return str(self.address)


if __name__ == "__main__":
    s = Server()
    s.run()