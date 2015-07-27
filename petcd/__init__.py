# Copyright 2015 Alex Brandt
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import aiohttp
import asyncio
import logging
import typing  # flake8: noqa (use mypy typing)

from typing import Union

logger = logging.getLogger(__name__)


class AsyncEtcdClient(object):
    '''Asynchronous etcd client.

    Properties
    ----------

    * ``cluster``
    * ``etcd_index``
    * ``follow_redirects``
    * ``nodes``
    * ``retries``
    * ``url``

    Public Methods
    --------------

    * ``delete``
    * ``first``
    * ``get``
    * ``get_dict``
    * ``get_json``
    * ``get_list``
    * ``get_value``
    * ``ls``
    * ``mkdir``
    * ``set``
    * ``watch``

    Examples
    --------

    TODO Add examples

    '''

    def __init__(self, url: str = 'http://localhost:7379/v2', connection_limit: int = 10, follow_redirects: bool = True, retries: int = 1) -> None:
        '''Create AsyncEtcdClient.

        Parameters
        ----------

        :``url``:              URL for etcd
        :``connection_limit``: number of simultaneous connections to use
        :``follow_redirects``: follow redirect responses (3xx)
        :``retries``:          number of times to retry failed requests

        '''

        self._url = url

        self._connection_limit = connection_limit
        self._follow_redirects = follow_redirects
        self._retries = retries

        self._session = aiohttp.ClientSession(
            connector = aiohttp.TCPConnector(limit = self.connection_limit)
        )

    @property
    def follow_redirects(self):
        '''True if redirects will be followed; otherwise, False.'''

        return self._follow_redirects

    @property
    def retries(self) -> int:
        '''Number of times to retry actions.'''

        return self._retries

    @property
    def url(self) -> str:
        '''URL for etcd.'''

        return self._url

    @property
    def session(self) -> aiohttp.ClientSession:
        '''aiohttp.ClientSession for this Client.'''

        return self._session

    @property
    def connection_limit(self) -> int:
        '''Number of simultaneous connections to etcd.'''

        return self._connection_limit

    @asyncio.coroutine
    def delete(self, key: str, directory: bool = False, previous_index: Union[None, int] = None, previous_value: Union[None, str] = None, recursive: bool = False):
        '''Perform a delete action on the given key.

        Parameters
        ----------

        :``key``:             the key to delete (i.e. '/foo')
        :``directory``:       act on a directory
        :``previous_index``:  only perform delete if key's previous index
        :``previous_value``:  only perform delete if key's value
        :``recursive``:       act on all children as well

        Return Value(s)
        ---------------

        EtcdResult ??

        '''

        params = {
            'directory': directory,
            'previous_index': previous_index,
            'previous_value': previous_value,
            'recursive': recursive,
        }

        return ( yield from self.session.request(method = 'DELETE', url = self._key_url(key), params = params) )

    @asyncio.coroutine
    def get(self, key: str, quorum: bool = False, recursive: bool = False, sorted: bool = False, wait: bool = False, wait_index: Union[int, None]  = None):
        '''Perform a get action on the given key.

        Parameters
        ----------

        :``key``:        the key to retrieve (i.e. '/foo')
        :``quorum``:     linearize the read (takes a similar path as write)
        :``recursive``:  return specified key and all children
        :``sorted``:     lexicographically sort the list of nodes (children)
        :``wait``:       wait for an event on the specified key
        :``wait_index``: point in time (etcd_index) to begin watching for events

        Return Value(s)
        ---------------

        EtcdResult ??

        '''

        params = {
            'quorum': quorum, 
            'recursive': recursive,
            'sorted': sorted,
            'wait': wait,
            'wait_index': wait_index,
        }

        return ( yield from self.session.request(method = 'GET', url = self._key_url(key), params = params) )

    @asyncio.coroutine
    def set(self, key: str, value: str, append: bool = False, directory: bool = False, previous_exists: Union[None, bool] = None, previous_index: Union[None, int] = None, previous_value: Union[None, str] = None, ttl: Union[None, int] = None):
        '''Perform a set action on the given key with the given value.

        Parameters
        ----------

        :``key``:             the key to set (i.e. '/foo')
        :``value``:           the value to set
        :``append``:          append value to auto-incrementing directory
        :``directory``:       act on a directory
        :``previous_exists``: only perform set if key already exists
        :``previous_index``:  only perform set if key's previous index
        :``previous_value``:  only perform set if key's value
        :``ttl``:             time to live of key

        Return Value(s)
        ---------------

        EtcdResult ??

        '''

        body = {
            'value': value,
            'append': append,
            'directory': directory,
            'previous_exists': previous_exists,
            'previous_index': previous_index,
            'previous_value': previous_value,
            'ttl': ttl,
        }

        return ( yield from self.session.request(method = 'PUT', url = self._key_url(key), data = body) )

    def _key_url(self, key: str) -> str:
        '''Add etcd URL and API endpoint to key.

        Parameters
        ----------

        :``key``: the key to retrieve an etcd API URL for

        Return Value(s)
        ---------------

        The etcd API endpoint URL for the given key.

        '''

        if not key.startswith('/'):
            key = '/' + key

        logger.debug('self.url: %s', self.url)

        return self.url + '/keys' + key
