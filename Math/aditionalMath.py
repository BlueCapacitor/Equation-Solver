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

    def function(value = None, **kwargs):
        if(value != None):
            return(eq.evaluate(guessVarMapping(eq, value)))
        else:
            return(eq.evaluate(kwargs))

    return(function)


def guessVarMapping(eq, value):
    if(len(eq.surfaces) > 0):
        return({eq.surfaces[0]: value})
    else:
        return({})


def cplxRound(x, d = 0):
    if(round(x.imag, d) == 0):
        return(round(x.real, d) if d != 0 else round(x.real))
    if(round(x.real, d) == 0):
        return(round(x.imag, d) * 1j if d != 0 else round(x.imag) * 1j)
    return(round(x, d) + round(x.imag, d) * 1j if d != 0 else round(x) + round(x.imag) * 1j)


def findNiceNumber(n):
    options = [1, 2, 5, 10]
    best = None
    bestScore = 0
    b = 10 ** floor(log10(n))
    for m in options:
        attempt = m * b
        if(attempt == n):
            return(attempt)
        score = 1 / abs(n - attempt)
        if(score > bestScore):
            best = attempt
            bestScore = score

    return(best)
