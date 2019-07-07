import time
from collections import Iterable
from itertools import count, islice

from functional import seq

from python_streams import Stream


def sieve_eratosthenes() -> Stream[int]:
    def _make_filter(prime: int):       # HACK: Necessary because python closures are late-binding
        return lambda x: x % prime != 0

    def _sieve():
        yield 1
        candidates = Stream(count(2))
        while True:
            prime, rest = candidates.advance()
            yield prime
            candidates = candidates.filter(_make_filter(prime))

    return Stream(_sieve())


def sieve_eratosthenes_pyfunctional() -> Stream[int]:
    def _make_filter(prime: int):       # HACK: Necessary because python closures are late-binding
        return lambda x: x % prime != 0

    def _sieve():
        yield 1
        candidates = seq(count(2))
        while True:
            prime = candidates.first()
            candidates.drop(1)
            yield prime
            candidates = candidates.filter(_make_filter(prime))

    return Stream(_sieve())


def sieve_eratosthenes_iterators():
    def _make_filter(prime: int):       # HACK: Necessary because python closures are late-binding
        return lambda x: x % prime != 0

    def _sieve():
        yield 1
        candidates = count(2)
        while True:
            prime = next(candidates)
            yield prime
            candidates = filter(_make_filter(prime), candidates)

    return _sieve()


def benchmark(num_primes):
    print('Printing first ten primes with each method to verify they work')
    print('Calculate with python-streams')
    sieve_eratosthenes().take(10).for_each(print)
    print('Calculate with pyfunctional')
    sieve_eratosthenes_pyfunctional().take(10).for_each(print)
    print('Calculate with iterators')
    for prime in islice(sieve_eratosthenes_iterators(), 10):
        print(prime)

    print(f'\n**Starting Benchmark for num_primes={num_primes}**')
    print(f'Calculating with python-streams...')
    start_ps = time.time()
    sieve_eratosthenes().take(num_primes).to_list()
    end_ps = time.time()
    print(f'python-streams: {end_ps - start_ps} seconds')

    print(f'Calculating with pyfunctional...')
    start_pf = time.time()
    sieve_eratosthenes_pyfunctional().take(num_primes).to_list()
    end_pf = time.time()
    print(f'python-streams: {end_pf - start_pf} seconds')

    print(f'Calculating with builtin iterators...')
    start_it = time.time()
    list(islice(sieve_eratosthenes_iterators(), num_primes))
    end_it = time.time()
    print(f'python-streams: {end_it - start_it} seconds')


if __name__ == '__main__':
    benchmark(10_000)
