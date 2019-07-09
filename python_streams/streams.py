from inspect import signature
from functools import lru_cache, reduce
from itertools import islice, chain
from types import BuiltinFunctionType
from typing import Iterable, Iterator, TypeVar, Callable, Tuple, Optional, Generic, List, Any, Union

T = TypeVar('T')
V = TypeVar('V')

Transform = Union[Callable[[T], V], Callable[..., V]]
Filter = Union[Callable[[T], bool], Callable[..., bool]]


def expand(func: Transform):
    def expanded_func(item: ...) -> V:
        return func(*item)

    return (expanded_func if not isinstance(func, BuiltinFunctionType) and len(signature(func).parameters) > 1
            else func)


class Stream(Generic[T], Iterable):
    def __init__(self, items: Iterable[T] = ()):
        self.items = iter(items)

    def __iter__(self) -> Iterator[T]:
        yield from self.items

    def __contains__(self, item_or_iterable: Union[T, Iterable[T]]) -> bool:
        return (self.contains_all(item_or_iterable)
                if isinstance(item_or_iterable, Iterable)
                else self.contains(item_or_iterable))

    def contains(self, item: T) -> bool:
        return item in self.items

    def contains_all(self, iterator: Iterable[T]) -> bool:
        return set(iterator).issubset(set(self))

    def __getitem__(self, index: int) -> T:
        return self.get(index)

    def get(self, index: int) -> T:
        return next(islice(self.items, index, index + 1))

    def map(self, func: Transform) -> 'Stream[V]':
        return Stream(map(expand(func), self.items))

    def map_if(self, condition: Filter, func: Transform) -> 'Stream[Union[T, V]]':
        return Stream(map(lambda x: expand(func)(x) if condition(x) else x, self.items))

    def filter(self, condition: Filter) -> 'Stream[T]':
        return Stream(filter(expand(condition), self.items))

    def reduce(self, func: Callable[[V, T], V], initial: Optional[V] = None) -> V:
        return reduce(func, self.items, initial)

    def for_each(self, func: Transform):
        for x in self.items:
            expand(func)(x)

    def zip(self, other: Iterable[V]) -> 'Stream[Tuple[T, V]]':
        return Stream(zip(self.items, other))

    def max(self, key: Optional[Transform] = None) -> T:
        return max(self.to_list(), key=key) if key else max(self.items)

    def take(self, n: int) -> 'Stream[T]':
        return Stream(islice(self, n))

    def drop(self, n: int) -> 'Stream[T]':
        for i in range(n):
            it = next(self.items, None)
            if it is None:
                return Stream(())
        return Stream(self.items)

    def first(self) -> T:
        return next(self.items)

    def advance(self) -> Tuple[T, 'Stream[T]']:
        return self.first(), self

    def chain(self, *streams: 'Iterable[T]') -> 'Stream[T]':
        return Stream(chain(self, *streams))

    def append(self, item: T) -> 'Stream[T]':
        return Stream((item,)).chain(self)

    def extend(self, item: T) -> 'Stream[T]':
        return self.chain(Stream((item,)))

    @lru_cache(1)
    def to_list(self) -> List[T]:
        return list(self.items)
