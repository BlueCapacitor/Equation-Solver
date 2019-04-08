'''
Created on Oct 22, 2018

@author: Gosha
'''

import sys
import traceback

from Numeric_Solver import NumSolver as Solver
from Parser import parse

if __name__ == '__main__':

    variables = {}
    action = ''

    while(True):
        action_input = input("Action: ").lower()
        action = action_input if(action_input != '') else action

        equation = input("Equation: ")
        if(action == "solve"):
            print(Solver(parse(equation)).solve(debug = False))
            continue

        if(action == "parse" or action == "show"):
            print(parse(equation).show())
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

        print("Command \"%s\" not recognized" % action)
