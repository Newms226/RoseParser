from tree import Tree
from lex import Lexer
from token import Token
import errors


def print_stack(stack):
    def _gen():
        for i in stack:
            yield i.name if isinstance(i, Token) else str(i)

    print(", ".join(_gen()))


def examine_error(actions, state, token, lexme):
    # err_lookup = {Token.IDENTIFIER.name: "Identifier expected"}
    filtered = set(actions[state].keys())
    print(f"\nERROR. STATE: {state}, TOKEN: {token.name}, LEXEME: {lexme}"
          f"\nPOSSIBLE RECOVERY FROM STATE {state}:\n  {filtered}\n")

    if filtered == {Token.IDENTIFIER}:
        raise errors.NO_IDENT
    elif filtered == {Token.IDENTIFIER, Token.INTEGER_LITERAL, Token.TRUE, Token.FALSE}:
        raise errors.NO_IDENT_OR_LIT
    elif filtered == {Token.BOOLEAN_TYPE, Token.INTEGER_TYPE}:
        raise errors.NO_TYPE
    elif filtered == {Token.VAR, Token.BEGIN}:
        raise errors.NO_SPECIAL_WORD
    elif filtered == {Token.EOF}:
        raise errors.EOF_EXPECTED
    elif filtered == {Token.ASSIGNMENT}:
        raise errors.NO_SYMBOL
    elif filtered == {Token.LESS, Token.EQUAL, Token.ADDITION, Token.SUBTRACTION, Token.LESS_EQUAL, Token.GREATER_EQUAL, Token.GREATER}:
        raise errors.NO_SYMBOL
    else:
        raise errors.SYNTAX_ERROR


def parse(input, grammar, actions, gotos):
    trees = []
    stack = [0]
    lexer = Lexer(input)

    while True:
        state = stack[-1]
        lexeme, token = lexer.cur
        print(f"stack: ", end="")
        print_stack(stack)
        print(f"current token: {token} read from {lexeme}")

        if token in actions[state]:
            action = actions[state][token]
            print(f"  action: {action}")
        else:
            examine_error(actions, state, token, lexeme)

        # shift operation
        if action[0] == 's':
            stack.append(token)

            state = int(action[1:])
            stack.append(state)

            tree = Tree(token)
            trees.append(tree)

            lexer.pop()

        # reduce operation
        elif action[0] == 'r':
            lhs, rhs = grammar[int(action[1:])]
            # print(f"read rhs: {' '.join(rhs)}")
            for i in range(len(rhs) * 2):
                stack.pop()
            # print(f"new stack: {stack}")
            state = stack[-1]

            stack.append(lhs)
            stack.append(int(gotos[state][lhs]))

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
            return root

        else:
            raise errors.with_msg(errors.BAD_SLR, "Bottomed out in syntax.py")
