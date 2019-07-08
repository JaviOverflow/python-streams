from itertools import count, cycle
from typing import Sequence, TypeVar

from python_streams import Stream


def test_iter():
    s = Stream([0, 1, 2, 3])
    for i, x in zip(range(4), s):
        assert i == x


def test_to_list():
    s = Stream(['a', 'b', 'c'])
    assert s.to_list() == ['a', 'b', 'c']
    assert s.to_list() == ['a', 'b', 'c']


def test_map():
    assert Stream([1, 5, 3]).map(lambda x: x * 2).to_list() == [2, 10, 6]


def test_first():
    assert Stream([2, 1, 4]).first() == 2


def test_take():
    assert Stream(count(1, 2)).take(3).to_list() == [1, 3, 5]


def test_drop():
    assert Stream(count(1, 2)).drop(3).first() == 7


def test_filter():
    assert Stream(count(1)).filter(lambda x: x % 7 == 0).take(4).to_list() == [7, 14, 21, 28]


accum = 0


def test_for_each():
    def _side_effect(inc: int):
        global accum
        accum += inc

    Stream(count(1)).take(5).for_each(_side_effect)
    assert accum == 15


def test_zip():
    ascii_a_to_c = range(ord('a'), ord('d'))
    assert Stream(cycle(ascii_a_to_c)).map(chr).zip(count(1)).take(5).to_list() == [
        ('a', 1), ('b', 2), ('c', 3), ('a', 4), ('b', 5)]


def test_max():
    def first(seq):
        return seq[0]

    def second(seq):
        return seq[1]

    assert Stream([2, 1, 5, 4, -6]).max() == 5
    s = Stream([('a', 2), ('z', 1), ('c', 7)])
    assert s.max(key=first) == ('z', 1)
    assert s.max(key=second) == ('c', 7)


def test_advance():
    x, rest = Stream(count(3)).take(4).advance()
    assert x == 3
    assert rest.to_list() == [4, 5, 6]


def test_chain():
    assert Stream([1, 2, 3]).chain(Stream(['a', 'b', 'c']), count(4)).take(8).to_list() == [
        1, 2, 3, 'a', 'b', 'c', 4, 5]


def test_append():
    assert Stream([1, 2, 3]).append(0).to_list() == [0, 1, 2, 3]


def test_extend():
    assert Stream([1, 2]).extend(3).to_list() == [1, 2, 3]


def test_map_when_items_are_tuples():
    assert (Stream([('a', 1), ('b', 5), ('c', 3)])
            .map(lambda k, v: (k, v * 2))
            .to_list()) == [('a', 2), ('b', 10), ('c', 6)]


def test_filter_when_items_are_tuples():
    assert (Stream([('a', 1), ('b', 5), ('c', 3)])
            .filter(lambda k, v: v > 3)
            .to_list()) == [('b', 5)]
