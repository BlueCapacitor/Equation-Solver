'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import parse
from Pattern import Pattern
from Solver import Solver, NumSolver
import Tree

if __name__ == '__main__':

    variables = {}
    action = ''

    while(True):
        action_input = input("Action: ").lower()
        action = action_input if(action_input != '') else action

        if(action == "<"):
            Tree.notation = "prefix"
            continue

        if(action == "*"):
            Tree.notation = "infix"
            continue

        if(action == ">"):
            Tree.notation = "postfix"
            continue

        if(action == "\\"):
            Tree.integers = True
            continue

        if(action == "."):
            Tree.integers = False
            continue

        if(action == "format"):
            print(Tree.notation + " notation")
            print("integers on" if Tree.integers else "integers off")
            continue

        equation = input("Equation: ")

        if(action[:5] == "solve"):
            if(len(action) > 6):
                v = int(action[6])
            else:
                v = 1

            if(len(action) > 8):
                cap_time = float(action[8:])
            else:
                cap_time = False

            solution = Solver(parse(equation), verbosity = v).solve(cap_time = cap_time)

            if(solution[0] is None):
                print("No solutions found by the numeric solver within the alloted time and reasonable bounds" if cap_time else "No solutions found by the numeric solver within reasonable bounds")
                continue

            if(type(solution[0]) in [set, list, tuple]):
                print(" and ".join(map(lambda x: str(x), solution[0])))
            else:
                print(str(solution[0]))
            if(not(solution[1])):
                print("These solutions may be incomplete" if type(solution[0]) in [set, list, tuple] else "There may be other solutions")
            continue

        if(action == "numsolve"):
            solver = NumSolver(parse(equation))
            print(solver.solve())
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
