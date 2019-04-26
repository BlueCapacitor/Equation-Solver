'''
Created on Nov 11, 2018

@author: Gosha
'''

from Define_Opperations import symbols, opp_functions, ord_op_numbers


def strType(s):
    if(issubclass(type(s), Tree)):
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

    def show(self, notation = "infix"):  # notations: prefix: =(x, 1), infix: x = 1, postfix: (x, 1)=
        out = ""

        if(self.node_type == "operation"):
            args = [branch.show(notation = notation) for branch in self.args]

            if(not(notation == "infix")):
                out += self.node + '(' if notation == "prefix" else '('
                out += args[0]
                for arg in args[1:]:
                    out += ", " + arg
                out += ')' + self.node if notation == "postfix" else ')'
            else:
                if(self.args[0].node_type == "operation"):
                    leftpar = ord_op_numbers[self.node] > ord_op_numbers[self.args[0].node]
                else:
                    leftpar = False
                if(self.args[1].node_type == "operation"):
                    rightpar = ord_op_numbers[self.node] > ord_op_numbers[self.args[1].node]
                else:
                    rightpar = False

                out += '(' if leftpar else ''
                out += args[0]
                out += ') ' if leftpar else ' '
                out += self.node
                out += ' (' if rightpar else ' '
                out += args[1]
                out += ')' if rightpar else ''

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
        #  check for (1 + a) + 2 = 3 + a

        if(self.node_type == "operation"):
            self.args[0].simplify()
            self.args[1].simplify()

            if(self.args[0].node_type == "constant" and self.args[1].node_type == "constant"):
                self.node_type = "constant"
                self.args = [opp_functions[self.node](self.args[0].args[0], self.args[1].args[0])]

    def __str__(self):
        return(self.show())
