'''
Created on Oct 22, 2018

@author: Gosha
'''

from Define_Opperations import fixSymbols, ord_op
from Tree import Tree, strType


def parse(eq, into = Tree):
    split_eq = fixSyntax(split(eq))
    return(parenthesesLoop(split_eq, into = into))


def parenthesesLoop(eq, into = Tree):
    if(not(eq.__contains__('('))):
        return(parseLoop(eq, into = into))
    else:
        r = innerPar(eq)
        parsed_eq = parseLoop(eq[r[0]: r[1]], into = into)
        insrt = eq[:r[0] - 1] + [parsed_eq] + eq[r[1] + 1:]
        return(parenthesesLoop(insrt, into = into))


def parseLoop(eq, into = Tree):
    eq = cutRedundantPar(eq)

    if(len(eq) == 1):
        if(strType(eq[0]) == "operation"):
            raise SyntaxError(eq[0])
        elif(strType(eq[0]) == "Tree"):
            return(eq[0])
        else:
            return(into(eq[0]))
    else:
        split_ord_op = splitOrdOp(eq)
        op = split_ord_op[1]
        arguments = [parseLoop(split_ord_op[0], into = into), parseLoop(split_ord_op[2], into = into)]
        return(into(op, arguments))


def split(eq):
    out = list(eq)
    while True:
        number_started = False

        for i in range(len(out)):
            if(len(out) > 1):
                pass

            str_type = strType(out[i])

            if(str_type == "blank"):
                del(out[i])
                break

            if(str_type == "number" or str_type == "decimal"):
                if(number_started):
                    out[i - 1] += out.pop(i)
                    break
                else:
                    number_started = True
            else:
                number_started = False
        else:
            break

    for i in range(len(out)):
        if(strType(out[i]) == "number"):
            out[i] = float(out[i])

    return(out)


def fixSyntax(eq):
    if(len(eq) <= 1):
        return(eq)

    if(eq[0] == '-' and
       (strType(eq[1]) == "number")):
        eq[1] = 0 - eq[1]
        del eq[0]

    for key in fixSymbols.keys():
        while(True):
            for i in range(len(eq) - len(key) + 1):
                if(eq[i: i + len(key)] == list(key)):
                    eq[i] = fixSymbols[key]
                    del(eq[i + 1: i + len(key)])
                    break
            else:
                break

    while(True):
        if('$' in eq):
            start = eq.index('$')
            end = eq[start + 1:].index('$') + start + 1
            eq[start] = ''.join(eq[start: end + 1])
            del(eq[start + 1: end + 1])
        else:
            break

    while(True):
        for i in range(len(eq) - 1):
            if((strType(eq[i]) == "number" and strType(eq[i + 1]) == "object") or (strType(eq[i]) == "object" and strType(eq[i + 1]) == "object")):
                eq = eq[0: i + 1] + ["*"] + eq[i + 1: len(eq)]
                break
        else:
            break

    while(True):
        for i in range(len(eq) - 2):
            if(strType(eq[i]) == "operation" and
               eq[i + 1] == '-' and
               strType(eq[i + 2]) == "number"):
                eq = eq[0: i + 1] + [0 - eq[i + 2]] + eq[i + 3: len(eq)]
                break
        else:
            break

    return(eq)


def splitOrdOp(eq):
    for ops in (ord_op[::-1]):
        maximum = 0
        for op in ops:
            if(op in eq and len(eq) - 1 - eq[::-1].index(op) > maximum):
                maximum = len(eq) - 1 - eq[::-1].index(op)

        if(maximum > 0):
            return([eq[0: maximum], eq[maximum], eq[maximum + 1:]])


def innerPar(eq):
    out = (0, len(eq) - 1)
    score = 0
    max_score = 0
    open_index = 0

    for i in range(len(eq)):
        p = eq[i]

        if(p == '('):
            open_index = i
            score += 1

        if(p == ')'):
            if(score >= max_score):
                max_score = score
                out = (open_index + 1, i)
                score -= 1

    return(out)


def cutRedundantPar(eq):
    eq = list(eq)
    for i in range(len(eq) - 2):
        if(eq[i] == '(' and eq[i + 2] == ')'):
            del(eq[i + 2])
            del(eq[i])
            return(cutRedundantPar(eq))

    return(eq)
