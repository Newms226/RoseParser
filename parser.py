import sys
import os
import errors

from lex import lex, lookup
from tree import Tree
from token import Token


INTRO = """
Welcome to the RoseParser. Built by Michael Newman from base code by 
Dr. Thyago Mota. This program expects the source as input to the command line 
as 'NAME.pas' which will automatically load from './sources/NAME.pas'.Further, 
it expects the grammar at './grammar.txt' and the SLR table at './slr.csv'.
"""

INPUT = """           
Reading from source code file: {}

Reading from grammar file: {}

Reading from SLR table file: {}
"""


def read_file(path, error):
    abs_path = os.path.abspath(path)

    if os.path.exists(abs_path):
        source = open(abs_path, "rt")
    else:
        raise error

    content = source.read()
    source.close()

    if len(content) == 0:
        raise error

    return abs_path, content


def load_grammar(input):
    grammar = []
    lines = input.split("\n")
    for line in lines:
        # print(f"PARSING LINE: {line}")
        line = line.strip()
        if line != "":
            lhs, rhs = line.split("->")
            lhs = lhs.strip()
            rhs = rhs.strip().split(" ")
            # print(f"PARSED VALUES: lhs: {lhs} rhs: {rhs}")
            grammar.append((lhs, rhs))
    return grammar


# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def load_table(input):
    actions = {}
    gotos = {}
    header = input.readline().strip().split(",")
    end = header.index("$")
    tokens = []
    for field in header[:end]:
        tokens.append(Token[field])
        # tokens.append(int(field))
    print(tokens)
    variables = header[end:]
    for line in input:
        row = line.strip().split(",")
        state = int(row[0])
        for i in range(len(tokens)):
            token = tokens[i]
            key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[key] = value
        for i in range(len(variables)):
            variable = variables[i]
            key = (state, variable)
            value = row[i + len(tokens)]
            if len(value) == 0:
                value = None
            gotos[key] = value
    return actions, gotos


# prints the productions of a given grammar, one per line
def print_grammar(grammar):
    for i, production in enumerate(grammar):
        lhs, rhs = production
        rhs_str = " ".join(rhs)
        print(f"{i}. {lhs} -> {rhs_str}")


# prints the given actions, one per line
def print_actions(actions):
    for key in actions:
        print(key, end = " -> ")
        print(actions[key])


# prints the given gotos, one per line
def print_gotos(gotos):
    for key in gotos:
        print(key, end = " -> ")
        print(gotos[key])


def parse(input, grammar, actions, gotos):
    trees = []
    stack = [0]

    while True:
        state = stack[-1]
        input, lexeme, token = lex(input)
        print(f"stack: {stack} current token: {token}")

        # TODO what should we do if NONE is returned? IE: When EOF is reached

        action = actions[(state, token)]
        print(f"  action: {action}")

        # if action is None:
        #     return None  # tree building update

        # shift operation
        if action[0] == 's':
            # input.pop(0)
            stack.append(token)
            state = int(action[1:])
            stack.append(state)
            tree = Tree(token)  # Should we include the lexeme too?
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            lhs, rhs = grammar[int(action[1:])]
            for i in range(len(rhs) * 2):
                stack.pop()
            state = stack[-1]
            stack.append(lhs)
            stack.append(int(gotos[(state, lhs)]))

            newTree = Tree(lhs)

            # TODOd #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                newTree.add(tree)

            # TODOd #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODOd #6: append the new tree to the list of trees
            trees.append(newTree)

            input = lexeme + " " + input

        # not a shift or reduce operation, must be an "accept" operation
        elif action == "acc":
            lhs, rhs = grammar[0]

            # TODOd #7: same as reduce but using the 1st rule of the grammar
            root = Tree()
            root.data = lhs
            for tree in trees:
                root.add(tree)

            # TODOd #8: return the new tree
            return root

        else:
            raise Exception("Failed :/")

if __name__ == "__main__":
    print(INTRO)

    if len(sys.argv) != 2:
        raise errors.MISSING_SOURCE

    source_path = "./sources/" + sys.argv[1]

    program_path, program = read_file(source_path, errors.SOURCE_ERROR)
    grammar_path, grammar = read_file("./grammar.txt", errors.MISSING_GRAMMAR)

    slr_path = os.path.abspath("./slr.csv")
    try:
        slr = open(slr_path, "r")
    except FileNotFoundError:
        raise errors.MISSING_SLR

    print(INPUT.format(program_path, grammar_path, slr_path))

    grammar = load_grammar(grammar)
    # print_grammar(grammar)

    actions, gotos = load_table(slr)
    print("\n\nActions:")
    print_actions(actions)
    print("\n\nGotos:")
    print_gotos(gotos)

    print("Beginning to parse....\n")
    # parse(program, grammar, actions, gotos)


# # returns the LHS (left hand side) of a given production
# def get_lhs(production):
#     return production.split("->")[0].strip()
#
#
# # returns the RHS (right hand side) of a given production
# def get_rhs(production):
#     return production.split("->")[1].strip().split(" ")
