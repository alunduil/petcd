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
import logging

from torment import fixtures
from torment import helpers

from test_petcd import test_helpers
from test_petcd.test_unit import AsyncEtcdClientInitFixture
from test_petcd.test_unit import AsyncEtcdClientPropertyFixture

logger = logging.getLogger(__name__)

expected = {
    '_connection_limit': 10,
    '_url': 'http://localhost:7379/v2',
    '_retries': 1,
    '_follow_redirects': True,
}

properties = [ { fixture.property: fixture.expected, } for fixture in fixtures.of(( AsyncEtcdClientPropertyFixture, )) ]

for subset in test_helpers.powerset(properties):
    fixtures.register(globals(), ( AsyncEtcdClientInitFixture, ), {
        'parameters': {
            'kwargs': functools.reduce(helpers.extend, list(subset), {}),
        },

        'expected': functools.reduce(helpers.extend, [ expected ] + [ { '_' + key: value for key, value in _.items() } for _ in list(subset) ], {}),
    })
