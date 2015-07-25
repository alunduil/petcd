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

import itertools
import logging
import typing  # flake8: noqa (use mypy typing)

from typing import Any
from typing import Dict
from typing import Iterable
from typing import Tuple

logger = logging.getLogger(__name__)


def evert(iterable: Iterable[Dict[str, Tuple]]) -> Iterable[Dict[str, Any]]:
    '''Evert dictionaries with tuples.

    Iterates over the list of dictionaries and everts them with their tuple
    values.  For example:
    
    ``[ { 'a': ( 1, 2, ), }, ]``

    becomes

    ``[ ( { 'a': 1, }, ), ( { 'a', 2, }, ) ]``

    The resulting iterable contains the same number of tuples as the
    initial iterable had tuple elements.  The number of dictionaries is the same
    as the cartesian product of the initial iterable's tuple elements.

    Parameters
    ----------

    :``iterable``: list of dictionaries whose values are tuples

    Return Value(s)
    ---------------

    All combinations of the choices in the dictionaries.

    Examples
    --------

    >>> list(evert([]))
    [[]]

    >>> list(evert([ { 'foo': ( True, False, ), }, ]))
    [[{'foo': True}], [{'foo': False}]]

    >>> list(evert([ { 'foo': ( True, False, ), }, { 'bar': ( True, False, ), }, ]))
    [[{'foo': True}, {'bar': True}], [{'foo': True}, {'bar': False}], [{'foo': False}, {'bar': True}], [{'foo': False}, {'bar': False}]]


    '''

    keys = list(itertools.chain.from_iterable([ _.keys() for _ in iterable ]))

    for values in itertools.product(*[ list(*_.values()) for _ in iterable ]):
        yield [ dict(( pair, )) for pair in zip(keys, values) ]


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
