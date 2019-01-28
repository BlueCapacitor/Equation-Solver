'''
Created on Jan 25, 2019

@author: gosha
'''

from random import uniform
from math import log10


def Derivative(f, x, variable_name, accuracy=1000):
    y0 = f.evaluate({variable_name: x - (1 / accuracy)})
    y1 = f.evaluate({variable_name: x + (1 / accuracy)})
    dy = y1 - y0
    dx = 2 / accuracy
    return(dy / dx)


def Newtons_Method(f, variable_name, accuracy=1000000, start=0, randRange=1, randRangeExp=1.1, attemptsMultiplier=100):
    while(True):
        x = start + uniform(- randRange, randRange)

        for attempts in range(accuracy * attemptsMultiplier):
            fx = f.evaluate({variable_name: x})
            dfx = Derivative(f, x, variable_name, accuracy)

            if(dfx != 0):
                x -= fx / dfx
            else:
                break

            if(abs(fx) <= 1 / accuracy):
                if(f.evaluate({variable_name: round(x, round(log10(accuracy) / 2))}) <= accuracy):
                    if(f.evaluate({variable_name: round(x)}) <= accuracy):
                        return(round(x))
                    return(round(x, round(log10(accuracy) / 2)))
                else:
                    return(x)

        randRange *= randRangeExp
