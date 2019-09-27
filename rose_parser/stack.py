from token import Token
import templates


def _stack_to_str(stack):
    for i in stack:
        yield i.name if isinstance(i, Token) else str(i)


class Stack:

    class StackFrame:

        def __init__(self, lexeme, token, action, cur_stack):
            self.lexeme = lexeme
            self.token = token
            self.action = action
            self.cur_state = int(cur_stack[-1])
            self.cur_stack = cur_stack

        def __str__(self):
            stack_str = ", ".join(_stack_to_str(self.cur_stack))

            return templates.stack_frame_template.format(
                self.lexeme, self.token, self.action, stack_str
            )



    # Stack class:
    def __init__(self):
        inital_frame = Stack.StackFrame("BOF", None, None, [0])
        self._frames = [inital_frame]

    def get_raw(self, i): return self._frames[-1].cur_stack[i]

    def get_frame(self, i): return self._frames[i]

    def cur_state(self): return self._frames[-1].cur_state

    def raw_stack(self): return self._frames[-1].cur_stack.copy()


    def append_frame(self, lexeme, token, action, new_stack):
        frame = Stack.StackFrame(lexeme, token, action, new_stack)
        self._frames.append(frame)
        return frame
    #
    # def append_token(self, token, lexeme, action, state):
    #     self._raw.append(token)
    #     self.frames.append({
    #         ""
    #     })
    #
    #     frame = Stack.StackFrame(token, lexeme, action, state, self._raw)
    #     self._frames.append(frame)
    #
    # def append_state(self, state):
    #     self._raw.append(state)
    #
    # def reduce(self, rhs):
    #     rhs_len = len(rhs) * 2
    #     self._raw = self._raw[:-rhs_len]
    #     return self.get(-1)

    def __str__(self):
        return "\n\n".join([str(frame) for frame in self._frames])


