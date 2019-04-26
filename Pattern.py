'''
Created on Apr 24, 2019

@author: gosha
'''

from Tree import Tree


class Pattern(Tree):

    def matches(self, tree):
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

            #  later check for + 0 or * 1 or - 0 or / 1
            a = self.args[0].matches(tree.args[0])
            b = self.args[1].matches(tree.args[1])

            if((a is False) or (b is False)):
                a = self.args[0].matches(tree.args[1])
                b = self.args[1].matches(tree.args[0])

                if((a is False) or (b is False)):
                    return(False)

            #  possibly try to deal with * 2 = / (1 / 2)

            #  check for a + b = a - (- b)

            #  check for 1 + (2 + 3) = (1 + 2) + 3 (and with *) (probably in Tree simplify because only 1 variable)

            #  maybe check for a - (b - c) = a - b + c

            if(self.node != tree.node):
                return(False)

            d = dict(a)

            for var in b.keys():
                if(var in list(d.keys()) and d[var] != b[var]):
                    return(False)
                d[var] = b[var]

            return(d)

        if(self.node_type == "expression"):
            return({self.node: tree.node} if self.args[0](tree.node) else False)
