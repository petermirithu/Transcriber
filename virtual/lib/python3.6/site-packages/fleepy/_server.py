# -*- coding: utf-8 -*-
import sys
import json
import logging
from collections import namedtuple

import requests


# Could have used Six, but this is the only case, could not see
# reasoning for the additional dependency.
if (sys.version_info > (3, 0)):
    # Python 3
    from urllib.parse import urljoin
else:
    # Python 2
    from urlparse import urljoin


Response = namedtuple(
    'Response', ['status_code', 'data', 'headers', 'cookies'])


class HTTPClient(object):
    """An abstraction of an HTTP client.
    """
    @classmethod
    def request(cls, method, url, data=None,
                headers=None, cookies=None, files=None):
        """
        :param method: A HTTP method.
        :param url: The URL to call.
        :param data: The data to be sent as body.
        :param headers: Any headers.
        :param cookies: Any cookies.
        :param files: A list of open files, if any.
        :returns: A `requests.models.Response` object.
        """
        method = method.lower()
        if method.lower() not in ('post', 'get', 'put', 'patch', 'delete'):
            raise ValueError("Invalid HTTP method")

        requester = getattr(requests, method)
        response = requester(
            url,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files)

        return response


class Server(object):
    """An abstraction of the API server. It makes the job of plugging
    the API with a HTTP client and takes care of details like maintaining
    the login session on each request.
    """
    def __init__(self, url='https://fleep.io/api/',
                 client=None, serializer=json):
        self._url = url
        self._client = client or HTTPClient()
        self._serializer = serializer

        self.ticket = None
        self._account_id = None
        self._cookies = {}
        self._account_id = None
        self._display_name = None

        self._logger = logging.getLogger(__name__)

    @property
    def account_id(self):
        """The connected user's account id.
        """
        return self._account_id

    @property
    def display_name(self):
        """The connected user's display name.
        """
        return self._display_name

    def call(self, method, endpoint, parameters=None, files=None, **kwargs):
        """
        :param files: A dictionary of files.
        :param raise_if_not_200: If True will raise ValueError if response
        is not 200. Defaults to False.
        """
        if parameters is None:
            parameters = {}

        url = urljoin(self._url, endpoint)

        if files is not None:
            headers = {"Content-Type": "multipart/form-data"}
        else:
            parameters.setdefault('ticket', self.ticket)
            headers = {"Content-Type": "application/json"}

        self.log(
            'Request to {} using {} method. '
            'Headers: {} / Cookies: {} / Data: {}'.format(
                url, method, headers, self._cookies, parameters))

        response = self._client.request(
            method, url,
            data=self._serialize(parameters),
            headers=headers,
            cookies=self._cookies,
            files=files)

        if response.status_code != 200:
            self.log(
                "Error making request to {}. Error below:\n".format(
                    url, response.text), level='error')
            if kwargs.get('raise_if_not_200', False):
                raise ValueError(response.text)

        try:
            data = response.json()
        except ValueError:
            data = response.text

        return Response(
            response.status_code, data,
            response.headers, response.cookies)

    def log(self, msg, level='debug'):
        """Logs a message using specified level. Defaults to debug.
        """
        logger = getattr(self._logger, level)
        logger(msg)

    def _set_session(self, account_id, token_id,
                     ticket, display_name, profiles):
        """Sets internal data relevant to keeping the session alive.
        """
        self._cookies['token_id'] = token_id
        self.ticket = ticket
        self._profiles = profiles
        self._account_id = account_id
        self._display_name = display_name

    def login(self, email, password, remember_me=False):
        """Performs the login in Fleep server and store relevant
        data for subsequent requests.

        :param email: The user's email.
        :param password: The user's password.
        :param remember_me: If true, will remember the user's session.
        Defauls to False.
        """
        response = self.post(
            "account/login",
            {'email': email, 'password': password, 'remember_me': remember_me})

        data = response.data
        self._set_session(
            data['account_id'],
            response.cookies['token_id'],
            data['ticket'],
            data['display_name'],
            data['profiles'])

        return response

    def logout(self):
        """Logouts from user account.
        """
        if self.ticket is None:
            raise ValueError('Not Logged In Yet!')
        return self.post('account/logout')

    def post(self, endpoint, *args, **kwargs):
        """Convenience wrapper to perform a POST.
        """
        return self.call('POST', endpoint, *args, **kwargs)

    def put(self, endpoint, *args, **kwargs):
        """Convenience wrapper to perform a PUT.
        """
        return self.call('PUT', endpoint, *args, **kwargs)

    def _deserialize(self, data):
        """Deserializes data using serializer passed. Defaults to json.
        """
        if data:
            return self._serializer.loads(data)

    def _serialize(self, data):
        """Serializes data using serializer passed. Defaults to json.
        """
        if data:
            return self._serializer.dumps(data)
