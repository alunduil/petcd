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
from test_petcd.test_unit import AsyncEtcdClientGetFixture

expected = {
    'key': '/foo',
    'quorum': False,
    'recursive': False,
    'sorted': False,
    'wait': False,
    'wait_index': None,
}

arguments = [
    { 'quorum': ( True, ), },
    { 'recursive': ( True, ), },
    { 'sorted': ( True, ), },
    { 'wait_index': ( 0, 1, ), },
    { 'wait': ( True, ), },
]

for combination in test_helpers.powerset(arguments):
    for subset in test_helpers.evert(combination):
        fixtures.register(globals(), ( AsyncEtcdClientGetFixture, ), {
            'parameters': {
                'kwargs': functools.reduce(helpers.extend, list(subset), { 'key': '/foo', }),
            },

            'expected': functools.reduce(helpers.extend, [ expected ] + list(subset), { 'key': '/foo', }),
        })
