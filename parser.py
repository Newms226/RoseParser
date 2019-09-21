import sys
import os
import errors

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
    return abs_path, content

def parse(program, slr, grammar):
    pass


if __name__ == "__main__":
    print(INTRO)

    if len(sys.argv) != 2:
        raise errors.MISSING_SOURCE

    source_path = "./sources/" + sys.argv[1]

    program_path, program = read_file(source_path, errors.SOURCE_ERROR)
    grammar_path, grammar = read_file("./grammar.txt", errors.MISSING_GRAMMAR)
    slr_path, slr = read_file("./slr.csv", errors.MISSSING_SLR)

    print(INPUT.format(program_path, grammar_path, slr_path))
    print("Beginning to parse....\n")
