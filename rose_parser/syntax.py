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


from language import Language


def parse(input, grammar, actions, gotos):
    trees = []
    stack = Stack()
    lexer = Lexer(input)

    while True:
        state = stack.cur_state()
        lexeme, token = lexer.cur

        if token in actions[state]:
            action = actions[state][token]
            new_stack = act(action, stack.raw_stack())
            stack.append_frame(lexeme, token, action, new_stack)
        else:
            examine_error(actions, stack.raw_stack())


def act(action, raw_stack):
    if action[o] == 's':
        return shift()



    # shift operation
    # noinspection PyUnboundLocalVariable
    if action[0] == 's':
        stack.append_token(token, lexeme, action, state)

        state = int(action[1:])
        stack.append_state(state)

        tree = Tree(token)
        trees.append(tree)

        lexer.pop()  # advances the input

    # reduce operation
    elif action[0] == 'r':
        lhs, rhs = grammar[int(action[1:])]
        state = stack.reduce(rhs)

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

        print(stack._frames[-1])


class SyntaxAnalyzer:

    def __init__(self, source_code, productions, actions, gotos):
        self.productions = productions
        self.actions = actions
        self.gotos = gotos

        self.stack = Stack()
        self.lexer = Lexer(source_code)
        self.trees = []



    # def loop(self):
    #     while self.lexer.has_next():
    #         self.iterate()

    def iterate(self):
        state = self.stack.cur_state()
        lexeme, token = self.lexer.cur

        if token in self.actions[state][token]:
            action = self.actions[state][token]
            new_stack = self.act(action)
            return self.stack.append_frame(lexeme, token, action, new_stack)
        else:
            self.examine_error()

    def act(self, action):
        if action[0] == 's':
            new_state = int(action[1:])
            return self.shift(new_state)
        elif action[0] == 'r':
            look_up = int(action[1:])
            return self.reduce(look_up)
        elif action == 'acc':
            pass
        else:
            raise Exception()

    def shift(self, new_state):
        _, token = self.lexer.cur

        self.trees.append(Tree(token))
        self.lexer.pop()
        return self.stack.raw_stack() + [token, new_state]

    def reduce(self, look_up):
        lhs, rhs = self.productions[look_up]

        new_stack = self.stack.raw_stack()[:-len(rhs) * 2]
        new_state = new_stack[-1]

        new_tree = Tree(lhs)
        for tree in self.trees[-len(rhs):]:
            new_tree.add(tree)

        self.trees = self.trees[:-len(rhs)] ++ [new_tree]

        return

    def _reduce_raw(self, rhs):


    def examine_error(self):
        raise Exception()




# def parse(input, lang):
#     trees = []
#     stack = Stack()
#     lexer = Lexer(input)
#
#     while True:
#         state = stack.get(-1)
#         lexeme, token = lexer.cur
#
#         if token in actions[state]:
#             action = actions[state][token]
#             _do_action(action, )
#             # print(f"  action: {action}")
#         else:
#             examine_error(actions, stack)
#
#         # shift operation
#         # noinspection PyUnboundLocalVariable
#         if action[0] == 's':
#             stack.append_token(token, lexeme, action, state)
#
#             state = int(action[1:])
#             stack.append_state(state)
#
#             tree = Tree(token)
#             trees.append(tree)
#
#             lexer.pop()  # advances the input
#
#         # reduce operation
#         elif action[0] == 'r':
#             lhs, rhs = grammar[int(action[1:])]
#             stack.reduce(rhs)
#
#             state = stack.get(-1)
#             stack.append_token(lhs, lexeme, action, state)
#             stack.append_state(int(gotos[state][lhs]))
#
#             new_tree = Tree(lhs)
#             for tree in trees[-len(rhs):]:
#                 new_tree.add(tree)
#
#             trees = trees[:-len(rhs)]
#             trees.append(new_tree)
#
#         # not a shift or reduce operation, must be an "accept" operation
#         elif action == "acc":
#             lhs, rhs = grammar[0]
#
#             # TODOd #7: same as reduce but using the 1st rule of the grammar
#             root = Tree()
#             root.data = lhs
#             for tree in trees:
#                 root.add(tree)
#
#             # TODOd #8: return the new tree
#             return root, stack
#
#         else:
#             raise SyntaxError("Bottomed out in syntax.py")
#
#             print(stack._frames[-1])
