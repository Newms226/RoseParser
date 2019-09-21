# lex.py
## Flow:
    - parses the input by lexeme/token
        * raises a LexicalError if code cannot be understood
## Issues/Concerns
    - it should be a method **not a loop**
    
    
# General Flow
    1. Load in source code
    2. Parser calls lex for the next token
        a. Valid token reply
        b. Raise Lex error if lexically incorrect
    3. Parser sends lex.py the valid token
    4. Lex analyzes the token
        a. peforms a reduce operation
            * looks up & pushes the next state onto its stack
            * calls lex() WITH THE CURRENT TOKEN and resumes oppperation
        b. performs a shift operation
            * pushes the token and state onto its stack
            * command flow returns to step 2
        c. Encounters an error and reports to Parser, moving to err
        
    err. Analyzes the error and displays it to the user
    
    
# Errors
    
1. Source file missing
    - happens in parser#main if the source file does not exist in the expected
      directory
2. Couldn’t open source file
    - happens in parser#main if the file cannot be read
3. Lexical error
    - happens in lex.py if the analyzer cannot understand the token
    ? Use cases? IE: When would this happen?
        * invalid token (just put something in there)
        * WATCH OUT for spaces and the like.
        * variable with a name like 4bob
4. Couldn’t open grammar file
    - happens in parser#main if no valid grammar file is present
5. Couldn’t open SLR table file
    - happens in parser#main if no valid SLR file is present 
6. EOF expected
    - happens if anything occurs after the .
    - THOUGHT:
        * lex can recoginze this. Once it encounters `end.` then we can assume
          that if there is anything following this, we can throw an error.
        * shortcut? When reading the input:
            a. find the end of the program IE: `end.`
            b. check to see if there are any NONBLANK chars after.
                TRUE: fail immedately and throw an exception
                FALSE: continue to parse.
7. Identifier expected
    - happens when there
8
Special word missing
9
Symbol missing
10
Data type expected
11
Identifier or literal value expected
99
Syntax error

    