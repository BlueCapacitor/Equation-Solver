'''
Created on Jan 25, 2019

@author: Gosha
'''

from Newtons_Method import Newtons_Method


class NumSolver(object):
    '''
    classdocs
    '''

    def __init__(self, equation):
        self.eq = equation

    def solve(self, accuracy=1000000, start=0, randRange=1, randRangeExp=1.1, attemptsMultiplier=0.01, debug=False):
        if(len(self.eq.objects) != 1):
            raise(ValueError("Solve should only get an equation with 1 variable. Variables detected: %s" % self.eq.objects))
        return(Newtons_Method(self.eq, self.eq.objects[0], accuracy, start, randRange, randRangeExp, attemptsMultiplier, debug))
