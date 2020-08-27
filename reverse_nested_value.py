'''
doc string
'''


class InvalidFormat(Exception):
    def __init__(self, message):
        super(InvalidFormat, self).__init__(message)


def deserialize(src: str) -> list:
    stack = []
    word = ''
    sentence = []
    open_quote = False

    for char in src:
        if char == '{':
            stack.append('}')
        elif char == '}':
            last = stack.pop() if stack else '#'
            if last != char:
                raise InvalidFormat('Input value supposed to be nested: invalid parentheses.')

        elif char == "'":
            if open_quote:
                sentence.append(word)
                word = ''
            open_quote = not open_quote

        elif char in [' ', ':', '\n']:
            continue
        else:
            if open_quote:
                word += char
            else:
                raise InvalidFormat('Input value supposed to be nested: chacters found outside of quote.')
    if stack or open_quote:
        raise InvalidFormat('Input value supposed to be nested.')

    return sentence


def serialize(words: list, indent: int = 4) -> str:
    out = ''
    padding_stack = []
    padding = ''
    for word in words[:-2]:
        padding += ' ' * indent
        padding_stack.append(padding)
        out += padding + f"'{word}': {{" + '\n'
    padding = padding_stack[-1] if padding_stack else ''
    padding += ' ' * indent
    out += padding + f"'{words[-2]}': '{words[-1]}'" + '\n'
    while padding_stack:
        padding = padding_stack.pop()
        out += padding + '}\n'
    return '{\n' + out + '}'


def reverse_nested_value(input_value: str, indent: int = 4) -> str:
    words = deserialize(input_value)
    words.reverse()
    out = serialize(words, indent)
    return out
