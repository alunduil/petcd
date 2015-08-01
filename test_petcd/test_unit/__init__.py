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
import os
import typing  # noqa (use mypy typing)
import unittest

from torment import contexts
from torment import decorators
from torment import fixtures
from torment import helpers

from petcd import AsyncEtcdClient

logger = logging.getLogger(__name__)


class AsyncEtcdClientInitFixture(fixtures.Fixture):
    @property
    def description(self) -> str:
        return super().description + '.AsyncEtcdClient(**{0.parameters[kwargs]})'.format(self)

    def run(self) -> None:
        self.result = AsyncEtcdClient(**self.parameters['kwargs'])

    def check(self) -> None:
        _ = vars(self.result)

        self.context.assertIsInstance(_.pop('_session'), aiohttp.ClientSession)
        self.context.assertEqual(self.expected, _)


class AsyncEtcdClientPropertyFixture(fixtures.Fixture):
    @property
    def description(self) -> str:
        return super().description + '.AsyncEtcdClient.{0.property} == {0.expected}'.format(self)

    def setup(self) -> None:
        self.client = AsyncEtcdClient(**{ self.property: self.expected })

    def run(self) -> None:
        self.result = getattr(self.client, self.property)

    def check(self) -> None:
        self.context.assertEqual(self.expected, self.result)


class AsyncEtcdClientMethodFixture(fixtures.Fixture):
    @property
    def description(self) -> str:
        return super().description + '.AsyncEtcdClient.'

    def setup(self) -> None:
        url = 'http://127.0.0.1:2379/v2'

        if not self.context.mock_aiohttp():
            url = self.context.host

        self.client = AsyncEtcdClient(url, retries = 0)

    def check(self) -> None:
        if self.context.mock_aiohttp():
            self.context.mocked_aiohttp_clientsession.request.assert_called_once_with(**self.expected['request'])


class AsyncEtcdClientDeleteFixture(AsyncEtcdClientMethodFixture):
    @property
    def description(self) -> str:
        return super().description + 'delete(**{0.parameters[kwargs]})'.format(self)

    def run(self) -> None:
        self.context.loop.run_until_complete(self.client.delete(**self.parameters['kwargs']))


class AsyncEtcdClientGetFixture(AsyncEtcdClientMethodFixture):
    @property
    def description(self) -> str:
        return super().description + 'get(**{0.parameters[kwargs]})'.format(self)

    def run(self) -> None:
        self.context.loop.run_until_complete(self.client.get(**self.parameters['kwargs']))


class AsyncEtcdClientSetFixture(AsyncEtcdClientMethodFixture):
    @property
    def description(self) -> str:
        return super().description + 'set(**{0.parameters[kwargs]})'.format(self)

    def run(self) -> None:
        self.context.loop.run_until_complete(self.client.set(**self.parameters['kwargs']))


class AsyncEtcdClientKeyUrlFixture(AsyncEtcdClientMethodFixture):
    @property
    def description(self) -> str:
        return super().description + '._key_url({0.parameters[key]}) == {0.expected}'.format(self)

    def run(self) -> None:
        self.result = self.client._key_url(self.parameters['key'])

    def check(self) -> None:  # override
        self.context.assertEqual(self.result, self.expected)

helpers.import_directory(__name__, os.path.dirname(__file__), sort_key = lambda _: -_.count('_') )


class ClientUnitTest(contexts.TestContext, metaclass = contexts.MetaContext):
    mocks = set()  # type: Set[str]

    fixture_classes = (
        AsyncEtcdClientInitFixture,
        AsyncEtcdClientPropertyFixture,
        AsyncEtcdClientMethodFixture,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.loop = asyncio.get_event_loop()

    def __del__(self) -> None:
        logger.info('deleting ClientUnitTest')

        self.loop.close()

    mocks.add('aiohttp')

    @decorators.mock('aiohttp')
    def mock_aiohttp(self):
        self.patch('aiohttp')

        self.mocked_aiohttp_clientsession = unittest.mock.MagicMock()
        self.mocked_aiohttp.ClientSession.return_value = self.mocked_aiohttp_clientsession
