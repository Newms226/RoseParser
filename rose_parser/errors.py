
MISSING_SOURCE = ValueError("ERROR 1: Source File Missing")
SOURCE_ERROR = IOError("ERROR 2: Couldn't open source file")
LEX_ERROR = SyntaxError("ERROR 3: Lexical Error")
MISSING_GRAMMAR = IOError("ERROR 4: Couldn't open grammar file")
MISSING_SLR = IOError("ERROR 5: Missing SLR table file")
EOF_EXPECTED = ValueError("ERROR 6: EOF expected")
NO_IDENT = ValueError("ERROR 7: Identifier expected")
NO_SPECIAL_WORD = ValueError("ERROR 8: Special word missing")
NO_SYMBOL = ValueError("ERROR 9: Symbol Missing")
NO_TYPE = TypeError("ERROR 10: Data type expected")
NO_IDENT_OR_LIT = TypeError("ERROR 11: Identifier or literal value expected")
SYNTAX_ERROR = SyntaxError("ERROR 99: Syntax Error")


def with_msg(error, msg):
    print(msg)
    return error

