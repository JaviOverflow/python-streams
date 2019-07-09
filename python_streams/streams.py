from inspect import signature
from functools import reduce
from inspect import signature
from itertools import islice, chain, count
from types import BuiltinFunctionType
from typing import Iterable, Iterator, TypeVar, Callable, Tuple, Optional, Generic, List, Union

from python_streams.partials import compose

T = TypeVar('T')
V = TypeVar('V')

Transform = Union[Callable[[T], V], Callable[..., V]]
Filter = Union[Callable[[T], bool], Callable[..., bool]]


def expand(func: Transform):
    def expanded_func(item: ...) -> V:
        return func(*item)

    return (expanded_func if not isinstance(func, BuiltinFunctionType) and len(signature(func).parameters) > 1
            else func)


def Not(value: bool):
    return not value


class Stream(Generic[T], Iterable):
    def __init__(self, items: Iterable[T] = (), with_cache=True):
        self.items = iter(items)
        self.with_cache = with_cache
        self.cache = None
        self.is_consumed = False

    def __iter__(self) -> Iterator[T]:
        yield from self.items

    def __len__(self) -> int:
        return len(self.to_list())

    # start kotlin functions

    def __eq__(self, other):
        for self_item, other_item in zip(self, other):
            if self_item != other_item:
                return False
        return True

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

    def index_of(self, item: T) -> int:
        for index, self_item in zip(self.items, count()):
            if self_item == item:
                return index
        return -1

    def is_empty(self) -> bool:
        try:
            self.items.__next__()
            return False
        except StopIteration:
            return True

    def last_index_of(self, item: T) -> int:
        last_index = -1
        for index, self_item in zip(count(), self.items):
            if self_item == item:
                last_index = index
        return last_index

    def sub_stream(self, from_index_inclusive: int, to_index_exclusive: int) -> 'Stream[T]':
        return Stream(islice(self, from_index_inclusive, to_index_exclusive))

    def indices(self) -> 'Stream[int]':
        return Stream(range(len(self)))

    def last_index(self) -> int:
        return len(self) - 1

    def all(self, condition: Filter) -> bool:
        return list(filter(compose(expand(condition), Not), self.items)) == []

    def any(self, condition: Filter) -> bool:
        return list(filter(expand(condition), self.items)) != []

    def count(self) -> int:
        return len(self)

    # TODO: Fix non laziness
    def distinct(self) -> 'Stream[T]':
        unique_items = []
        for item in self.to_list():
            if item not in unique_items:
                unique_items.append(item)
        return Stream(unique_items)

    # TODO: Fix non laziness
    def distinct_by(self, selector: Transform) -> 'Stream[T]':
        unique_items = []
        unique_keys = []
        for item in self.to_list():
            key = expand(selector)(item)
            if key not in unique_keys:
                unique_keys.append(key)
                unique_items.append(item)
        return Stream(unique_items)

    # end kotlin functions

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

    class AlreadyConsumed(Exception):
        pass

    def to_list(self) -> List[T]:
        if self.with_cache:
            if not self.cache:
                self.cache = list(self.items)
            return self.cache
        else:
            if self.is_consumed:
                raise self.AlreadyConsumed
            else:
                self.is_consumed = True
                return list(self.items)
