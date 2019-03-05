import abc
import logging
import os
from collections import defaultdict


class ApplicationBackend:
    """Interface for registering and updating WebSocket clients."""
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.clients = defaultdict(list)

    def subscribe(self, client, room):
        """Subscribe websocket client to a specific room."""
        self.clients[room].append(client)        

    def unsubscribe(self, client, room):
        """Unsubscribe websocket client from a room."""
        if room in self.clients and client in self.clients[room]:
            self.clients[room].remove(client)

        if not self.clients[room]:
            del self.clients[room]

    def set_callback(self, f):
        """Callback function when message is received."""
        self.callback = f

    @abc.abstractmethod
    def start(self):
        """Maintains subscription in the background."""
        raise NotImplementedError()
