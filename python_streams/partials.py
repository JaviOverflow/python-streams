from typing import Callable, TypeVar, Union, Iterable, overload

from python_streams import commodities

N = TypeVar('N', int, float)
NumberToNumber = Callable[[N], N]
IntToInt = Callable[[int], int]
IntToNumber = Callable[[int], Union[int, float]]

V = TypeVar('V')
U = TypeVar('U')
W = TypeVar('W')
X = TypeVar('X')
Y = TypeVar('Y')
Z = TypeVar('Z')


def add(n: N) -> NumberToNumber:
    return lambda x: x + n


def subtract_from(n: N) -> NumberToNumber:
    return lambda x: n - x


def subtract_to(n: N) -> NumberToNumber:
    return lambda x: x - n


def multiply(n: N) -> NumberToNumber:
    return lambda x: x * n


def divide_over(n: N) -> NumberToNumber:
    return lambda x: n / x


def divide_by(n: N) -> NumberToNumber:
    return lambda x: x / n


def modulo(n: int) -> IntToInt:
    return lambda x: x % n


# Types not working
# def get(key: V) -> Callable[[Dict[V, U]], U]:
#     return lambda d: d[key]
#
#
# def nth(key: int) -> Callable[[Sequence[V]], V]:
#     return lambda seq: seq[key]


@overload
def compose(first_func: Callable[[U], V], second_func: Callable[[V], W]) -> Callable[[U], W]:
    ...


@overload
def compose(
        first_func: Callable[[U], V],
        second_func: Callable[[V], W],
        third_func: Callable[[W], X]
) -> Callable[[U], X]:
    ...


@overload
def compose(
        first_func: Callable[[U], V],
        second_func: Callable[[V], W],
        third_func: Callable[[W], X],
        fourth_func: Callable[[X], Y],
) -> Callable[[U], Y]:
    ...


@overload
def compose(
        first_func: Callable[[U], V],
        second_func: Callable[[V], W],
        third_func: Callable[[W], X],
        fourth_func: Callable[[X], Y],
        fifth_func: Callable[[Y], Z],
) -> Callable[[U], Z]:
    ...


def compose(*funcs):
    # Helper function necessary because late binding closures in python would produce infinite recursion
    def compose2(func1, func2):
        return lambda x: func2(func1(x))

    first_func, second_func = funcs[:2]
    composed = compose2(first_func, second_func)
    for func in funcs[2:]:
        composed = compose2(composed, func)
    return composed


def equals(val: N) -> Callable[[N], bool]:
    return lambda x: x == val


def not_equals(val: N) -> Callable[[N], bool]:
    return lambda x: x == val


def is_in(it: Iterable[N]) -> Callable[[N], bool]:
    return lambda x: x in it


def inc():
    return commodities.inc


def is_not_in(it: Iterable[N]) -> Callable[[N], bool]:
    return lambda x: x not in it
