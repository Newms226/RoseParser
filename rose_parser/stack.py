from token import Token


def _stack_to_str(stack):
    for i in stack:
        yield i.name if isinstance(i, Token) else str(i)


class Stack:

    class StackFrame:
        def __init__(self, token, lexeme, action, state, cur_stack):
            self.token = token
            self.lexeme = lexeme
            self.action = action
            self.state = state
            self.cur_stack = cur_stack.copy()

        def __str__(self):
            return f"""
                Stack: {", ".join(_stack_to_str(self.cur_stack))}
                  current token: {self.token.name} read from {self.lexeme}
                  action: {self.action}
                """

    # Stack class:
    def __init__(self):
        self._raw = [0]
        self._frames = []

    def get(self, i):
        return self._raw[i]

    def append_token(self, token, lexeme, action, state):
        self._raw.append(token)

        frame = Stack.StackFrame(token, lexeme, action, state, self._raw)
        self._frames.append(frame)

    def append_state(self, state):
        self._raw.append(state)

    def reduce(self, lhs, rhs):
        rhs_len = len(rhs) * 2
        to_reduce = [x for x in self._raw[-rhs_len:] if not isinstance(x, int)]

        if to_reduce == rhs:
            self._raw = self._raw[:-rhs_len]
            self._raw.append(lhs)
        else:
            raise SyntaxError(f"""
                Failed to reduce. 
                  Attempted to reduce rhs `{rhs}` into `{lhs}`
                  to_reduce {to_reduce} != rhs
                  Current state: 
                {str(self)}
                """)

    def __str__(self):
        return "\n".join([str(x) for x in self._raw])


