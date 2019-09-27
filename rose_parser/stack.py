from token import Token
import templates


def _stack_to_str(stack):
    for i in stack:
        yield i.name if isinstance(i, Token) else str(i)


class Stack:

    class StackFrame:

        def __init__(self, lexeme, token, action, cur_stack, cur_trees):
            self.lexeme = lexeme
            self.token = token
            self.action = action
            self.cur_state = int(cur_stack[-1])
            self.cur_stack = cur_stack
            self.cur_trees = cur_trees

        def __str__(self):
            stack_str = ", ".join(_stack_to_str(self.cur_stack))

            return templates.STACK_FRAME.format(
                self.lexeme, self.token, self.action, stack_str
            )

    # Stack class:
    def __init__(self):
        initial_frame = Stack.StackFrame("BOF", None, None, [0], [])
        self._frames = [initial_frame]

    def cur_state(self): return self._frames[-1].cur_state

    def cur_frame(self): return self._frames[-1]

    def raw_stack(self): return self._frames[-1].cur_stack.copy()

    def append_frame(self, lexeme, token, action, new_stack, trees):
        frame = Stack.StackFrame(lexeme, token, action, new_stack, trees)
        self._frames.append(frame)
        return frame

    def __str__(self):
        return "\n\n".join([str(frame) for frame in self._frames])


