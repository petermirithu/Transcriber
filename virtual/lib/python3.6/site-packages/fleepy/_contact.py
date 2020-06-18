# -*- coding: utf-8 -*-
class Sync(object):
    def __init__(self, server, handler='contact/sync'):
        self._server = server
        self._handler = handler

    def __call__(self, contact_id):
        """Top-level sync call. __call__ used to replicate API
        behaviour.

        Returns profile data for given id. Use it to update local client
        side cache.
        """
        return self._server.post('contact/sync', {'contact_id': contact_id})

    def activity(self, contacts):
        """Sync last seen time for requested contacts

        :param contacts: List of account IDs to sync.
        """
        return self._server.post(
            'contact/sync/activity', {'contacts': contacts})

    def all(self, ignore=None, search_str=None):
        """Returns profile data for given list of id’s.
        Use it to update local client side cache.

        :param ignore: list of account_ids client already has.
        :param search_str: filter found contacts using given string
        """
        return self._server.post(
            'contact/sync/all', {'ignore': ignore, 'search_str': search_str})

    def list(self, contacts):
        """Returns profile data for given list of IDs. Use it to update
        local client side cache.

        :param contacts: List of account IDs to sync.
        """
        return self._server.post('contact/sync/list', {'contacts': contacts})


class Contact(object):
    """
    """
    def __init__(self, server, handler='contact'):
        self._server = server
        self._handler = handler

        self.sync = Sync(self._server)

    def describe(self, contact_id, contact_name=None, phone_nr=None):
        """Provide description for the contact that will be displayed
        only to the user
        """
        return self._server.post(
            "contact/describe",
            {'contact_id': contact_id,
             'contact_name': contact_name,
             'phone_nr': phone_nr})

    def hide(self, contacts):
        """Hide contacts from this user’s contact list

        :param contacts: List of contacts to hide.
        """
        return self._server.post("contact/hide", {'contacts': contacts})

    def import_(self, contact_list):
        """Underscore added to not clash with native python import.

        Import contacts into user's contact list. Used for Gmail contact
        import.

        :param contact_list: A list of contact dictionaries. These dictionaries
        must have keys addr_full (email address), addr_descr (contact name) and
        phone_nr (phone number).
        """
        return self._server.post(
            "contact/import", {'contact_list': contact_list})

    def unlist(self, contact_id):
        """Remove contact from conversation list dialog suggestions.

        :param contact_id: The account ID to remove from conversation list.
        """
        self._server.post('contact/unlist', {'contact_id': contact_id})
