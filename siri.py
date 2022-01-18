import os
# Import lexer and parser from ply module
import ply.lex as lex
import ply.yacc as yacc

# List of token types.
tokens = (
    'OPERATE',
    'TYPE'
)


# Token types may be defined as regular expressions, e.g. r'open | close'
def t_OPERATE(t):
    r'open | close'
    return t


def t_TYPE(t):
    r'(document | program | website)'
    if t.value == 'document':
        t.value = 1
    elif t.value == 'program':
        t.value = 2
    elif t.value == 'website':
        t.value = 3
    return t


# Lexer error handling rule (Handle words out of vocabulary)
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Ignore white spaces
t_ignore = ' \t'


# Main parser rule (command)
def p_command(p):
    'command : OPERATE TYPE'
    if p[1] == 'open':
        pass
    elif p[1] == 'close':
        pass


# Syntax error handling rule
def p_error(p):
    print("Syntax error in input!")


#######################################
# Main program

# Build the lexer
lexer = lex.lex()

# Build the parser
parser = yacc.yacc()

# Main loop
while True:
    s = input('What can I do for you? \n')
    if s == 'Bye':
        break
    parser.parse(s)
