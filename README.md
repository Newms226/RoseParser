A Left-Recursive, Top-Down Parser by Michael Newman

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

SLR Machine can be generated from [SLR](http://jsmachines.sourceforge.net/machines/slr.html)

Initial Code from Dr. Thyago Mota at the Metropolitan State University of
Colorado.

Project description located at `design/Prg01.docx`.