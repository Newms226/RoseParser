

MISSING_SOURCE = ValueError("ERROR 1: Source File Missing")
SOURCE_ERROR = IOError("ERROR 2: Couldn't open source file")
MISSING_GRAMMAR = IOError("ERROR 4: Couldn't open grammar file")
MISSSING_SLR = IOError("ERROR 5: Missing SLR table file")
EOF_EXPECTED = ValueError("ERROR 6: EOF expected")
NO_IDENT = ValueError("ERROR 7: Identifier expected")
NO_SPECIAL_WORD = ValueError("ERROR 8: Special word missing")
NO_SYMBOL = ValueError("ERROR 9: Symbol Missing")
NO_TYPE = TypeError("ERROR 10: Data type expected")
NO_IDENT_OR_LIT = TypeError("ERROR 11: Identifier or literal value expected")
SYNTAX_ERROR = SyntaxError("ERROR 99: Syntax Error")


class LexProblem(Exception):

    def __init__(self, message=None):
        super(LexProblem, self).__init__()
        init_msg = "ERROR 3: Lexical Error"
        if message:
            init_msg += message
        self.message = init_msg
