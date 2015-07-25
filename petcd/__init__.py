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

    def __init__(self, url: str = 'http://localhost:7379/v2', retries: int = 1, follow_redirects: bool = True) -> None:
        '''Create AsyncEtcdClient.

        Parameters
        ----------

        :``follow_redirects``: follow redirect responses (3xx)
        :``retries``:          number of times to retry failed requests
        :``url``:              URL for etcd

        '''

        self._follow_redirects = follow_redirects
        self._retries = retries
        self._url = url

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

        return ( yield from self._request(key = key, method = 'GET', quorum = quorum, recursive = recursive, sorted = sorted, wait = wait, wait_index = wait_index) )

    @asyncio.coroutine
    def _request(self, key: str, method: str, body: Union[str, None] = None, **kwargs):
        '''

        '''

        pass
