'''
Created on Nov 11, 2018

@author: Gosha
'''

from Define_Opperations import symbols, opp_functions


def strType(s):
    if(type(s) == Tree):
        return("Tree")

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


class Tree:

    def __init__(self, node, arguments = []):
        self.node = node

        if(strType(node) == "number"):
            self.node_type = "constant"
            self.args = [node]
            self.objects = []

        if(strType(node) == "object"):
            self.node_type = "variable"
            self.args = [node]
            self.objects = [self.node]

        if(strType(node) == "operation"):
            self.node_type = "operation"
            self.args = arguments
            self.objects = []
            for argument in arguments:
                for o in argument.objects:
                    if(not(o in self.objects)):
                        self.objects += o

    def show(self):
        out = ""

        if(self.node_type == "operation"):
            args = [branch.show() for branch in self.args]

            out += str(self.node) + '('
            out += str(args[0])
            for arg in args[1:]:
                out += ", " + str(arg)
                out += ')'

        else:
            out = str(self.args[0])

        return(out)

    def evaluate(self, var_values):
        if(self.node_type == "constant"):
            return(self.node)
        elif(self.node_type == "variable"):
            return(var_values[self.node])
        else:
            arg0 = self.args[0].evaluate(var_values)
            arg1 = self.args[1].evaluate(var_values)

            if(self.node == "="):
                return(arg0 - arg1)
            else:
                return(opp_functions[self.node](arg0, arg1))

    def simplify(self):
        if(self.node_type == "operation"):
            self.args[0].simplify()
            self.args[1].simplify()

            if(self.args[0].node_type == "constant" and self.args[1].node_type == "constant"):
                self.node_type = "constant"
                self.args = [opp_functions[self.node](self.args[0].args[0], self.args[1].args[0])]
