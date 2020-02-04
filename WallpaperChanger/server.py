import sys
import multiprocessing
import socket
import os
import select
from queue import Queue, Empty
import pickle
from . import config, _SERVER_PORT, _SERVER_MAX_CONN
from . import client




# We put the server module in the same directory as the wallpaper changer as it requires modules such as config.


class Server(object):
    def __init__(self):
        self._sock = None
        self.address = ("", _SERVER_PORT)
        self._inputs = []
        self._outputs = []
        self._message_queues = {}

    def bind(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.setblocking(0)
        self._sock.bind(self.address)

    def listen(self):
        self._sock.listen(_SERVER_MAX_CONN)
        self._inputs.append(self._sock)

    def run(self):
        self.bind()
        self.listen()

        while self._inputs:
            readable, writable, exception = select.select(
                self._inputs, self._outputs, self._inputs, 0.5)

            # Handle self._inputs
            for s in readable:
                if s is self._sock:
                    # A "readable" server socket is ready to accept a connection.
                    connection, client_address = s.accept()
                    print("A new connection from {}".format(client_address))
                    connection.setblocking(0)
                    self._inputs.append(connection)

                    # Give the connection a queue for data we want to send.
                    self._message_queues[connection] = Queue()
                else:
                    data = s.recv(1024)
                    if data:
                        # A readable client socket has data
                        print("Received {} from {}".format(
                            data, s.getpeername()))
                        self._message_queues[s].put(data)

                        payload = self.unjar_payload(data)

                        # Add output channel for response
                        if s not in self._outputs:
                            self._outputs.append(s)
                    else:
                        # Interpret empty result as closed connection
                        print("Closing {}".format(s.getpeername()))
                        if s in self._outputs:
                            self._outputs.remove(s)
                        self._inputs.remove(s)
                        s.close()

                        # Remove message queue
                        del self._message_queues[s]

            # Handle writable
            for s in writable:
                try:
                    next_msg = self._message_queues[s].get_nowait()
                except Empty:
                    # No messages
                    print("Output queue for {}".format(s.getpeername()))
                    self._outputs.remove(s)
                else:
                    print("Sending {} to {}".format(next_msg, s.getpeername()))
                    s.send(next_msg)

            for s in exception:
                print("Handling exception condition for {}".format(s.getpeername()))
                self._inputs.remove(s)
                if s in self._outputs:
                    self._outputs.remove(s)
                s.close()

                # Remove message queue
                del self._message_queues[s]

    def unjar_payload(self, payload):
        return pickle.loads(payload)



def main():
    if client.Client().ping_server() is False:
        Server().run()
    else:
        print("Service of server is running.")


if __name__ == "__main__":
    main()
