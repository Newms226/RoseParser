import os
import sys

from lookup import lookup
from token import Token
import errors
import syntax

INTRO = """
Welcome to the RoseParser. 

Built by Michael Newman from base code by Dr. Thyago Mota. This program expects
the input source as the first command line argument. A non ambiguous, LR 
grammar file is expected at './grammar.txt'. A valid SLR parse table is 
expected at './slr.csv'.
"""

INPUT = """           
Reading from source code file: {}

Reading from grammar file: {}

Reading from SLR table file: {}
"""


def _open_file(path, error=None):
    abs_path = os.path.abspath(path)

    if os.path.exists(abs_path):
        source = open(abs_path, "r")
    else:
        raise error

    if not source:
        raise error

    return abs_path, source


def _load_grammar(input):
    grammar = []

    for line in input:
        # print(f"PARSING LINE: {line}")
        line = line.strip()
        if line != "":
            lhs, rhs = line.split("->")
            lhs = lhs.strip()
            rhs = rhs.strip().split(" ")
            # print(f"PARSED VALUES: lhs: {lhs} rhs: {rhs}")
            grammar.append((lhs, rhs))

    return grammar

def _load_table(input):
    actions = []
    gotos = []
    tokens = []

    headers = input.readline().strip().split(",")
    end = headers.index("$")
    variables = headers[end + 1:]

    # Read Headers
    for field in [x.lower() for x in headers[1:end + 1]]:
        if field in lookup:
            tokens.append(lookup[field])
        else:  # assume token
            tokens.append(Token[field])

    for line in input:
        actions += [{}]
        gotos += [{}]

        row = line.strip().split(",")
        state = int(row[0])

        # Extract the tokens and their operations
        for i, token in enumerate(tokens):
            value = row[i + 1]
            if len(value) != 0:
                actions[state].update({token: value})

        # Extract the goto table
        for i, variable in enumerate(variables):
            value = row[i + len(tokens) + 1]
            if len(value) != 0:
                gotos[state].update({variable: value})

    return actions, gotos


def _dict_to_strs(list_o_dicts):
    for i, d in enumerate(list_o_dicts):
        yield f"{i}:"
        for k, v in d.items():
            yield f"  {k}: {v}"


def _grammar_to_strs(grammar):
    for production in grammar:
        lhs, rhs = production
        yield f"{lhs} -> {' '.join(rhs)}"


def _log(grammar, actions, gotos):
    def _file_dump(lines, name):
        path = f"./logs/{name}.txt"
        file = open(path, "w")
        file.write(f"{name}:\n\n")
        for line in lines:
            file.write(line + "\n")

    os.makedirs("./logs", exist_ok=True)
    _file_dump(_dict_to_strs(gotos), 'GOTOS')
    _file_dump(_dict_to_strs(actions), 'ACTIONS')
    _file_dump(_grammar_to_strs(grammar), 'GRAMMAR')


def main():
    print(INTRO)

    if len(sys.argv) < 2:
        raise errors.MISSING_SOURCE

    program_path, source = _open_file(sys.argv[1], errors.MISSING_SOURCE)
    grammar_path, grammar = _open_file("./grammar.txt", errors.MISSING_GRAMMAR)
    slr_path, slr = _open_file('./slr.csv', errors.MISSING_SLR)

    print(INPUT.format(program_path, grammar_path, slr_path))

    grammar = _load_grammar(grammar)
    actions, gotos = _load_table(slr)

    # read program as string
    program = source.read()
    source.close()

    _log(grammar, actions, gotos)

    _ = input("Config loaded. Logs generated. See ./logs for "
              "gotos, actions, and grammar. \nPress enter to continue")
    print("Beginning to parse...\n\n")

    tree, frames = syntax.parse(program, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!\n\n")

        i = input("Would you like to view the parse tree? ('y' to accept)\n>")
        if i == 'y':
            tree.print("")

        i = input("\nWould you like to view the parse frames? ('y' to accept)\n")
        if i == 'y':
            for frame in frames:
                syntax._print_frame(frame)
    else:
        print("Code has syntax errors!")



if __name__ == "__main__":
    main()
