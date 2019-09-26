from tree import Tree
from stack import Stack
from lex import Lexer
from token import Token
import errors


#
# def print_stack(stack):
#     print(", ".join(_stack_to_str(stack)))

err_template = """
ERROR: {}

STATE: {}, TOKEN: {}, LEXEME: {}
POSSIBLE RECOVERY FROM STATE {}:
   {}
   
Would you like to see the stack? ('y' for yes)
>>>
"""


def examine_error(actions, state, token, lexeme, stack):
    # err_lookup = {Token.IDENTIFIER.name: "Identifier expected"}
    filtered = set(actions[state].keys())
    err = _filtered_to_error(filtered)

    msg = err_template.format(err, state, token.name, lexeme, state, filtered)
    response = input(msg)
    if response == 'y':
        print(str(stack))

    raise err


def _filtered_to_error(filtered):
    if filtered == {Token.IDENTIFIER}:
        return errors.NO_IDENT
    elif filtered == {Token.IDENTIFIER, Token.INTEGER_LITERAL, Token.TRUE,
                      Token.FALSE}:
        return errors.NO_IDENT_OR_LIT
    elif filtered == {Token.BOOLEAN_TYPE, Token.INTEGER_TYPE}:
        return errors.NO_TYPE
    elif filtered == {Token.VAR, Token.BEGIN}:
        return errors.NO_SPECIAL_WORD
    elif filtered == {Token.EOF}:
        return errors.EOF_EXPECTED
    elif filtered == {Token.ASSIGNMENT}:
        return errors.NO_SYMBOL
    elif filtered == {Token.LESS, Token.EQUAL, Token.ADDITION,
                      Token.SUBTRACTION, Token.LESS_EQUAL, Token.GREATER_EQUAL,
                      Token.GREATER}:
        return errors.NO_SYMBOL
    else:
        return errors.SYNTAX_ERROR


# def _print_frame(frame):
#     lexeme, token, stack, action = frame
#     print(f"stack: ", end="")
#     print_stack(stack)
#     print(f"current token: {token} read from {lexeme}")
#     print(f"  action: {action}")


def parse(input, grammar, actions, gotos):
    trees = []
    stack = Stack()
    lexer = Lexer(input)

    while True:
        state = stack.get(-1)
        lexeme, token = lexer.cur

        if token in actions[state]:
            action = actions[state][token]
            # print(f"  action: {action}")
        else:
            examine_error(actions, state, token, lexeme, stack)

        # print(stack._frames[-1])
        # print(f"new action: {action}")

        # shift operation
        # noinspection PyUnboundLocalVariable
        if action[0] == 's':
            stack.append_token(token, lexeme, action, state)

            state = int(action[1:])
            stack.append_state(state)

            tree = Tree(token)
            trees.append(tree)

            lexer.pop()

        # reduce operation
        elif action[0] == 'r':
            lhs, rhs = grammar[int(action[1:])]
            stack.reduce(lhs, rhs)

            state = stack.get(-1)
            stack.append_token(lhs, lexeme, action, state)
            stack.append_state(int(gotos[state][lhs]))

            new_tree = Tree(lhs)
            for tree in trees[-len(rhs):]:
                new_tree.add(tree)

            trees = trees[:-len(rhs)]
            trees.append(new_tree)

        # not a shift or reduce operation, must be an "accept" operation
        elif action == "acc":
            lhs, rhs = grammar[0]

            # TODOd #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODOd #8: return the new tree
            return root, stack

        else:
            raise SyntaxError("Bottomed out in syntax.py")
