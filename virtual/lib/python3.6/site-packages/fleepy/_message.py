# -*- coding: utf-8 -*-
class Message(object):
    """
    """
    def __init__(self, server, handler='message'):
        self._server = server
        self._handler = handler

    def copy(self, conversation_id, message_nr,
             to_conv_id, from_message_nr=None):
        """Copy message from another chat.
        """
        data = {
            'message_nr': message_nr,
            'to_conv_id': to_conv_id,
            'from_message_nr': from_message_nr}
        return self._server.post("message/copy/{}".format(
            conversation_id), data)

    def delete(self, conversation_id, message_nr,
               attachment_id=None, from_message_nr=None):
        """Send message to flow.
        """
        data = {
            'message_nr': message_nr,
            'attachment_id': attachment_id,
            'from_message_nr': from_message_nr}
        return self._server.post("message/delete/{}".format(
            conversation_id), data)

    def edit(self, conversation_id, message, message_nr,
             from_message_nr=None, attachments=None):
        """Send message to flow.
        """
        data = {
            'message': message,
            'message_nr': message_nr,
            'attachments': attachments,
            'from_message_nr': from_message_nr}
        return self._server.post("message/edit/{}".format(
            conversation_id), data)

    def _mark(self, mark_type, conversation_id, message_nr, from_message_nr):
        data = {'message_nr': message_nr, 'from_message_nr': from_message_nr}
        return self._server.post(
            'message/mark_{}/{}'.format(mark_type, conversation_id), data)

    def mark_read(self, conversation_id, message_nr, from_message_nr=None):
        """Set conversation read horizon for this account. Used when client
        determines that it has shown messages to user for long enough for
        them to get read or user wants to move read horizon up again.
        """
        return self._mark('read', conversation_id, message_nr, from_message_nr)

    def mark_unread(self, conversation_id, message_nr, from_message_nr=None):
        """Used for marking conversation as unread, ie moving read horizon
        back in message flow.
        """
        return self._mark(
            'unread', conversation_id, message_nr, from_message_nr)

    def send(self, conversation_id, message, from_message_nr=None,
             attachments=None, is_retry=False):
        """Send message to flow.

        :param conversation_id: The conversation id.
        :param message: Message content.
        :param from_message_nr: used to return next batch of changes
        :param attachments: list of attachment urls
        :param is_retry: Client is retrying same message send n'th time
        Will fail if from_message_nr != last_message_nr
        """
        # In case we receive an actual UUID obj.
        conversation_id = str(conversation_id)
        if len(conversation_id) != 36:
            raise TypeError('conversation_id must be an 36-char UUID')

        data = {'message': message}
        response = self._server.post("message/send/{}".format(
            conversation_id), data)

        return response

    def store(self, conversation_id, **kwargs):
        """Store message changes whatever they are.
        Do changes in local cache and send only changed fields.

        :param conversation_id: The conversation id.

        Allowed params in kwargs:
        :param message_nr: message nr for edits and deletes
        :param subject: message (email) subject
        :param message: mmessage content
        :param attachments: list of attachment urls
        :param tags: list of tags for message
                        pin - pinned message
                        is_todo - task incomplete
                        is_done - done task
                        is_separator - task separator
                        is_deleted - message deleted
                        is_archived - pin or task archived
        :param pin_weight: Used for sorting
        :param assignee_ids: Assignees for task or message
        :param client_req_id: CrapNet id for message
        :param from_message_nr: used to return next batch of changes
        :param is_retryNone: Client is retrying same message send n'th time
        Will fail if from_message_nr != last_message_nr.
        :param is_url_preview_disabled: Disable generating url previews f
        or this messageand remove if generated
        """

        return self._server.post(
            'message/store/{}'.format(conversation_id), kwargs)
