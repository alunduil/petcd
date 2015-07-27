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

import functools

from torment import fixtures
from torment import helpers

from test_petcd import test_helpers
from test_petcd.test_unit import AsyncEtcdClientSetFixture

expected = {
    'value': 'bar',
    'append': False,
    'directory': False,
    'previous_exists': None,
    'previous_index': None,
    'previous_value': None,
    'ttl': None,
}

arguments = [
    { 'append': ( True, ), },
    { 'directory': ( True, ), },
    { 'previous_exists': ( False, True, ), },
    { 'previous_index': ( False, True, ), },
    { 'previous_value': ( 'bar', ), },
    { 'ttl': ( 0, 1, ), },
]

for combination in test_helpers.powerset(arguments):
    for subset in test_helpers.evert(combination):
        fixtures.register(globals(), ( AsyncEtcdClientSetFixture, ), {
            'parameters': {
                'kwargs': functools.reduce(helpers.extend, list(subset), { 'key': '/foo', 'value': 'bar', }),
            },

            'expected': {
                'result': None,
                'request': {
                    'method': 'PUT',
                    'url': 'http://127.0.0.1:2379/v2/keys/foo',
                    'data': functools.reduce(helpers.extend, [ expected ] + list(subset), {}),
                },
            },
        })
