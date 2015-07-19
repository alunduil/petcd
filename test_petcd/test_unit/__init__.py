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

import os

from torment import fixtures
from torment import helpers
from torment import MetaContext
from torment import TestContext

from petcd import AsyncEtcdClient


class EtcdClientInitFixture(fixtures.Fixture):
    def check(self):
        self.context.assertEqual(self.expected, vars(self.result))


class AsyncEtcdClientInitFixture(EtcdClientInitFixture):
    def description(self):
        return super().description + 'AsyncEtcdClient({0.parameters[kwargs]})'.format(self)

    def run(self):
        self.result = AsyncEtcdClient(**self.parameters['kwargs'])

helpers.import_directory(__name__, os.path.dirname(__file__))


class ClientUnitTest(TestContext, metaclass = MetaContext):
    fixture_classes = (
        AsyncEtcdClientInitFixture,
    )
