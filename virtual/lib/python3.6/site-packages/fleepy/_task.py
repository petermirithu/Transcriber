# -*- coding: utf-8 -*-
class Task(object):
    """Task management.

    .. note: This is listed under Conversation section in the API
    docs. However, as it has its own top-level handler (/api/task),
    we chose to split that up in Fleepy.

    https://fleep.io/fleepapi/ref-conversation.html#task-sync
    """
    def __init__(self, server, handler='task'):
        self._server = server
        self._handler = handler

    def sync(self, conversation_id, from_message_nr=None):
        """Sync all tasks into client.

        :param from_message_nr: Earliest message nr client has received.
        previous messages are read and returned
        :returns: Response data contains>

        header    dict    - `ConvInfo
        <https://fleep.io/fleepapi/ref-info.html#info-convinfo>`_ record
        stream    list    - see account/poll for stream record definitions

        """
        self._server.post(
            'task/sync/{}'.format(conversation_id),
            {'from_message_nr': from_message_nr})
