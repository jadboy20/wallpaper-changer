import sys
import os
import socket
import pickle
from . import _SERVER_PORT



class Client(object):
    def __init__(self):
        pass

    def ping_server(self):
        """Use this function to check if the server is online or not.
        We do not want to create an instance of the server if it is already online.

        Return True if server is running. False if otherwise
        """
        running = True
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10.0)
                s.connect(('127.0.0.1', _SERVER_PORT))
                s.close()
        except (ConnectionRefusedError, socket.timeout):
            running = False

        return running

    def _send_message_with_response(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(5.0)
                s.connect(('127.0.0.1', _SERVER_PORT))
                if type(message) is bytes:
                    s.sendall(message)
                else:
                    s.sendall(message.encode('utf-8'))
                data = s.recv(1024)
                print("Got: {}".format(data))
                s.close()
        except (ConnectionRefusedError, socket.timeout):
            running = False

    def pickle_payload(self, command="PING", args=()):
        obj = {}
        obj['command'] = command
        obj['args'] = args
        return pickle.dumps(obj)

    def send_test(self):
        payload = self.pickle_payload(command="KILL")
        self._send_message_with_response(payload)

    def send_kill(self):
        payload = self.pickle_payload(command="KILL")
        self._send_message_with_response(payload)

    def send_reset_timer(self, duration):
        payload = self.pickle_payload(command="RSTTMR", args=(duration,))
        self._send_message_with_response(payload)

    def next_image(self):
        payload = self.pickle_payload(command="NXTIMG", args=(duration,))
        self._send_message_with_response(payload)


if __name__ == "__main__":
    Client().send_kill()
    # Client().send_reset_timer(5)



