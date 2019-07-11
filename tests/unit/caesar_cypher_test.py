from python_streams import Stream, partials, compose4
from python_streams import partials as _


def caesar_cypher(message: str, shift: int) -> str:
    num_letters = (ord('z') - ord('a')) + 1
    ascii_cycle = partials.compose3(
        partials.add(-ord('a')),
        partials.modulo(num_letters),
        partials.add(ord('a')))
    return ''.join(Stream(message).map(ord).map(partials.add(shift)).map(ascii_cycle).map(chr))


def caesar_decypher(encrypted_message: str, shift: int) -> str:
    return caesar_cypher(encrypted_message, -shift)


def caesar_cypher2(message: str, shift: int) -> str:
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    return Stream(message).map_if(
        condition=_.is_in(alphabet),
        func=compose4(alphabet.find, _.add(shift), _.modulo(len(alphabet)), alphabet.__getitem__)
    ).join()


def test_caesar_cypher():
    assert caesar_cypher('hey', 3) == 'khb'
    assert caesar_decypher('wigvix', 4) == 'secret'
    assert caesar_cypher2('hey', 3) == 'khb'
    assert caesar_cypher2('hey hey!', 3) == 'khb khb!'


def caesar_cypher_with_special_chars(message: str, shift: int) -> str:
    a = ord('a')
    z = ord('z')
    num_letters = (z - a) + 1
    ascii_cycle = partials.compose3(
        partials.add(-a),
        partials.modulo(num_letters),
        partials.add(a))
    return ''.join(Stream(message).map(ord).map_if(
        condition=partials.is_in(range(a, z + 1)),
        func=partials.add(shift)
    ).map_if(
        condition=partials.is_in(range(a + shift, z + shift + 1)),
        func=ascii_cycle
    ).map(chr))


def test_caesar_cypher_with_special_chars():
    assert caesar_cypher('hey hey!', 3) != 'khb khb!'
    assert caesar_cypher_with_special_chars('hey hey!', 3) == 'khb khb!'


# def test_get():
#     x = Stream([{'x': 1, 'y': 3}, {'x': 2, 'y': 4}]).map(partials.get('x'))
#     y = Stream([[1, 2], [3, 4]]).map(partials.nth(1))
#     z = partials.nth(3)
