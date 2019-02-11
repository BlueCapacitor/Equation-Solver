'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import parse
from Numeric_Solver import NumSolver as Solver
import Unittest

if __name__ == '__main__':
    while(True):
        do = input("Action: ")

        equation = input("Equation: ")
        if(do.lower() == "solve"):
            print(Solver(parse(equation)).solve(debug=False))
            continue

        if(do.lower() == "parse"):
            print(parse(equation).show())
            continue

        print("Command \"%s\" not recognized" % do)
