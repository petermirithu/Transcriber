# -*- coding: utf-8 -*-
class Alias(object):
    """Email Alias management.

    https://fleep.io/fleepapi/ref-alias.html
    """
    def __init__(self, server, handler='alias'):
        self._server = server
        self._handler = handler

    def add(self, emails):
        """Register email aliases for given account.
        Requires confirmation through email. All conversations are
        transferred under primary account as a result.

        :param emails: Emails to be registered as aliases
        :returns: List of ContactInfo records.
        """
        return self._server.post('alias/add', {'emails': emails})

    def confirm(self, notification_id):
        """Confirm that alias email received confirmation code.

        :param notification_id: The notification ID.
        """
        return self._server.post(
            'alias/confirm', {'notification_id': notification_id})

    def remove(self, emails):
        """Remove email alaiases from given account.

        :param emails: emails to be removed as aliases
        :returns: List of ContactInfo records.
        """
        return self._server.post('alias/remove', {'emails': emails})

    def sync(self):
        """Fetch all aliases for given account. Used for displaying aliases in UI.

        :returns: List of ContactInfo records.
        """
        return self._server.post('alias/sync')
