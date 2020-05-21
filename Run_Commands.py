'''
Created on Apr 18, 2020

@author: Gosha
'''

from Graph import *
from Parser import parse

commandParser = exec


def run():
    commandF = open("./commands", 'r')
    commands = pythonify(commandF.read())

    commandParser(commands)

    turtle.listen()
    turtle.mainloop()


def pythonify(commands):
    while(True):  # var |= equation
        for start in range(len(commands) - 1):
            if(commands[start: start + 2] == '|='):
                for end in range(start + 1, len(commands)):
                    if(commands[end] == '\n'):
                        break
                else:
                    raise SyntaxError("error after '|='")
                break
        else:
            break

        commands = commands[:start] + "= parse(\"" + commands[start + 2: end] + "\")" + commands[end:]

    while(True):  # |equation|
        for start in range(len(commands)):
            if(commands[start] == '|'):
                for end in range(start + 1, len(commands)):
                    if(commands[end] == '|'):
                        break
                else:
                    raise SyntaxError("unmatched '|' on line %s of commands" % (1 + sum(map(lambda c: c == '\n', commands[:start]))))
                break

        else:
            break

        commands = commands[:start] + "parse(\"" + commands[start + 1: end] + "\")" + commands[end + 1:]

    return(commands)
