from functools import lru_cache
from itertools import islice, chain
from typing import Iterable, Iterator, TypeVar, Callable, Tuple, Optional, Generic, List, Any, Union

T = TypeVar('T')
V = TypeVar('V')


class Stream(Generic[T], Iterable):
    def __init__(self, items: Iterable[T] = ()):
        self.items = iter(items)

    def __iter__(self) -> Iterator[T]:
        yield from self.items

    def map(self, func: Callable[[T], V]) -> 'Stream[V]':
        return Stream(map(func, self.items))

    def map_if(self, condition: Callable[[T], bool], func: Callable[[T], V]) -> 'Stream[Union[T, V]]':
        return Stream(map(lambda x: func(x) if condition(x) else x, self.items))

    def filter(self, func: Callable[[T], bool]) -> 'Stream[T]':
        return Stream(filter(func, self.items))

    def for_each(self, func: Callable[[T], Any]):
        for x in self.items:
            func(x)

    def zip(self, other: Iterable[V]) -> 'Stream[Tuple[T, V]]':
        return Stream(zip(self.items, other))

    def max(self, key: Optional[Callable[[T], Any]] = None) -> T:
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
