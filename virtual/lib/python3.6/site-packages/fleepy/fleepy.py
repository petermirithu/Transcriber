# -*- coding: utf-8 -*-
from __future__ import absolute_import

from fleepy._task import Task
from fleepy._info import Info
from fleepy._file import File
from fleepy._alias import Alias
from fleepy._avatar import Avatar
from fleepy._server import Server
from fleepy._search import Search
from fleepy._account import Account
from fleepy._contact import Contact
from fleepy._message import Message
from fleepy._conversation import Conversation


class Fleepy(object):
    """A simple consumer for Fleepy API using.

    You can find detailed documentation about the API here:
    https://fleep.io/fleepapi/reference.html
    """
    def __init__(self, url='https://fleep.io/api/', **kwargs):
        """
        Defaults to https://fleep.io/api.
        """
        self._url = url
        self._compress = kwargs.get('compress', False)
        self._server = kwargs.get('server', Server(self._url))
        self._initialize_handlers()

    def _initialize_handlers(self):
        """Initialize the classes responsible for the top
        level handlers.
        """
        self.conversation = Conversation(self._server)
        self.task = Task(self._server)
        self.avatar = Avatar(self._server)
        self.account = Account(self._server)
        self.message = Message(self._server)
        self.info = Info(self._server)
        self.contact = Contact(self._server)
        self.file = File(self._server)
        self.alias = Alias(self._server)
        self.search = Search(self._server)

    def hangout(self, hangout_id, hangout_url, participants):
        """Handle heartbeat from hangout app.

        :param hangout_id: google_key.
        :param hangout_url: Hangout url.
        :param participants: List of participants.
        """
        data = {
            'hangout_id': hangout_id,
            'hangout_url': hangout_url,
            'participants': participants}
        return self._server.post('hangout', data)

    def classificators(self):
        """Returns classificators for current acount.
        """
        return self._server.post('classificators')
