"""A Left-Recursive, Top-Down Parser by Michael Newman

Parser uses a list of grammar productions and a SLR lookup table to analyze the
syntax of a given input program.

Assumed directory structure:
    ./
    |- slr.csv
    |- grammar.txt
    |- rose_parser
       |- parser.py
       |- ...
    |- ...

SLR Machine can be generated from
http://jsmachines.sourceforge.net/machines/slr.html

Initial Code from Dr. Thyago Mota at the Metropolitan State University of
Colorado.

Project description located at `design/Prg01.docx`
"""


import os
import sys
import errors

from lookup import lookup
from templates import INTRO, INPUT, SHIFT_REDUCE_CONFLICT, MODE
from token import Token
from syntax import SyntaxAnalyzer


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

    # Log current config for de-bugging
    path = f"./logs/grammar.txt"
    with open(path, 'w') as file:
        file.write("\n".join(_grammar_to_strs(grammar)))

    path = f"./logs/gotos.txt"
    with open(path, 'w') as file:
        file.writelines("\n".join(_dict_to_strs(gotos)))

    path = f"./logs/actions.txt"
    with open(path, 'w') as file:
        file.writelines("\n".join(_dict_to_strs(actions)))

    # read source code input as string
    source_str = source.read()
    source.close()

    # Analyze the code
    analyzer = SyntaxAnalyzer(source_str, grammar, actions, gotos)
    # while True:
    #     response = input(MODE)
    #     if response == 'i':
    #         pass
    #     elif response == 'r':
    #         stack = analyzer.loop()
    #         break
    #     else:
    #         print("Invalid input, try again")

    print("Parsing...")
    stack = analyzer.loop()
    print("Input is syntactically correct!\n\n")

    i = input("Would you like to view the parse tree? ('y' to accept)\n")
    if i == 'y':
        stack.get_frame(-1).cur_trees[0].print("")

    i = input("Would you like to view the parse frames? ('y' to accept)\n")
    if i == 'y':
        print(str(stack))

    print("Goodbye! ^.^")


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


def _examine_shift_reduce_conflict(value, token, state):
    shift, reduce = value.split('/')
    if shift[0] != 's' or reduce[0] != 'r':
        raise Exception(f"Invalid shift/reduction pair: {value}")

    msg = SHIFT_REDUCE_CONFLICT.format(state, token, shift, reduce)

    while True:
        response = input(msg)
        if response == 'r':
            to_return = reduce
            break
        elif response == 's':
            to_return = shift
            break
        else:
            print(f"Invalid input `{response}`, try again")

    return to_return


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
                if '/' in value:
                    value = _examine_shift_reduce_conflict(value, token, i + 1)
                actions[state][token] = value

        # Extract the goto table
        for i, variable in enumerate(variables):
            value = row[i + len(tokens) + 1]
            if len(value) != 0:
                gotos[state][variable] = int(value)

    return actions, gotos


def _dict_to_strs(list_o_dicts):
    for i, d in enumerate(list_o_dicts):
        yield f"{i}:"
        for k, v in d.items():
            yield f"  {k}: {v}"


def _grammar_to_strs(grammar):
    for i, production in enumerate(grammar):
        lhs, rhs = production
        yield f"{i}: {lhs} -> {' '.join(rhs)}"


if __name__ == "__main__":
    main()
