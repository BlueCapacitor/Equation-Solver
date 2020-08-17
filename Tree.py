'''
Created on Nov 11, 2018

@author: Gosha
'''

from Define_Opperations import symbols, opp_functions, ord_op_numbers, expressions, special_cases, \
    symetric_op, numbersToSymbols, fastLatexOperations, op_costs

notation = "infix"
integers = True
stringFormat = 2


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
        if(node == None):
            return(None)

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

    def updateObjects(self):
        if(self.node_type == "constant"):
            self.objects = []
        if(self.node_type == "variable"):
            self.objects = [self.node]
        if(self.node_type == "operation"):
            self.objects = []
            for argument in self.args:
                for o in argument.objects:
                    if(not(o in self.objects)):
                        self.objects.append(o)
        if(self.node_type == "expression"):
            self.objects = []

    def show(self, notationOveride = None):  # notations: prefix: =(x, 1), infix: x = 1, postfix: (x, 1)=, latex
        if(notationOveride == None):
            global notation
            currentNotation = notation
        else:
            currentNotation = notationOveride

        out = ""

        if(self.node_type == "operation"):
            args = [branch.show() for branch in self.args]

            if(currentNotation in ["prefix", "postfix"]):
                out += self.node + '(' if currentNotation == "prefix" else '('
                out += args[0]
                for arg in args[1:]:
                    out += ", " + arg
                out += ')' + self.node if currentNotation == "postfix" else ')'
            elif(currentNotation in ["infix", "latex"]):
                if(self.args[0].node_type == "operation"):
                    leftpar = ord_op_numbers[self.node] > ord_op_numbers[self.args[0].node] or ord_op_numbers[self.args[0].node] == 3
                elif(self.args[0].node_type == "constant"):
                    leftpar = (str(self.args[0])[0] == '-') and (ord_op_numbers[self.node] > 1)
                else:
                    leftpar = False
                if(self.args[1].node_type == "operation"):
                    rightpar = ord_op_numbers[self.node] > ord_op_numbers[self.args[1].node] or (self.node not in symetric_op and (ord_op_numbers[self.node] == ord_op_numbers[self.args[1].node]))
                elif(self.args[1].node_type == "constant"):
                    rightpar = (str(self.args[1])[0] == '-') and (ord_op_numbers[self.node] > 1)
                else:
                    rightpar = False

                if(currentNotation == "infix"):
                    out += '(' if leftpar else ''
                    out += args[0]
                    out += ') ' if leftpar else ' '
                    out += self.node
                    out += ' (' if rightpar else ' '
                    out += args[1]
                    out += ')' if rightpar else ''
                elif(currentNotation == "latex"):
                    if(self.node == '^'):
                        rightpar = False
                    if(self.node == '_'):
                        rightpar = True
                        leftpar = False
                    if(self.node == '/'):
                        rightpar = False
                        leftpar = False

                    template = fastLatexOperations[self.node]
                    out = template[0] + '(' * leftpar + str(self.args[0]) + ')' * leftpar + template[1] + '(' * rightpar + str(self.args[1]) + ')' * rightpar + template[2]

                if(stringFormat >= 1 and self.args[0].node_type == "constant" and self.node == '_' and str(args[0]) == 'e'):
                    out = 'ln(' + args[1] + ')' if currentNotation == "infix" else fastLatexOperations['ln'][0] + '(' + args[1] + ')' + fastLatexOperations['ln'][1]

        else:
            if(stringFormat >= 1 and self.node_type == "constant" and round(self.args[0], 12) in list(numbersToSymbols.keys())):
                out = str(numbersToSymbols[round(self.args[0], 12)])
            elif(integers and self.node_type == "constant" and self.args[0] == int(self.args[0])):
                out = str(int(self.args[0]))
            else:
                out = str(self.args[0])

        return(out)

    def evaluate(self, var_values = []):
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

    def condense(self):
        if(self.node_type == "operation"):
            if(not(self.args[0].condense() and self.args[1].condense())):
                return(False)
            if(self.args[0].node_type == "constant" and self.args[1].node_type == "constant"):
                if(self.node == '/' and self.args[1].node == 0):
                    return(False)
                self.set(Tree(opp_functions[self.node](self.args[0].args[0], self.args[1].args[0])))
        return(True)

    def simplifyCopy(self, maxSteps = 200, maxCostRatio = 20):
        from Simplification import simplify
        return(simplify(self, maxSteps = maxSteps, maxCostRatio = maxCostRatio))

    def simplify(self, maxSteps = 200, maxCostRatio = 20):
        from Simplification import simplify
        self.set(simplify(self, maxSteps = maxSteps, maxCostRatio = maxCostRatio))

    def oldSimplify(self, timeout = 100):
        cycleCount = 0
        while(True):
            pself = self.copy()
            while(True):
                self.updateObjects()
                if(self.node_type == "operation"):
                    self.args[0].simplify()
                    self.args[1].simplify()

                    # check for + 0, * 1, etc. (only after modifying pattern to try + 0, * 1, etc.)
                    for case in special_cases:
                        if(self.node == case[0]):
                            if(case[1] == '='):
                                if(str(self.args[0]) == str(self.args[1]) or (self.args[0].node_type == "constant" and self.args[1].node_type == "constant" and (round(self.args[0].args[0], 12) == round(self.args[1].args[0], 12)))):
                                    self.set(self.args[0] if case[4] == 'x' else Tree(case[4]))
                                    break

                            if(case[2]):
                                if(type(case[1]) in [int, float]):
                                    if(self.args[0].args == [case[1]]):
                                        self.set(self.args[1] if case[4] == 'x' else Tree(case[4]))
                                        break
                            if(case[3]):
                                if(type(case[1]) in [int, float]):
                                    if(self.node == case[0]):
                                        if(self.args[1].args == [case[1]]):
                                            self.set(self.args[0] if case[4] == 'x' else Tree(case[4]))
                                            break
                    else:
                        break
                else:
                    break

            self.updateObjects()

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

                elif(self.args[1].node_type == "constant" and self.node in symetric_op):
                    self.args[0], self.args[1] = self.args[1], self.args[0]

            self.updateObjects()

            cycleCount += 1
            if(cycleCount == timeout):
                print("simplification timed-out")
            if(self.args == pself.args or cycleCount == timeout):
                break

        # check for a + 2 * a = 3 * a

        # check for same or compatable operation on both sides of =

    def update(self, var_values):
        if(self.node_type == "variable" and self.node in var_values):
            self.set(var_values[self.node] if issubclass(type(var_values[self.node]), Tree) else Tree(var_values[self.node]))

        elif(self.node_type == "operation"):
            self.args[0].update(var_values)
            self.args[1].update(var_values)

        self.updateObjects()

    def updateCopy(self, var_values):
        out = self.copy()
        out.update(var_values)
        return(out)

    def set(self, other):
        other = other.copy()
        self.node = other.node
        self.node_type = other.node_type
        self.args = other.args
        self.objects = other.objects

    def copy(self):
        out = type(self)(None)
        out.node = self.node
        out.node_type = self.node_type
        if(self.node_type == "operation"):
            out.args = list(map(lambda eq: eq.copy(), self.args))
        else:
            out.args = list(self.args)
        out.objects = list(self.objects)
        return(out)

    def getCost(self):
        if(self.node_type == "operation"):
            c0 = self.args[0].getCost()
            c1 = self.args[1].getCost()
            return((op_costs[self.node] + c0[0] + c1[0], c0[1] + c1[1]))
        if(self.node_type == "variable"):
            return((0, 1))
        return((0, 0))

    def applyToCopy(self, rule, reverse = False):
        out = self.copy()
        out.apply(rule, reverse)
        return(out)

    def apply(self, rule, reverse = False):
        if(not(reverse)):
            assert(rule.fromPattern.directMatch(self) is not False)
            self.set(rule.toPattern.updateCopy(rule.fromPattern.directMatch(self)))
        else:
            assert(rule.toPattern.directMatch(self) is not False)
            self.set(rule.fromPattern.updateCopy(rule.toPattern.directMatch(self)))

        self.updateObjects()

    def getHash(self):
        return(hash(self.show(notationOveride = "prefix")))

    def __str__(self):
        return(self.show())

    def __add__(self, other):
        return(Tree("+", [self, other]))

    def __sub__(self, other):
        return(Tree("-", [self, other]))

    def __mul__(self, other):
        return(Tree('*', [self, other]))

    def __truediv__(self, other):
        return(Tree('/', [self, other]))

    def __pow__(self, other, modulo = None):
        if(modulo != None):
            return(NotImplemented)
        return(Tree('^', [self, other]))
