'''
Created on Nov 11, 2018

@author: Gosha
'''

from Define_Opperations import *


def strType(s):
    if(type(s) == tree):
        return("tree")

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

    if(s in symbols["parentheses"]):
        return("parentheses")

    return("object")


class tree:
    def __init__(self, node, arguments=[]):
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

    def show(self):
        out = ""

        if(self.node_type == "operation"):
            args = [branch.show() for branch in self.arguments]

            out += str(self.node) + '('
            out += str(args[0])
            for arg in args[1:]:
                out += ", " + str(arg)
                out += ')'

        else:
            out = str(self.arguments[0])

        return(out)

    def evaluate(self, varValues):
        if(self.node_type == "constant"):
            return(self.node)
        elif(self.node_type == "variable"):
            return(varValues[self.node])
        else:
            arg0 = self.arguments[0].evaluate(varValues)
            arg1 = self.arguments[1].evaluate(varValues)

            if(self.node == "="):
                return(arg0 - arg1)
            else:
                return(opp_functions[self.node](arg0, arg1))
