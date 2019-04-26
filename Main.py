'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import parse
from Pattern import Pattern
from Solver import Solver as Solver

if __name__ == '__main__':

    variables = {}
    action = ''
    notation = "infix"

    while(True):
        action_input = input("Action: ").lower()
        action = action_input if(action_input != '') else action

        if(action == "<"):
            notation = "prefix"
            continue

        if(action == "*"):
            notation = "infix"
            continue

        if(action == ">"):
            notation = "postfix"
            continue

        equation = input("Equation: ")
        if(action[:5] == "solve"):
            if(len(action) > 6):
                v = int(action[5])
            else:
                v = 2
            if(v != 0):
                Solver(parse(equation), verbosity = v).solve()
            else:
                print(Solver(parse(equation), verbosity = v).solve())
            continue

        if(action == "parse" or action == "show"):
            print(parse(equation).show(notation = notation))
            continue

        if(action == "eval" or action == "evaluate" or action == "find"):
            print(parse(equation).evaluate(variables))
            continue

        if(action == "set" or action == "var" or action == "variable" or action == "assign" or action == "="):
            name = input("variable name: ")
            variables[name] = parse(equation).evaluate(variables)
            print("%s = %s" % (name, parse(equation).evaluate(variables)))
            continue

        if(action[:3] == "sim"):
            eq = parse(equation)
            eq.simplify()
            print(eq.show())
            continue

        if(action == "fit"):
            eq = parse(equation)
            pattern = parse(input("Pattern: "), Pattern)
            print(pattern.matches(eq))
            continue

        print("Command \"%s\" not recognized" % action)
