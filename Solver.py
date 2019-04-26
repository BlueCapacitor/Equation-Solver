'''
Created on Jan 25, 2019

@author: Gosha
'''

from Define_Opperations import direct_rules, Base
from Numeric_Solver import NumSolver
from Parser import parse
from Pattern import Pattern


class Solver(Base):

    def __init__(self, equation, verbosity = 0):
        self.eq = equation
        self.verbosity = verbosity
        self.p(3, "Solver init complete")

    def solve(self):
        self.p(3, "Solve started")
        self.eq.simplify()
        self.p(2, "Simplify to:")
        self.p(1, self.eq)

        result = self.directRules()
        if(result != None):
            self.p(1, result)
            return(result)
        else:
            solver = NumSolver(self.eq)
            return(solver.solve)

    def directRules(self):
        for expresion, solution in direct_rules.items():
            pattern = parse(expresion, Pattern)
            fits = pattern.matches(self.eq)
            if(fits is not False):
                self.p(2, "Apply %s => x = %s" % (expresion, solution))
                return(parse(solution).evaluate(fits))
