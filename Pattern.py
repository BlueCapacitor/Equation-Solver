'''
Created on Apr 24, 2019

@author: gosha
'''

from Define_Opperations import symetric_op
from Parser import parse
from Tree import Tree


class Pattern(Tree):

    def matches(self, tree):  # logically wrong (does not account for asymmetric functions)
        if(self.node_type == "constant"):
            return({} if tree.node_type == "constant" and tree.args[0] == self.args[0] else False)

        if(self.node_type == "variable"):
            if(self.args[0] == 'x'):
                return({'x': tree.args[0]} if tree.node_type == "variable" else False)
            else:
                return({self.args[0]: tree.args[0]} if tree.node_type == "constant" else False)

        if(self.node_type == "operation"):
            if(not(tree.node_type == "operation")):
                return(False)

            # later check for + 0 or * 1 or - 0 or / 1
            a = self.args[0].matches(tree.args[0])
            b = self.args[1].matches(tree.args[1])

            if((a is False) or (b is False)):
                a = self.args[0].matches(tree.args[1])
                b = self.args[1].matches(tree.args[0])

                if((a is False) or (b is False)):
                    return(False)

            # possibly try to deal with * 2 = / (1 / 2)

            # check for a + num = a - (- num)

            # maybe check for a - (b - c) = a - b + c

            if(self.node != tree.node):
                return(False)

            d = dict(a)

            for var in b.keys():
                if(var in list(d.keys()) and d[var] != b[var]):
                    return(False)
                d[var] = b[var]

            return(d)

        if(self.node_type == "expression" and tree.node_type == "constant"):
            dash = list(self.node).index('-')
            end = -1
            return({self.node[dash + 1: end]: tree.node} if self.args[0](tree.node) else False)

        return(False)

    def specialCases(self):
        if(self.node_type != "operation"):
            return(dict())
        else:
            options = [{}]

            if(self.args[0].node_type == "variable"):
                if(self.node == '+'):
                    options += [option + {self.args[0].node: 0} for option in options]
                if(self.node == '-'):
                    options += [option + {self.args[0].node: 0} for option in options]
                if(self.node == '*'):
                    options += [option + {self.args[0].node: 0} for option in options]
                if(self.node == '^'):
                    options += [option + {self.args[0].node: 0} for option in options]

                if(self.node == '*'):
                    options += [option + {self.args[0].node: 1} for option in options]
                if(self.node == '^'):
                    options += [option + {self.args[0].node: 1} for option in options]
                if(self.node == '√'):
                    options += [option + {self.args[0].node: 1} for option in options]

            if(self.args[1].node_type == "variable"):
                if(self.node == '+'):
                    options += [option + {self.args[1].node: 0} for option in options]
                if(self.node == '-'):
                    options += [option + {self.args[1].node: 0} for option in options]
                if(self.node == '-'):
                    options += [option + {self.args[1].node: 0} for option in options]
                if(self.node == '^'):
                    options += [option + {self.args[1].node: 0} for option in options]
                if(self.node == '√'):
                    options += [option + {self.args[1].node: 0} for option in options]
                if(self.node == '_'):
                    options += [option + {self.args[1].node: 0} for option in options]

                if(self.node == '*'):
                    options += [option + {self.args[1].node: 1} for option in options]
                if(self.node == '/'):
                    options += [option + {self.args[1].node: 1} for option in options]

    def directMatch(self, eq):
        if(self.node_type == "variable"):
            if(eq.node_type == "operation"):
                return({self.node: eq.copy()})

            return({self.node: eq.node})
        if(self.node_type == "constant"):
            if(eq.node_type not in ["constant"]):
                return(False)

            return({} if closeEnough(self.node, eq.node) else False)

        if(self.node_type == "operation"):
            if(eq.node_type not in ["operation"] or self.node != eq.node):
                return(False)

            a, b = self.args[0].directMatch(eq.args[0]), self.args[1].directMatch(eq.args[1])

            if(a is False or b is False):
                return(False)

            aKeys = a.keys()
            bKeys = b.keys()

            out = b

            for var in aKeys:
                if(var in bKeys):
                    if(a[var].getHash() != b[var].getHash() if (issubclass(type(a[var]), Tree) and issubclass(type(b[var]), Tree)) else b[var] != a[var]):
                        return(False)
                else:
                    out[var] = a[var]

            return(out)


def closeEnough(a, b):
    return(abs(a - b) < 10 ** -12)
