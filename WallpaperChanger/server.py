import sys
import multiprocessing
import socket
import os
import select
from queue import Queue, Empty
import pickle
from . import config, _SERVER_PORT, _SERVER_MAX_CONN
from . import client
from . import wallpaper
import logging
import time



# We put the server module in the same directory as the wallpaper changer as it requires modules such as config.


class Server(object):
    def __init__(self, args):
        self._sock = None
        self.address = ("", _SERVER_PORT)
        self._inputs = []
        self._outputs = []
        self._message_queues = {}
        self._exit = False
        self._duration = 10
        self.timeout = self.get_timeout(10)

        self._callbacks = {
            'KILL': self.callback_kill,
            'RSTTMR': self.callback_reset_timer
        }
        self.wp = wallpaper.Wallpaper(args)

    def check_timer(self, timer):
        if time.time() > timer:
            return True
        return False

    def get_timeout(self, duration):
        return time.time() + duration


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

                        response = "OK"
                        payload = self.unjar_payload(data)

                        command = payload['command']

                        if command in self._callbacks:
                            resp = self._callbacks[command](*payload['args'])
                            if resp is not None:
                                response = resp
                        else:
                            response = "ERROR"

                        # Add output channel for response
                        if s not in self._outputs:
                            self._outputs.append(s)

                        self._message_queues[s].put(response.encode('utf-8'))

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
                    s.sendall(next_msg)

                    if self._exit:
                        # Exit the app.
                        sys.exit(0)

            for s in exception:
                print("Handling exception condition for {}".format(s.getpeername()))
                self._inputs.remove(s)
                if s in self._outputs:
                    self._outputs.remove(s)
                s.close()

                # Remove message queue
                del self._message_queues[s]

            if self.check_timer(self.timeout):
                self.timer_callback()
                self.timeout = self.get_timeout(10)

        logging.info("Exiting app")

    def unjar_payload(self, payload):
        return pickle.loads(payload)

    def callback_kill(self, *args):
        logging.info("Got Kill Command. Good bye!")
        self._exit = True

    def timer_callback(self):
        print("Changing image")
        self.wp.next_image()

    def callback_reset_timer(self, *args):
        # If args is nothing, then we will not change the time.
        print(args)
        if (len(args) == 0) and (args[0] is not int):
            return
        else:
            self.timer_callback()
            self.timeout = self.get_timeout(args[0])
            return "OK"

def main(args):
    # We will want to spawn this as a daemon.
    if client.Client().ping_server() is False:

        Server(args).run()
    else:
        print("Service of server is running.")


if __name__ == "__main__":
    main()
