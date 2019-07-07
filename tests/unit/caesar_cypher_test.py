from python_streams import Stream, partials


def caesar_cypher(message: str, shift: int) -> str:
    num_letters = (ord('z') - ord('a')) + 1
    ascii_cycle = partials.compose3(
        partials.add(-ord('a')),
        partials.modulo(num_letters),
        partials.add(ord('a')))
    return ''.join(Stream(message).map(ord).map(partials.add(shift)).map(ascii_cycle).map(chr))


def caesar_decypher(encrypted_message: str, shift: int) -> str:
    return caesar_cypher(encrypted_message, -shift)


def test_caesar_cypher():
    assert caesar_cypher('hey', 3) == 'khb'
    assert caesar_decypher('wigvix', 4) == 'secret'


# def test_get():
#     x = Stream([{'x': 1, 'y': 3}, {'x': 2, 'y': 4}]).map(partials.get('x'))
#     y = Stream([[1, 2], [3, 4]]).map(partials.nth(1))
#     z = partials.nth(3)
