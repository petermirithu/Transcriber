# -*- coding: utf-8 -*-
import os


class Avatar(object):
    """Avatar management.

    https://fleep.io/fleepapi/ref-account.html#avatar-delete
    """
    def __init__(self, server, handler='avatar'):
        self._server = server
        self._handler = handler

    def delete(self):
        """Deletes current avatar

        :returns: Response has no data.
        """
        self._server.post('avatar/delete')

    def upload(self, image_path):
        """
        Upload avatar image.

        :param image_path: The image path.
        :returns: Response contains file_id, name and size.
        """
        if image_path is None:
            file_name = os.path.basename(image_path)

        with open(image_path, 'rb') as file_data:
            files = {'files': (file_name, file_data)}

            return self._server.put('avatar/upload/?ticket={}'.format(
                self._server.ticket), files=files)
