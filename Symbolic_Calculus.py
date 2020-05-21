'''
Created on Mar 17, 2020

@author: Gosha
'''

from math import e

from Tree import Tree


def checkConstant(eq, respectTo = None):
    if(respectTo == None):
        return(len(eq.objects) == 0)
    return(respectTo not in eq.objects)


def sym1stDerivative(eq, respectTo = None, sim = True):
    if(sim):
        eq.simplify(maxSteps = 8 * eq.getCost()[0])

    if(respectTo == None):
        if(len(eq.objects) == 1):
            respectTo = eq.objects[0]
        elif(len(eq.objects) > 1):
            raise Exception("ambiguous variable of derivation: ")

    if(checkConstant(eq, respectTo)):  # constant rule
            return(Tree(0))

    if(eq.node_type == "variable"):
        if(eq.node == respectTo):  # identity rule
            return(Tree(1))
        else:
            return(Tree(0))  # constant rule

    if(eq.node_type == "operation"):
        a = eq.args[0]
        b = eq.args[1]
        der = lambda eq: sym1stDerivative(eq, respectTo = respectTo, sim = sim)

        if(eq.node == '+'):  # adition rule
            if(checkConstant(a, respectTo)):
                out = (der(b))
            elif(checkConstant(b, respectTo)):
                out = (der(a))
            else:
                out = (der(a) + der(b))

        if(eq.node == '-'):  # subtraction rule
            if(checkConstant(a, respectTo)):
                out = (Tree(0) - der(b))
            elif(checkConstant(b, respectTo)):
                out = (der(a))
            else:
                out = (der(a) - der(b))

        if(eq.node == '*'):
            if(checkConstant(a, respectTo)):
                out = (a * der(b))
            elif(checkConstant(b, respectTo)):
                out = (b * der(a))
            else:
                out = (der(a) * b + der(b) * a)

        if(eq.node == '/'):
            if(checkConstant(b, respectTo)):
                out = (der(a) / b)
            elif(checkConstant(a, respectTo)):
                out = (Tree(0) - der(b) / (b ** Tree(2)))
            else:
                out = ((der(a) * b - der(b) * a) / (b ** Tree(2)))

        if(eq.node == '^'):
            if(checkConstant(a, respectTo)):
                out = (eq * Tree('_', [Tree(e), a]) * der(b))
            elif(checkConstant(b, respectTo)):
                out = (b * a ** (b - Tree(1)) * der(a))
            else:
                out = (a ** b * (der(b) * Tree('_', [Tree(e), a]) + der(a) * b / a))

        if(eq.node == '_'):
            if(checkConstant(a, respectTo)):
                out = (der(b) / (b * Tree('_', [Tree(e), a])))
            else:
                out = (der(Tree('_', [Tree(e), b]) / Tree('_', [Tree(e), a])))

        if(eq.node == '√'):
            out = (der(b ** (Tree(1) / a)))

    if(sim):
        out.simplify(maxSteps = max(out.getCost()[0], 30))
    return(out)


def symDerivative(eq, n = 1, respectTo = None, sim = True):
    for _ in range(n):
        eq = sym1stDerivative(eq, respectTo = respectTo, sim = sim)
    return(eq)
