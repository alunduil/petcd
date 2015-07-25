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

import asyncio
import logging
import os
import typing  # flake8: noqa (use mypy typing)
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
        self.context.assertEqual(self.expected, vars(self.result))


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

class AsyncEtcdClientGetFixture(fixtures.Fixture):
    @property
    def description(self) -> str:
        return super().description + '.AsyncEtcdClient.get(**{0.parameters[kwargs]})'.format(self)

    def setup(self) -> None:
        url = 'http://127.0.0.1:2379/v2'

        if not self.context.mock_aiohttp():
            url = self.context.host

        _ = unittest.mock.patch.object(AsyncEtcdClient, '_request', unittest.mock.MagicMock())
        self.mocked_request = _.start()
        self.context.addCleanup(_.stop)

        self.client = AsyncEtcdClient(url, retries = 0)

    def run(self) -> None:
        self.context.loop.run_until_complete(self.client.get(**self.parameters['kwargs']))

    def check(self) -> None:
        self.mocked_request.assert_called_once_with(method = 'GET', **self.expected)


helpers.import_directory(__name__, os.path.dirname(__file__), sort_key = lambda _: -_.count('_') )


class ClientUnitTest(contexts.TestContext, metaclass = contexts.MetaContext):
    mocks = set()  # type: Set[str]

    fixture_classes = (
        AsyncEtcdClientInitFixture,
        AsyncEtcdClientPropertyFixture,
        AsyncEtcdClientGetFixture,
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
