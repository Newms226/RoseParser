# CS3210 - Principles of Programming Languages - Fall 2019
# A Lexical Analyzer for an expression

import sys

from enum import Enum
from errors import gen_lex_problem
from token import Token


# all char classes
class CharClass(Enum):
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR = 4
    BLANK = 5
    COMPOUND_OP = 6
    OTHER = 7


OPERATORS = [";", ".", "+", "-", "*", "=", ":", "<", ">"]

# lexeme to token conversion
lookup = {
    '+': Token.ADDITION,
    ":=": Token.ASSIGNMENT,
    "begin": Token.BEGIN,
    "boolean": Token.BOOLEAN_TYPE,
    "boolean_type": Token.BOOLEAN_TYPE,
    ":": Token.COLON,
    "do": Token.DO,
    "else": Token.ELSE,
    "end": Token.END,
    "=": Token.EQUAL,
    "false": Token.FALSE,
    ">": Token.GREATER,
    ">=": Token.GREATER_EQUAL,
    "if": Token.IF,
    "integer": Token.INTEGER_TYPE,
    "integer_type": Token.INTEGER_TYPE,
    "<": Token.LESS,
    "<=": Token.LESS_EQUAL,
    "*": Token.MULTIPLICATION,
    '.': Token.PERIOD,
    "program": Token.PROGRAM,
    "read": Token.READ,
    ';': Token.SEMICOLON,
    '-': Token.SUBTRACTION,
    "then": Token.THEN,
    "true": Token.TRUE,
    "var": Token.VAR,
    "while": Token.WHILE,
    "write": Token.WRITE,
    "id": Token.IDENTIFIER,
    "$": Token.EOF,
    "integer_lit": Token.INTEGER_LITERAL,

}


# reads the next char from input and returns its class
def get_char(input):
    if len(input) == 0:
        return None, CharClass.EOF
    c = input[0].lower()
    if c.isalpha():
        return c, CharClass.LETTER
    if c.isdigit():
        return c, CharClass.DIGIT
    if c in [':', '>', '<'] and input[1] == '=':
        return str(input[:2]), CharClass.COMPOUND_OP
    if c in OPERATORS:
        return c, CharClass.OPERATOR
    if c in [' ', '\n', '\t']:
        return c, CharClass.BLANK
    # else
    raise gen_lex_problem(f"failed to get_char with c={c}")


# calls getChar and getChar until it returns a non-blank
def get_non_blank(input):
    ignore = ""
    while True:
        c, char_class = get_char(input)
        if char_class == CharClass.BLANK:
            input, _ = add_char(input, ignore)
        else:
            return input


# adds the next char from input to lexeme, advancing the input by one char
def add_char(input, lexeme, count=1):
    if len(input) > 0:
        lexeme += input[:count]
        input = input[count:]
    return (input, lexeme)


# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = get_non_blank(input)

    c, char_class = get_char(input)
    lexeme = ""

    # check EOF first
    if char_class == CharClass.EOF:
        return input, "$", Token.EOF

    # elif char_class == CharClass.LETTER:
    #     input, lexeme = read_ident(lexeme, input)
    #     if lexeme in lookup:
    #         return input, lexeme, lookup[lexeme]
    #     else:
    #         return input, lexeme, Token.IDENTIFIER

    if char_class == CharClass.LETTER:
        while True:
            input, lexeme = add_char(input, lexeme)
            c, char_class = get_char(input)
            if char_class not in [CharClass.LETTER, CharClass.DIGIT]:
                break
        if lexeme in lookup:
            return input, lexeme, lookup[lexeme]
        else:
            return input, lexeme, Token.IDENTIFIER

    elif char_class == CharClass.DIGIT:
        while True:
            input, lexeme = add_char(input, lexeme)
            c, char_class = get_char(input)
            if char_class != CharClass.DIGIT:
                break
        return input, lexeme, Token.INTEGER_LITERAL

    elif char_class == CharClass.OPERATOR:
        input, lexeme = add_char(input, lexeme)
        if lexeme in lookup:
            return input, lexeme, lookup[lexeme]
        else:
            raise Exception(f"Operator '{c}' is not in the lookup!'")

    elif char_class == CharClass.COMPOUND_OP:
        input, lexeme = add_char(input, lexeme, count=2)
        if lexeme in lookup:
            return input, lexeme, lookup[lexeme]
        else:
            raise Exception(f"Compound Operator '{c}' is not in the lookup!'")

    else:

        raise Exception("bottomed out in lex, command flow failure. Dumping." +
                        f"\nc: {c}, class: {char_class}. INPUT:\n{input}")


# main
if __name__ == "__main__":

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


# all reserved words
# RESERVED = {
#     "program": 21 ,
#     "var": 27,
#     "integer": 16,
#     "boolean":4,
#     "begin": 3,
#     "end": 8,
#     "read": 22,
#     "write": 29,
#     "if": 14,
#     "then": 25,
#     "else": 7,
#     "while": 28,
#     "do": 6,
#     "true": 26,
#     "false": 10,
#
#     # operators
#     ";": 23,
#     ".": 20,
#     "+": 1,
#     "-": 24,
#     "*": 19,
#     "=": 9,
#     ":": 5,
#     "<": 17,
#     ">": 11,
# s
#     # compound operators
#     ":=": 2,
#     ">=": 12,
#     "<=": 18,
# }


# 13: identifier
# 15: int_lit
#
# RESERVED_WORDS = ["program", "var", "integer", "boolean", "begin", "end",
#                   "read", "write", "if", "then", "else", "while", "do",
#                   "true", "false"]

