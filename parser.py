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

    lhs, _ = grammar[2]
    grammar[2] = (lhs, ["EXPR", ";", "STMT"])  # TODO THIS IS SOOO BAD :(
    return grammar


# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def load_table(input):
    actions = []
    gotos = []
    headers = input.readline().strip().split(",")
    end = headers.index("EOF")
    tokens = []
    for field in headers[:end + 1]:
        tokens.append(Token[field])
        # tokens.append(int(field))
    print(tokens)
    variables = headers[end:]

    # for i in range(tokens):
    #     actions ++ [{}

    for line in input:
        actions += [{}]
        gotos += [{}]
        row = line.strip().split(",")
        state = int(row[0])
        # print(f"parsing line {line}")
        actions[state].update({Token.EOF: None})
        assert Token.EOF in actions[state]
        for i, token in enumerate(tokens):
            # key = (state, token)
            value = row[i + 1]
            if len(value) == 0:
                value = None
            actions[state].update({token: value})
        for i, variable in enumerate(variables):
            # key = (state, variable)
            value = row[i + len(tokens)]
            if len(value) == 0:
                value = None
            gotos[state].update({variable: value})
    return actions, gotos


# prints the productions of a given grammar, one per line
def print_grammar(grammar):
    for i, production in enumerate(grammar):
        lhs, rhs = production
        rhs_str = " ".join(rhs)
        print(f"{i}. {lhs} -> {rhs_str}")


# prints the given actions, one per line
def print_actions(actions):
    for i, a in enumerate(actions):
        print(f"{i}:")
        for k, v in a.items():
            print(f"  {k}: {v}")


# prints the given gotos, one per line
def print_gotos(gotos):
    for key in gotos:
        print(key, end=" -> ")
        print(gotos[key])

def examine_error(actions, state, token, lexme):
    # err_lookup = {Token.IDENTIFIER.name: "Identifier expected"}
    filtered = [k for k, v in actions[state].items() if v is not None]
    print(f"\nERROR LIKELY. STATE: {state}, TOKEN: {token.name}, LEXEME: {lexme}"
          f"\nPOSSIBLE RECOVERY:\n  {filtered}\n\n")

    if filtered == [Token.IDENTIFIER]:
        raise errors.NO_IDENT
    elif filtered == [Token.IDENTIFIER, Token.TRUE, Token.FALSE, Token.INTEGER_LITERAL]:
        raise errors.NO_IDENT_OR_LIT
    else:
        raise errors.SYNTAX_ERROR

    # names = [k.name for k in filtered]



def parse(input, grammar, actions, gotos):
    trees = []
    stack = [0]

    accept = False
    while not accept:
        state = stack[-1]
        input, lexeme, token = lex(input)
        print(f"stack: {stack} \n  current token: {token}")

        # TODO what should we do if NONE is returned? IE: When EOF is reached

        action = actions[state][token]
        print(f"  action: {action}")

        if action is None:
            examine_error(actions, state, token, lexeme)
            return None


        # shift operation
        elif action[0] == 's':
            # input.pop(0)
            stack.append(token)
            state = int(action[1:])
            stack.append(state)
            tree = Tree(token)  # Should we include the lexeme too?
            trees.append(tree)

        # reduce operation
        elif action[0] == 'r':
            lhs, rhs = grammar[int(action[1:])]
            print(f"read rhs: {' '.join(rhs)}")
            for i in range(len(rhs) * 2):
                stack.pop()
            print(f"new stack: {stack}")
            state = stack[-1]
            stack.append(lhs)
            print(f"reading state: {state}, lhs: {lhs}")
            stack.append(int(gotos[state][lhs]))

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
    # print_actions(actions)
    print("\n\nGotos:")
    # print_gotos(gotos)
    # print_actions(gotos)
    #
    print("Beginning to parse....\n")
    tree = parse(program, grammar, actions, gotos)

    if tree:
        print("Input is syntactically correct!")
        print("\nParse Tree:")
        tree.print("")
    else:
        print("Code has syntax errors!")

# # returns the LHS (left hand side) of a given production
# def get_lhs(production):
#     return production.split("->")[0].strip()
#
#
# # returns the RHS (right hand side) of a given production
# def get_rhs(production):
#     return production.split("->")[1].strip().split(" ")
