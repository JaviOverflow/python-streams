from typing import Callable, TypeVar, Union, Any, Sequence, Dict

T = TypeVar('T', int, float)
NumberToNumber = Callable[[T], T]
IntToInt = Callable[[int], int]
IntToNumber = Callable[[int], Union[int, float]]

V = TypeVar('V')
U = TypeVar('U')
W = TypeVar('W')
X = TypeVar('X')

def add(n: T) -> NumberToNumber:
    return lambda x: x + n


def subtract_from(n: T) -> NumberToNumber:
    return lambda x: n - x


def subtract_to(n: T) -> NumberToNumber:
    return lambda x: x - n


def multiply(n: T) -> NumberToNumber:
    return lambda x: x * n


def divide_over(n: T) -> NumberToNumber:
    return lambda x: n / x


def divide_by(n: T) -> NumberToNumber:
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


def compose(first_func: Callable[[U], V], second_func: Callable[[V], W]) -> Callable[[U], W]:
    return lambda x: second_func(first_func(x))


def compose3(
        first_func: Callable[[U], V],
        second_func: Callable[[V], W],
        third_func: Callable[[W], X]
) -> Callable[[U], X]:
    return compose(first_func, compose(second_func, third_func))
