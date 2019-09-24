import sys
import os
from errors import *

from lex import lex, lookup
from tree import Tree
from token import Token

INTRO = """
Welcome to the RoseParser. Built by Michael Newman from base code by 
Dr. Thyago Mota. This program expects the source as input to the command line 
as 'NAME.pas' which will automatically load from './ources/NAME.pas'.Further, 
it expects the grammar at './grammar.txt' and the SLR table at './lr.csv'.
"""

INPUT = """           
Reading from source code file: {}

Reading from grammar file: {}

Reading from SLR table file: {}
"""

class Flags(Enum):
    LEX_ERROR = 0

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
    # grammar[2] = (lhs, ["EXPR", ";", "STMT"])  # TODO THIS IS SOOO BAD :(
    return grammar


# reads the given input containing an SLR parsing table and returns the "actions" and "gotos" as dictionaries
def load_table(input):
    actions = []
    gotos = []
    headers = input.readline().strip().split(",")
    end = headers.index("$")
    tokens = []
    for field in [x.lower() for x in headers[1:end + 1]]:
        if field in lookup:
            tokens.append(lookup[field])
        else:  # assume token
            tokens.append(Token[field])
        # tokens.append(int(field))
    print(tokens)
    variables = headers[end + 1:]

    # for i in range(tokens):
    #     actions ++ [{}

    for line in input:
        actions += [{}]
        gotos += [{}]
        row = line.strip().split(",")
        state = int(row[0])
        # print(f"parsing line {line}")
        # actions[state].update({Token.EOF: None})
        # assert Token.EOF in actions[state]
        for i, token in enumerate(tokens):
            # key = (state, token)
            value = row[i + 1]
            if len(value) != 0:
                if '/' in value:
                    value = Flags.LEX_ERROR
                    # raise Exception(f"Invalid table construction. Found {value} at {i +1} in {line}")
                # value = None
                actions[state].update({token: value})
        for i, variable in enumerate(variables):
            # key = (state, variable)
            value = row[i + len(tokens) + 1]
            if len(value) != 0:
                # value = None
                gotos[state].update({variable: value})
    return actions, gotos


# prints the productions of a given grammar, one per line
def print_grammar(grammar):
    for i, production in enumerate(grammar):
        lhs, rhs = production
        rhs_str = " ".join(rhs)
        print(f"{i}. {lhs} -> {rhs_str}")

def _gen_dict(actions):
    for i, a in enumerate(actions):
        yield f"{i}:"
        for k, v in a.items():
            yield f"  {k}: {v}"
# prints the given actions, one per line
def print_dict(actions):
    for line in _gen_dict(actions):
        print(line)
#
#
# error_lookup = {
#     :
#         Errors.NO_IDENT,
#     :
#         Errors.NO_IDENT_OR_LIT
#     # {}
#
#
# }


def examine_error(actions, state, token, lexme, flags=[]):
    # err_lookup = {Token.IDENTIFIER.name: "Identifier expected"}
    filtered = set(actions[state].keys())
    print(f"\nERROR. STATE: {state}, TOKEN: {token.name}, LEXEME: {lexme}"
          f"\nPOSSIBLE RECOVERY FROM STATE {state}:\n  {filtered}\n")

    if filtered == {Token.IDENTIFIER}:
        raise Errors.NO_IDENT
    elif filtered == {Token.IDENTIFIER, Token.INTEGER_LITERAL, Token.TRUE, Token.FALSE}:
        raise Errors.NO_IDENT_OR_LIT
    elif filtered == {Token.BOOLEAN_TYPE, Token.INTEGER_TYPE}:
        raise Errors.NO_TYPE
    elif filtered == {Token.VAR, Token.BEGIN}:
        raise Errors.NO_SPECIAL_WORD
    elif filtered == {Token.EOF}:
        raise Errors.EOF_EXPECTED
    elif Flags.LEX_ERROR in flags:
        raise Errors.LEX_ERROR
    else:
        raise Errors.SYNTAX_ERROR

    # names = [k.name for k in filtered]



def print_stack(stack):
    def _gen():
        for i in stack:
            yield i.name if isinstance(i, Token) else str(i)

    print(", ".join(_gen()))


def parse(input, grammar, actions, gotos):
    trees = []
    stack = [0]

    accept = False
    while not accept:
        state = stack[-1]
        input, lexeme, token = lex(input)
        print(f"stack: ", end="")
        print_stack(stack)
        print(f"current token: {token} read from {lexeme}")

        # TODO what should we do if NONE is returned? IE: When EOF is reached
        if token in actions[state]:
            action = actions[state][token]
            print(f"  action: {action}")
            if action is Flags.LEX_ERROR:
                examine_error(actions, state, token, lexeme, [Flags.LEX_ERROR])
                # return None

        else:
            examine_error(actions, state, token, lexeme)
            # return None

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
            # print(f"read rhs: {' '.join(rhs)}")
            for i in range(len(rhs) * 2):
                stack.pop()
            # print(f"new stack: {stack}")
            state = stack[-1]

            stack.append(lhs)
            # print(f"reading state: {state}, lhs: {lhs}")
            stack.append(int(gotos[state][lhs]))

            new_tree = Tree(lhs)

            # TODOd #4: get "len(rhs)" trees from the right of the list of trees and add each of them as child of the new tree you created, preserving the left-right order
            for tree in trees[-len(rhs):]:
                new_tree.add(tree)

            # TODOd #5: remove "len(rhs)" trees from the right of the list of trees
            trees = trees[:-len(rhs)]

            # TODOd #6: append the new tree to the list of trees
            trees.append(new_tree)

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

def _file_dump(dict, name):
    path = f"./logs/{name}.txt"
    file = open(path, "w")
    file.write(f"{name}\n\n")
    for line in _gen_dict(dict):
        file.write(line + "\n")


if __name__ == "__main__":
    print(INTRO)

    if len(sys.argv) != 2:
        raise Errors.MISSING_SOURCE

    # TODO: Edit the intro, just loads a normal file path

    program_path, program = read_file(sys.argv[1], Errors.SOURCE_ERROR)
    grammar_path, grammar = read_file("./grammar.txt", Errors.MISSING_GRAMMAR)

    slr_path = os.path.abspath("./slr.csv")
    try:
        slr = open(slr_path, "r")
    except FileNotFoundError:
        raise Errors.MISSING_SLR

    print(INPUT.format(program_path, grammar_path, slr_path))

    grammar = load_grammar(grammar)
    # print_grammar(grammar)


    actions, gotos = load_table(slr)

    os.makedirs("./logs", exist_ok=True)
    _file_dump(gotos, "gotos")
    _file_dump(actions, "actions")

    # print(f"\n\nActions:")
    # print_dict(actions)
    # print(f"\n\nGotos:")
    # print_dict(gotos)
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
