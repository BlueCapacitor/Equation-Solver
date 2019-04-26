'''
Created on Jan 25, 2019

@author: Gosha
'''

from Newtons_Method import Newtons_Method


class NumSolver:
    '''
    classdocs
    '''

    def __init__(self, equation):
        self.eq = equation

    def solve(self, accuracy = 1000000, start = 0, randRange = 1, randRangeExp = 1.1, attemptsMultiplier = 0.01, debug = False, defined_vars = []):
        defined_vars = list(defined_vars)
        variables = self.eq.objects
        undefined_vars = []
        for v in variables:
            if(not(v in defined_vars)):
                undefined_vars.append(v)

        assert len(undefined_vars) == 1, "Solve should only get an equation with 1 undefined variable. Undefined variables detected: %s" % undefined_vars

        return(Newtons_Method(self.eq, undefined_vars[0], accuracy, start, randRange, randRangeExp, attemptsMultiplier, debug))
