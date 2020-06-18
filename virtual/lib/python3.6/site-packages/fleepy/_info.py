# -*- coding: utf-8 -*-
class Info(object):
    """
    """
    def __init__(self, server, handler='info'):
        self._server = server
        self._handler = handler

    def activityinfo(self):
        """Activity Info.
        """
        return self._server.post("info/activityinfo")
