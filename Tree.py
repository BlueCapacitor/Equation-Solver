'''
Created on Nov 11, 2018

@author: Gosha
'''

from Define_Opperations import symbols, opp_functions, ord_op_numbers, expressions, special_cases

notation = "infix"
integers = True


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

    if(s[0] == '$' and s[-1] == '$'):
        return('expression')

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

        if(strType(node) == "expression"):
            self.node_type = "expression"
            start = 1
            dash = list(node).index('-')
            self.args = [expressions[node[start: dash]]]
            self.objects = []

    def show(self):  # notations: prefix: =(x, 1), infix: x = 1, postfix: (x, 1)=
        global notation, integers

        out = ""

        if(self.node_type == "operation"):
            args = [branch.show() for branch in self.args]

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
            if(integers and self.node_type == "constant" and self.args[0] == int(self.args[0])):
                out = str(int(self.args[0]))
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
        return
        while(True):
            if(self.node_type == "operation"):
                self.args[0].simplify()
                self.args[1].simplify()

                # check for + 0, * 1, etc. (only after modifying pattern to try + 0, * 1, etc.)
                for case in special_cases:
                    print(case)
                    if(self.node == case[0]):
                        if(case[2]):
                            if(self.args[0].args[0] == case[1]):
                                if(case[4] == 'x'):
                                    self.set(self.args[1])
                                else:
                                    self.set(Tree(case[4]))
                                    break
                        if(case[3]):
                            print(self.args[1], self.args[1].args)
                            if(self.args[1].args[0] == case[1]):
                                if(case[4] == 'x'):
                                    self.set(self.args[0])
                                else:
                                    self.set(Tree(case[4]))
                                    break
                else:
                    break
            else:
                break

        if(self.node_type == "operation"):
            if(self.node in ['+', '*']):  # extend for - and /
                if(self.args[1].node == self.node and self.args[1].args[0].node_type == "constant"):
                    if(self.args[0].node == self.node):
                        self.args[0].args[1], self.args[1].args[0] = self.args[1].args[0], self.args[0].args[1]
                        self.args[0].simplify()
                    else:
                        self.args[0] = Tree(self.node, [self.args[0], self.args[1].args[0]])
                        self.args[1] = self.args[1].args[1]
                        self.args[0].simplify()

                if(self.args[0].node == self.node and self.args[0].args[1].node_type == "variable"):
                    self.args[1] = Tree(self.node, [self.args[1], self.args[0].args[1]])
                    self.args[0] = self.args[0].args[0]
                    self.args[1].simplify()

            if(self.args[0].node_type == "constant" and self.args[1].node_type == "constant"):
                self.node_type = "constant"
                self.args = [opp_functions[self.node](self.args[0].args[0], self.args[1].args[0])]
                self.node = self.args[0]
                self.objects = []

            elif(self.args[1].node_type == "constant"):
                self.args[0], self.args[1] = self.args[1], self.args[0]

            # check for a + 2 * a = 3 * a

            # check for same or compatable operation on both sides of =

    def update(self, var_values):
        if(self.node_type == "variable" and self.node in var_values):
            self.set(var_values[self.node] if type(var_values[self.node]) == Tree else Tree(var_values[self.node]))

        elif(self.node_type == "operation"):
            arg0 = self.args[0].update(var_values)
            arg1 = self.args[1].update(var_values)

    def set(self, other):
        self.node = other.node
        self.node_type = other.node_type
        self.args = other.args
        self.objects = other.objects

    def __str__(self):
        return(self.show())
