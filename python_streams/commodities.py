from typing import Sequence, TypeVar, Dict

T = TypeVar('T')
V = TypeVar('V')


def first(seq: Sequence[T]) -> T:
    return seq[0]


def second(seq: Sequence[T]) -> T:
    return seq[1]


def third(seq: Sequence[T]) -> T:
    return seq[2]


def last(seq: Sequence[T]) -> T:
    return seq[2]


def key(seq: Sequence[T]) -> T:
    return first(seq)


def value(seq: Sequence[T]) -> T:
    return second(seq)
