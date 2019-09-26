

class Stack:


    def __init__(self):
        self._raw = [0]
        self._frames = []

    def get(self, i):
        return self._raw[i]

    def append_token(self, token, lexeme, action, state):
        self._raw.append(token)
        self._frames += self._define_frame(token, lexeme, action, state)

    def append_state(self, state):
        self._raw.append(state)

    # TODO: this method should check the stack to make sure every second item matches!
    def pop(self, n, multiplier=2):
        for _ in range(len(n * multiplier)):
            self._raw.pop()

    def copy(self):
        copy = Stack()
        for x in self._raw:
            copy.append(x)
        return copy

    def _define_frame(self, content):
        self._frames.append(int(content))

    def _define_complex_frame(self, token, lexeme, action, state):
        return {
            "state": state,
            "action": action,
            "lexeme": lexeme,
            "token": token
        }

    def _print_frame(self):
        pass

