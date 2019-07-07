from functools import lru_cache
from typing import Iterable, Iterator, TypeVar, Callable, Tuple, Optional, Generic, List

T = TypeVar('T')
V = TypeVar('V')


class Stream(Generic[T], Iterable):
    def __init__(self, items: Iterable[T] = ()):
        self.items = iter(items)

    def __iter__(self) -> Iterator[T]:
        yield from self.items

    def map(self, func: Callable[[T], V]) -> 'Stream[V]':
        print('Map')
        return Stream(map(func, self.items))

    def filter(self, func: Callable[[T], bool]) -> 'Stream[T]':
        return Stream(filter(func, self.items))

    def for_each(self, func: Callable[[T], None]):
        for x in self.items:
            func(x)

    def zip(self, other: Iterable[V]) -> 'Stream[Tuple[T, V]]':
        return Stream(zip(self.items, other))

    def max(self, comparator: Optional[Callable[[T, T], T]]) -> T:
        return max(self.to_list(), key=comparator) if comparator else max(self.items)

    def first

    @lru_cache(1)
    def to_list(self) -> List[T]:
        return list(self.items)


if __name__ == '__main__':
    def inc(x: int):
        print(f'Incremented {x}')
        return x + 1

    x = Stream([1, 2, 3]).map(inc)
    print('Mark')
    print(x.to_list())
    print(x.to_list())
    y = Stream([1, 2, 3])
    # for i, c in Stream(cycle(['a', 'b', 'c', 'd'])).zip(count(1)):
    #     pass
