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

    def solve(self, cap_time = False):
        self.p(3, "Solve started")
        self.p(3, "Received equation %s" % str(self.eq))
        self.eq.simplify()
        self.p(2, "Simplify to:")
        self.p(1, self.eq)

        result = self.directRules()
        if(result != None):
            return((result, True))
        else:
            self.p(2, "Attempting to solve numerically")
            solver = NumSolver(self.eq)
            try:
                solution = (solver.solve(cap_time = cap_time), False)
            except(OverflowError):
                return((None, False))
            return(solution)

    def directRules(self):
        for expresion, solutions in direct_rules:
            pattern = parse(expresion, Pattern)
            fits = pattern.matches(self.eq)
            if(fits is not False):
                self.p(2, "Apply %s => x = %s" % (expresion, " and ".join(solutions)))
                return({parse(solution).evaluate(fits) for solution in list(solutions)})
            else:
                self.p(3, "Rule %s => x = %s does not apply" % (expresion, solutions))
        self.p(2, "Failed to find applicable rules")
