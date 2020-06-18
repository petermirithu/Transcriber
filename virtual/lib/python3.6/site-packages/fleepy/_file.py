# -*- coding: utf-8 -*-
import os


class Upload(object):
    """Wraps Upload capabilities.

    https://fleep.io/fleepapi/ref-file.html
    """
    def __init__(self, server, handler='file/upload'):
        self._server = server
        self._handler = handler

    def __call__(self, file_path, file_name=None):
        """Top-level File Upload API call.

        Upload a file.

        .. note:: According to Fleep Docs, their endpoint supports
        multiple-files, however, even though it doesn't fail, it seems to
        always return a single file_id. Until we clear what happens here,
        this method is supporting single-file upload only.

        Returns file_id which needs later given to /api/file/send.

        NOTE: /api/file/send is not documented in Fleep API documentation.

        :param file_path: The file path.
        :param file_name: An optional custom file name. Defaults to the actual
        file name.
        :returns: Response contains a list of:

        file_id             text                - backward compat
        upload_url          text                - unique url
        name                text                - file name
        size                bigint              - file size
        width               integer             - width of picture
        height              integer             - height of picture
        is_animated         bool                - is animated picture
        file_type           text                - file mime type
        file_sha256         text                - file sha256
        """
        if file_name is None:
            file_name = os.path.basename(file_path)

        with open(file_path, 'rb') as file_data:
            files = {'files': (file_name, file_data)}

            return self._server.put('file/upload/?ticket={}'.format(
                self._server.ticket), files=files)

    def external(self, file_url, file_name, file_size=0,
                 conversation_id=None, upload_id=None):
        """Add file into Fleep from an external source.
        Maximum allowed file size is 1GB. Upload request is
        put into queue and processed by a background job.
        Upload progress events are sent to the client during the
        upload process, see UploadInfo for more details.

        :param file_url: The URL to get the file.
        :param file_name: The name of the file.
        :param file_size: Max 1073741824. Defaults to 0.
        :param conversation_id: Needed if file is related to a conversation.
        :param upload_id: Upload ID on client side.
        :returns: Response contains request_id which is an unique upload id -
        not the same as file_id.
        """
        return self._server.post(
            'file/upload/external/',
            {'file_url': file_url,
             'file_name': file_name,
             'file_size': file_size,
             'conversation_id': conversation_id,
             'upload_id': upload_id})


class File(object):
    """Empty wrapper for :class: `Upload` for now as Fleep File Management
    API only supports upload capabilities.
    """
    def __init__(self, server, handler='file'):
        self._server = server
        self._handler = handler

        self.upload = Upload(self._server)
