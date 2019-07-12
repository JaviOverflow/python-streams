# Python Streams

## Getting started

```bash
pip install python-streams
```

```python
from streams import Stream
Stream(('hello', 'world')).for_each(print)
```

## Example

```python
from streams import Stream, compose4
from streams import partials as _


def caesar_cypher(message: str, shift: int) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return Stream(message).map_if(
        condition=_.is_in(alphabet),
        func=compose4(alphabet.find, _.add(shift), _.modulo(len(alphabet)), alphabet.__getitem__)
    ).join()
```
Result:
```
caesar_cypher('hey there!', 5)
Out[3]: 'mjd ymjwj!'
```

Here for each letter in the message if it's in the alphabet then we get it's position in the alphabet, add the shift, apply the modulo operator to cycle back to the start and finally access the letter in that position on the alphabet.

Let's attempt an alternate implementation to show some more features:
```python
from itertools import cycle

from streams import Stream, compose
from streams import partials as _


def caesar_cypher(message: str, shift: int) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = Stream(cycle(alphabet)).drop(shift).take(len(alphabet)).to_list()
    return Stream(message).map_if(
        condition=_.is_in(alphabet),
        func=compose(alphabet.find, shifted_alphabet.__getitem__),
    ).join()
```

Here we create a shifted alphabet. For example, if shift is 5 then shifted_alphabet will be `'fghijklmnopqrstuvwxyzabcde'`. That way each letter at position `i` in the alphabet corresponds to the letter at the same position `i` in the shifted alphabet. Knowing this we just need to find the position of each letter, then access the shifted letter at that position.

## Motivation
Python has always lacked a modern rich functional streams API over lists, maps and tuples. Some attempts have been done such as [PyFunctional](https://github.com/EntilZha/PyFunctional), but after being users of those libraries for a some times, we felt the lack of some core features that are hard to add without a redesign of the whole library.

## Guidelines
- Support for latest typing Python 3.6+ features.
- Implement methods from already successful streams API such as the ones already existing in modern languages as Kotlin or Swift. Rich operators suit is always best than poor due to the lack of function extension in Python.
- Support for multiple argument lambdas in order to handle streams of tuples.
- Concurrency design when possible such in operations as map or filter.
