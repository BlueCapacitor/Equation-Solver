'''
Created on Feb 28, 2020

@author: Gosha
'''

from math import *
from random import *


def derivative(f, x = None, dx = 10 ** (-2.81)):
    if(x == None):
        return(lambda x: derivative(f, x, dx))
    else:
        return((f(x + dx) - f(x - dx)) / (2 * dx))


def nDerivative(f, n, x = None, dx = 10 ** (-2.81)):
    if(n == 0):
        if(x == None):
            return(f)
        else:
            return(x)
    return(derivative(nDerivative(f, n - 1, None, dx), x, dx))


def resilientDerivative(f, x = None, dx = 10 ** (-2.81)):
    if(x == None):
        return(lambda x: derivative(f, x, dx))
    else:
        for a, b in [(x + dx, x - dx), (x + dx, x), (x, x - dx), (x + dx, x + 0.5 * dx), (x - 0.5 * dx, x - dx)]:
            try:
                return((f(a) - f(b)) / (a - b))
            except Exception:
                pass
        raise("Could not take derivative of %s at %s" % (f, x))


def integral(f, a = 0, b = None, c = 0, dx = 0.0001):
    if(b == None):
        return(lambda x: integral(f, a, x))
    elif(a < b):
        return(sum(map(f, fRange(a, b, dx))) * dx + c)
    else:
        return(-sum(map(f, fRange(a, b, -dx))) * dx + c)


def solveDifEquation(f, ix, iy):
    return(integral(f, a = ix, c = iy))


def fRange(start, stop, step):
    r = stop - start
    newStop = round(r / step)
    return([x * step + start for x in range(0, newStop)])


def clamp(n, m, M):
    return(min(M, max(m, n)))


def gradDis(f, xi, dx = 10 ** (-2.81), acceptedSlope = 0.0001):
    df = resilientDerivative(f, dx = dx)
    x = xi
    while(True):
        try:
            slope = df(x)
            if(abs(slope) <= acceptedSlope):
                return(x)
            x -= slope * 0.01
        except Exception:
            return(x)


def equationToFunction(eq):
    if(len(eq.objects) == 0):
        return(lambda: eq.evaluate())
    elif(len(eq.objects) == 1):
        return(lambda val: eq.evaluate(list(val.items) if type(val) == dict else guessVarMapping(eq, val)))
    else:
        return(lambda **varValues: eq.evaluate(varValues))


def guessVarMapping(eq, value):
    return({eq.objects[0]: value})
