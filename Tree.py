'''
Created on Nov 11, 2018

@author: gosha
'''

symbols = {"blank": [" "],
           "digit": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
           "operation": ['=', '^', '*', '/', '+', '-'],
           "decimal": ['.']}


def strType(s):
    if(s in symbols["blank"]):
        return("blank")

    if(s in symbols["decimal"]):
        return("decimal")

    if(type(s) == int or type(s) == float):
        return("number")
    for c in s:
        if((c not in symbols["digit"]) and c not in symbols["decimal"]):
            break
    else:
        return("number")

    if(s in symbols["operation"]):
        return("operation")

    return("object")


class tree:
    def __init__(self, node, arguments = []):
        self.node = node

        if(strType(node) == "number"):
            self.node_type = "constant"
            self.arguments = [node]

        if(strType(node) == "object"):
            self.node_type = "variable"
            self.arguments = [node]

        if(strType(node) == "operation"):
            self.node_type = "operation"
            self.arguments = arguments


def showTree(t):
    out = ""

    if(t.node_type == "operation"):
        args = [showTree(t2) for t2 in t.arguments]

        out += str(t.node) + '('
        out += str(args[0])
        for arg in args[1:]:
            out += ", " + str(arg)
        out += ')'

    else:
        out = str(t.arguments[0])

    return(out)
