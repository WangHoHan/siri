from gtts import gTTS
import os
import playsound
import speech_recognition as sr
import subprocess
import webbrowser
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
        if p[3] == 'document':
            dir_path = os.path.dirname(os.path.realpath(__file__))
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    if file.startswith(p[2].strip(" ")):
                        os.startfile(root + '/' + str(file))
        elif p[3] == 'program':
            os.system("start " + p[2])
        elif p[3] == 'website':
            webbrowser.open_new_tab(p[2].strip(" ") + ".com")
    elif p[1] == 'close':
        os.system("TASKKILL /F /IM " + p[2].strip(" ") + ".exe")


# Syntax error handling rule
def p_error(p):
    print("Syntax error in input!")


def speak(text):
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


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
        if s.lower() == "hey siri":
            print(s.title())
            speak("aha")
            audio = r.record(source, duration=4)
            s = r.recognize_google(audio)
            print(s.capitalize() + ".")
    except:
        print("Sorry could not recognize your voice")
    parser.parse(s.lower())
