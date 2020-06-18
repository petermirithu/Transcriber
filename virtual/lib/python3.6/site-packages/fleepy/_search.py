# -*- coding: utf-8 -*-
class Search(object):
    """
    """
    def __init__(self, server, handler='search'):
        self._server = server
        self._handler = handler

    def __call__(self, keywords, conversation_id=None,
                 need_suggestions=False, is_extended_search=False):
        """Top-level Search API call.

        Search for content in Fleep.

        :param keywords: A list of keywords.
        :param conversation_id: If provided, limits search to a single
        conversation. Optional.
        :param need_suggestions: Request suggestion list. Defaults to False.
        :param is_extended_search: Search also in topic and members.
        Defaults to False.
        """
        keywords = ' '.join(keywords)
        data = {
            'keywords': keywords,
            'conversation_id': conversation_id,
            'need_suggestions': need_suggestions,
            'is_extended_search': is_extended_search}
        return self._server.post('search', data)

    def prepare(self):
        """Load current user’s index data to cache.
        """
        return self._server.post('search/prepare')

    def reset(self):
        """Drop user’s index from cache.
        """
        return self._server.post('search/reset')

    def suggest(self, keywords, conversation_id=None):
        """Suggest words.

        :param keywords: List of keywords.
        :param conversation_id: limit search to one conversation
        :returns: List of strings. Suggestions are given for last
        word of keywords.
        """
        keywords = ' '.join(keywords)
        return self._server.post(
            'search/suggest',
            {'keywords': keywords, 'conversation_id': conversation_id})
