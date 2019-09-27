import errors

from templates import ERROR
from tree import Tree
from stack import Stack
from lex import Lexer
from token import Token


class SyntaxAnalyzer:

    def __init__(self, source_code, productions, actions, gotos):
        self.productions = productions
        self.actions = actions
        self.gotos = gotos

        self.stack = Stack()
        self.lexer = Lexer(source_code)
        self.trees = []

        self._is_accepted = False

    def loop(self):
        while not self._is_accepted:
            self.iterate()

        return self.stack

    def iterate(self):
        state = self.stack.cur_state()
        lexeme, token = self.lexer.cur

        if token in self.actions[state]:
            action = self.actions[state][token]
            new_stack = self._act(action)
            self.stack.append_frame(lexeme, token, action, new_stack,
                                    self.trees.copy())
        else:
            self._examine_error()

    def _act(self, action):
        if action[0] == 's':
            new_state = int(action[1:])
            return self._shift(new_state)
        elif action[0] == 'r':
            look_up = int(action[1:])
            return self._reduce(look_up)
        elif action == 'acc':
            return self._accept()
        else:
            raise Exception()

    def _shift(self, new_state):
        _, token = self.lexer.cur

        self.trees.append(Tree(token))
        self.lexer.pop()
        return self.stack.raw_stack() + [token, new_state]

    def _reduce(self, look_up):
        lhs, rhs = self.productions[look_up]

        new_tree = Tree(lhs)
        for tree in self.trees[-len(rhs):]:
            new_tree.add(tree)

        self.trees = self.trees[:-len(rhs)] + [new_tree]

        reduced_stack = self.stack.raw_stack()[:-len(rhs) * 2]
        temp_state = reduced_stack[-1]
        new_state = self.gotos[temp_state][lhs]

        return reduced_stack + [lhs, new_state]

    def _accept(self):
        lhs, rhs = self.productions[0]

        parse_tree = Tree()
        parse_tree.data = lhs
        for tree in self.trees:
            parse_tree.add(tree)

        self._is_accepted = True
        self.trees = [parse_tree]

        return self.stack.raw_stack()

    def _examine_error(self):
        state = self.stack.cur_state()
        filtered = set(self.actions[state].keys())
        lexeme, token = self.lexer.cur
        err = self._filtered_to_error(filtered)

        filtered_str = [token.name for token in filtered]
        msg = ERROR.format(err, state, token.name, lexeme, state,
                           filtered_str)
        response = input(msg)
        if response == 'y':
            print(str(self.stack))
        else:
            print("Raising Error...")

        raise err

    @classmethod
    def _filtered_to_error(cls, filtered):
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
                          Token.SUBTRACTION, Token.LESS_EQUAL,
                          Token.GREATER_EQUAL,
                          Token.GREATER}:
            return errors.NO_SYMBOL
        else:
            return errors.SYNTAX_ERROR
