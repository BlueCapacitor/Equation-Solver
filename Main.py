'''
Created on Oct 22, 2018

@author: Gosha
'''

import os

from Parser import parse
from Pattern import Pattern
from Simplification import Rule, simplify, applyAllRules
from Solver import Solver, NumSolver
from Symbolic_Calculus import symDerivative
import Tree

LaTeXFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output.txt"
htmlFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output_equation.html"
htmlTemplateFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/html_output_equation_template.html"

latexMode = "html"


def displayEquation(eq):
    print(eq)
    if(Tree.notation == "latex"):
        if(latexMode == "pure LaTeX"):
            f = open(LaTeXFile, 'w')
            f.write(str(eq))
            f.close()
            os.system("osascript ./display_latex.scpt")
        else:
            templatef = open(htmlTemplateFile, 'r')
            template = templatef.read()
            templatef.close()
            f = open(htmlFile, 'w')
            f.write(template.format(*[str(eq)]))
            f.close()


if __name__ == '__main__':

    variables = {}
    action = ''
    lock = False
    lockedAction = None

    while(True):
        action_input = input("Action: ").lower() if lock is False else lockedAction
        action = action_input if(action_input != '') else action

        if(action in ["<", "prefix"]):
            Tree.notation = "prefix"
            continue

        if(action in ["*", "infix"]):
            Tree.notation = "infix"
            continue

        if(action in [">", "postfix"]):
            Tree.notation = "postfix"
            continue

        if(action in ["#l", "latex"]):
            Tree.notation = "latex"
            latexMode = "pure LaTeX"
            continue

        if(action in ["#h", "html"]):
            Tree.notation = "latex"
            latexMode = "html"
            continue

        if(action == "\\"):
            Tree.integers = True
            continue

        if(action == "."):
            Tree.integers = False
            continue

        if(action == "f0"):
            Tree.stringFormat = 0
            continue

        if(action == "f1"):
            Tree.stringFormat = 1
            continue

        if(action == "f2"):
            Tree.stringFormat = 2
            continue

        if(action == "format"):
            print(Tree.notation + " notation")
            print("integers on" if Tree.integers else "integers off")
            continue

        if(action == "lock"):
            lock = True
            lockedAction = input("Action: ")
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
            displayEquation(parse(equation))
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
            displayEquation(eq)
            continue

        if(action == "fit"):
            eq = parse(equation)
            pattern = parse(input("Pattern: "), Pattern)
            displayEquation(pattern.matches(eq))
            continue

        if(action == "dfit"):
            eq = parse(equation)
            pattern = parse(input("Pattern: "), Pattern)
            match = pattern.directMatch(eq)
            if(type(match) == dict):
                print(dict(map(lambda item: (item[0], str(item[1])), match.items())))
            else:
                print(match)
            continue

        if(action == "apply"):
            eq = parse(equation)
            rule = Rule(input("From: "), input("To: "))
            displayEquation(eq.applyToCopy(rule))
            continue

        if(action == "rapply"):
            eq = parse(equation)
            rule = Rule(input("From: "), input("To: "), reversible = True)
            displayEquation(eq.applyToCopy(rule, reverse = True))
            continue

        if(action in ["cost", "getcost", "get cost", "complex", "complexity", "get complexity", "getcomplexity", "cplx"]):
            eq = parse(equation)
            print(eq.getCost())
            continue
        if(action == "hash"):
            eq = parse(equation)
            print(eq.getHash())
            continue

        if(action == "applyall"):
            eq = parse(equation)
            print(list(map(str, applyAllRules(eq))))
            continue

        if(len(action) >= 3 and (action[0:3] == "der" or (len(action.split(' ')) == 2 and action.split(' ')[1][0:3] == "der"))):
            n = 1 if len(action.split(' ')) == 1 else int(action.split(' ')[0])
            eq = parse(equation)
            if(len(eq.objects) > 1):
                respectTo = input("With respect to: ")
            else:
                respectTo = None
            der = symDerivative(eq, respectTo = respectTo, n = n, sim = action[-1] != 'x')
            displayEquation(der)
            continue

        print("Command \"%s\" not recognized" % action)
