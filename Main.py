'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import parse
from Pattern import Pattern
from Solver import Solver as Solver
from Tree import notation, integers

if __name__ == '__main__':

    variables = {}
    action = ''

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

        if(action == "\\"):
            integers = True
            continue

        if(action == "."):
            integers = True
            continue

        equation = input("Equation: ")

        if(action[:5] == "solve"):
            if(len(action) > 6):
                v = int(action[6])
            else:
                v = 1
            print(Solver(parse(equation), verbosity = v).solve())
            continue

        if(action == "parse" or action == "show"):
            print(parse(equation).show())
            continue

        if(action == "eval" or action == "evaluate" or action == "find"):
            solution = parse(equation).evaluate(variables)
            if(int(solution) == solution):
                print(int(solution))
            else:
                print(solution)
            continue

        if(action == "set" or action == "var" or action == "variable" or action == "assign" or action == "="):
            name = input("variable name: ")
            variables[name] = parse(equation).evaluate(variables)

            if(int(variables[name]) == variables[name]):
                print("%s = %s" % (name, int(variables[name])))
            else:
                print("%s = %s" % (name, variables[name]))
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
