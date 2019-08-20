from typing import Any, Union, Callable

import pytest

from python_streams import partials as _, compose


@pytest.mark.parametrize(
    'funcs,expected',
    [
        ([_.inc(), _.divide_by(2)], 10),
        ([_.inc(), _.divide_by(2), _.multiply(7)], 70),
        ([_.inc(), _.divide_by(2), _.multiply(7), _.subtract_to(5)], 65),
    ]
)
def test_compose(funcs, expected):
    assert compose(*funcs)(19) == expected
