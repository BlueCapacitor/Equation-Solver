'''
Created on Jan 25, 2019

@author: Gosha
'''

from math import log10
from random import uniform


def Derivative(f, x, variable_name, accuracy = 1000000):
    y0 = f.evaluate({variable_name: x - (1 / accuracy)})
    y1 = f.evaluate({variable_name: x + (1 / accuracy)})
    dy = y1 - y0
    dx = 2 / accuracy
    return(dy / dx)


def Newtons_Method(f, variable_name, accuracy = 1000000, start = 0, randRange = 1, randRangeExp = 1.1, attemptsMultiplier = 0.01, debug = False):
    while(True):
        x = start + uniform(-randRange, randRange)

        for attempt in range(round(accuracy * attemptsMultiplier)):
            try:
                fx = f.evaluate({variable_name: x})
                dfx = Derivative(f, x, variable_name, accuracy)
            except ValueError:
                break

            if(dfx != 0):
                x -= fx / dfx
            else:
                break

            if(abs(fx) <= 1 / accuracy):
                print(x)
                if(abs(f.evaluate({variable_name: round(x, round(log10(accuracy) / 2))})) <= 1 / accuracy):
                    return(round(x, round(log10(accuracy) / 2)))
                else:
                    return(x)

        randRange *= randRangeExp
