import os
import speech_recognition as sr
# Import lexer and parser from ply module
import ply.lex as lex
import ply.yacc as yacc

# List of token types.
tokens = (
    'OPERATE',
    'NAME',
    'TYPE'
)


# Token types may be defined as regular expressions, e.g. r'open | close'
def t_OPERATE(t):
    r'open | close'
    return t


def t_NAME(t):
    r'\w+\s'
    return t


def t_TYPE(t):
    r'document | program | website'
    return t


# Lexer error handling rule (Handle words out of vocabulary)
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Ignore white spaces
t_ignore = ' \t'


# Main parser rule (command)
def p_command(p):
    'command : OPERATE NAME TYPE'
    if p[1] == 'open':
        if p[3] == 'program':
            os.system("start " + p[2])
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

r = sr.Recognizer()

with sr.Microphone() as source:
    audio = r.record(source, duration=4)
    try:
        s = r.recognize_google(audio)
        print(s.capitalize() + ".")
    except:
        print("Sorry could not recognize your voice")
    parser.parse(s.lower())
