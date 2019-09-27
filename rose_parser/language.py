import json
import time


class Language:
    def __init__(self, grammar, actions, gotos):
        self.grammar = grammar
        self.actions = actions
        self.gotos = gotos

        self.log()

    def to_json(self):
        return {
            "grammar": self.grammar,
            "actions": self.actions,
            "gotos": self.gotos
        }

    def log(self):
        path = f"./logs/lang_{time.time()}.json"
        with open(path, 'w') as log_file:
            json.dump(self.to_json(), log_file, indent=4)


