from token import Token


def _stack_to_str(stack):
    for i in stack:
        yield i.name if isinstance(i, Token) else str(i)


stack_frame_template = """
Stack: {}
  current token: {} read from {}
  action: {}
"""


class Stack:

    class StackFrame:
        def __init__(self, token, lexeme, action, state, cur_stack):
            self.token = token.name if isinstance(token, Token) else str(token)
            self.lexeme = lexeme
            self.action = action
            self.state = state
            self.cur_stack = cur_stack.copy()

        def __str__(self):
            stack_str = ", ".join(_stack_to_str(self.cur_stack))
            return stack_frame_template.format(stack_str, self.token,
                                               self.lexeme, self.action)

    # Stack class:
    def __init__(self):
        self._raw = [0]
        self._frames = [0]

    def get(self, i):
        return self._raw[i]

    # def get_frame(self, i):
    #     return self._

    def append_token(self, token, lexeme, action, state):
        self._raw.append(token)

        frame = Stack.StackFrame(token, lexeme, action, state, self._raw)
        self._frames.append(frame)

    def append_state(self, state):
        self._raw.append(state)

    def reduce(self, lhs, rhs):
        rhs_len = len(rhs) * 2
        self._raw = self._raw[:-rhs_len]


    def __str__(self):
        return "".join([str(x) for x in self._frames])


