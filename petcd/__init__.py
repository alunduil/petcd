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


class AsyncEtcdClient(object):
    '''Asynchronous etcd client.

    Properties
    ----------

    * ``etcd_index``
    * ``follow_redirects``
    * ``retries``
    * ``url``
    * ``cluster``
    * ``nodes``

    Public Methods
    --------------

    * ``get``
    * ``set``
    * ``delete``
    * ``mkdir``
    * ``ls``
    * ``watch``
    * ``first``
    * ``get_dict``
    * ``get_list``
    * ``get_value``
    * ``get_json``

    Examples
    --------

    TODO Add examples

    '''

    def __init__(self, url, retries = 1, follow_redirects = True):
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
    def url(self):
        '''URL for etcd.'''

        return self._url
