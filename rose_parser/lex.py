from enum import Enum

from token import Token
from lookup import lookup
import errors as errors
from errors import LEX_ERROR


class CharClass(Enum):
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR = 4
    PUNCTUATOR = 5
    QUOTE = 6
    BLANK = 7
    COMPOUND_OP = 8
    OTHER = 9


class Lexer:
    def __init__(self, input):
        self.cur = None
        self._input = input
        self._read()

    def pop(self): self._read()

    def has_next(self):
        _, char_class = get_char(self._input)
        return self.cur is not None and char_class != CharClass.EOF

    def _read(self):
        _input, lexeme, token = lex(self._input)
        self._input = _input
        self.cur = (lexeme, token)


def get_char(input):
    if len(input) == 0:
        return None, CharClass.EOF
    c = input[0].lower()
    if c.isalpha():
        return c, CharClass.LETTER
    elif c.isdigit():
        return c, CharClass.DIGIT
    elif c in [':', '>', '<'] and input[1] == '=':
        return str(input[:2]), CharClass.COMPOUND_OP
    elif c in ['+', '-', '*', '/', '>', '=', '<']:
        return c, CharClass.OPERATOR
    elif c in ['.', ':', ',', ';']:
        return c, CharClass.PUNCTUATOR
    elif c in [' ', '\n', '\t']:
        return c, CharClass.BLANK
    else:
        msg = f"Could not classify the char {c} :/"
        raise errors.with_msg(LEX_ERROR, msg)


def add_char(input, lexeme, count=1):
    if len(input) >= count:
        lexeme += input[:count]
        input = input[count:]
        return input, lexeme
    else:
        msg = f"Failed in add_char. Count: {count}, lexeme: {lexeme}, " \
              f"input: {input}"
        raise errors.with_msg(LEX_ERROR, msg)


def get_non_blank(input):
    ignore = ""
    while True:
        c, char_class = get_char(input)
        if char_class == CharClass.BLANK:
            input, _ = add_char(input, ignore)
        else:
            return input


def _read_letter(input):
    lexeme = ""
    while True:
        input, lexeme = add_char(input, lexeme)
        c, char_class = get_char(input)
        if char_class not in [CharClass.LETTER, CharClass.DIGIT]:
            break
    return input, lexeme


def _read_digit(input):
    lexeme = ""

    while True:
        input, lexeme = add_char(input, lexeme)
        c, char_class = get_char(input)
        if char_class != CharClass.DIGIT:
            break

    return input, int(lexeme)


def _lexeme_to_token(lexeme):
    if lexeme in lookup:
        return lookup[lexeme]
    else:
        msg = f"{lexeme}' is not in the lookup!"
        raise errors.with_msg(LEX_ERROR, msg)


# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = get_non_blank(input)
    c, char_class = get_char(input)

    if char_class == CharClass.EOF:
        return input, None, Token.EOF

    elif char_class == CharClass.LETTER:
        input, lexeme = _read_letter(input)
        token = lookup[lexeme] if lexeme in lookup else Token.IDENTIFIER
        return input, lexeme, token

    elif char_class == CharClass.DIGIT:
        input, lexeme = _read_digit(input)
        return input, lexeme, Token.INTEGER_LITERAL

    elif char_class == CharClass.COMPOUND_OP:
        input, lexeme = add_char(input, "", count=2)
        token = _lexeme_to_token(lexeme)
        return input, lexeme, token

    elif char_class in [CharClass.OPERATOR, CharClass.PUNCTUATOR]:
        input, lexeme = add_char(input, "")
        token = _lexeme_to_token(lexeme)
        return input, lexeme, token

    else:
        msg = "bottomed out in lex, command flow failure. Dumping." + \
              f"\nc: {c}, class: {char_class}. INPUT:\n{input}"
        raise errors.with_msg(LEX_ERROR, msg)


# For testing purposes
if __name__ == "__main__":
    import sys

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if not lexeme:
            break
        output.append((lexeme, token))

        # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)
