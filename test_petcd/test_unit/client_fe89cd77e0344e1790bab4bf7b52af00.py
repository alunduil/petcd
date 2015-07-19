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
import itertools

from torment import fixtures
from torment import helpers
from typing import Any
from typing import Iterable

from test_petcd.test_unit import AsyncEtcdClientInitFixture


def powerset(iterable: Iterable[Any]) -> Iterable[Iterable[Any]]:
    '''Powerset of iterable.

    Parameters
    ----------

    :``iterable``: set to calculate powerset

    Return Value(s)
    ---------------

    All subsets of iterable.

    Examples
    --------

    >>> list(powerset([]))
    [()]

    >>> list(powerset([ 1, ]))
    [(), (1,)]

    >>> list(powerset([ 1, 2, ]))
    [(), (1,), (2,), (1, 2)]

    '''

    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))

base = {
    'parameters': {
        'kwargs': {
            'url': 'http://localhost:4001/v2',
        },
    },

    'expected': {
        '_url': 'http://localhost:4001/v2',
        '_retries': 1,
        '_follow_redirects': True,
    },
}

properties = [
    { 'retries': 0, },
    { 'follow_redirects': False, },
]

for subset in powerset(properties):
    fixtures.register(globals(), ( AsyncEtcdClientInitFixture, ), {
        'parameters': {
            'kwargs': functools.reduce(helpers.extend, [ base['parameters']['kwargs'] ] + list(subset), {}),
        },

        'expected': functools.reduce(helpers.extend, [ base['expected'] ] + [ { '_' + key: value for key, value in _.items() } for _ in list(subset) ], {}),
    })
