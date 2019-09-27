STACK_FRAME = """\
Read input `{}` as token `{}`"
  action: {}
New Stack: {}"""

INTRO = """\
Welcome to the RoseParser. 

Built by Michael Newman from base code by Dr. Thyago Mota. This program expects
the input source as the first command line argument. A non ambiguous, LR 
grammar file is expected at './grammar.txt'. A valid SLR parse table is 
expected at './slr.csv'.
"""

INPUT = """\
Reading from source code file: {}

Reading from grammar file: {}

Reading from SLR table file: {}
"""

SHIFT_REDUCE_CONFLICT = """\
SHIFT REDUCE CONFLICT

Found a shift reduce conflict in state row {} for token {}
Shift: {}
Reduce: {}

Would you like to reduce? ('r')
Or shift? ('s')
>>>"""

ERROR = """\
ERROR: {}

STATE: {}, TOKEN: {}, LEXEME: {}
POSSIBLE RECOVERY FROM STATE {}:
   {}
   
Would you like to see the stack? ('y' for yes)
>>>"""

MODE = """\
Language has been loaded and logged at `./logs`

How would you like to proceed?
  'i' for interactive mode (examine the parser frame before continuing)
  'r' for regular
>"""