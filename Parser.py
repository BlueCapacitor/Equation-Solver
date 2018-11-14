'''
Created on Oct 22, 2018

@author: gosha
'''

from Tree import *


def parse(eq):
    split_eq = fixSyntax(split(eq))

    if(len(eq) == 1):
        if(strType(split_eq[0]) == "operation"):
            raise SyntaxError(split_eq[0])
        else:
            return(tree(split_eq[0]))
    else:
        split_ord_op = splitOrdOp(split_eq)
        op = split_ord_op[1]
        arguments = [parse(split_ord_op[0]), parse(split_ord_op[2])]
        return(tree(op, arguments))


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
    while(True):
        for i in range(len(eq) - 1):
            if(strType(eq[i]) == "number" and strType(eq[i + 1]) == "object"):
                eq = eq[0: i + 1] + ["*"] + eq[i + 1: len(eq)]
                break
        else:
            break

    return(eq)


def splitOrdOp(eq):
    for op in (symbols["operation"][:: -1]):
        if(op in eq):
            i = eq.index(op)
            return([eq[0: i], eq[i], eq[i + 1:]])
