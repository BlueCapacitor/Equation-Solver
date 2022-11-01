'''
Created on Mar 21, 2020

@author: gosha
'''
import copy
import heapq

from Core.defineOpperations import rec, binEncode
from Core.equationParser import parse
from Core.pattern import Pattern
from Core.tree import Tree

rules = []


def addRule(stringFrom, stringTo, reversible = False):
    global rules
    rules.append(Rule(stringFrom, stringTo, reversible))


def applyAllRules(eq):
    global rules

    out = shallowApplyAllRules(eq)

    if(eq.node_type == "operation"):
        out += [Tree(eq.node, [arg0, eq.args[1].copy()]) for arg0 in applyAllRules(eq.args[0])]
        out += [Tree(eq.node, [eq.args[0].copy(), arg1]) for arg1 in applyAllRules(eq.args[1])]

    return(out)


def shallowApplyAllRules(eq):
    global rules

    out = []

    for rule in rules:
        if(rule.check(eq)):
            out.append(eq.applyToCopy(rule))
        if(rule.reversible and rule.check(eq, reverse = True)):
            out.append(eq.applyToCopy(rule, reverse = True))

    return(out)


class Rule:

    def __init__(self, stringFrom, stringTo, reversible = False):
        self.fromPattern = parse(stringFrom, into = Pattern)
        self.toPattern = parse(stringTo, into = Pattern)
        self.reversible = reversible

    def check(self, eq, reverse = False):
        return((self.fromPattern.directMatch(eq) is not False) if not reverse else (self.toPattern.directMatch(eq) is not False))


class HashBank():

    def __init__(self, depth = 50):
        self.depth = depth
        self.hashes = copy.deepcopy(rec([], lambda x: [x] * 2, depth))

    def addHash(self, h, inList = None):
        if(type(h) == int):
            h = binEncode(h, self.depth)

        if(inList == None):
            inList = self.hashes

        if(len(inList) == 0 or type(inList[0]) != list):
            inList.append(h)
        else:
            self.addHash(h, inList[int(h[0])])

    def checkForHash(self, h, inList = None):
        if(type(h) == int):
            h = binEncode(h, self.depth)

        if(inList == None):
            inList = self.hashes

        if(len(inList) == 0 or type(inList[0]) != list):
            return(h in inList)
        else:
            return(self.checkForHash(h, inList[int(h[0])]))

    def checkAndAdd(self, h, inList = None):
        if(type(h) == int):
            h = binEncode(h, self.depth)

        if(inList == None):
            inList = self.hashes

        if(len(inList) == 0 or type(inList[0]) != list):
            if(h not in inList):
                inList.append(h)
                return(False)
            return(True)
        else:
            return(self.checkAndAdd(h, inList[int(h[0])]))


class PriorityQueue():

    def __init__(self):
        self.heap = []

    def isEmpty(self):
        return(len(self.heap) == 0)

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self, quantity = None):
        if(quantity == None):
            return(heapq.heappop(self.heap))
        else:
            return([heapq.heappop(self.heap) for _ in quantity])

    def getMin(self):
        return(self.heap[0])


def simplify(eq, maxSteps = 200, maxCostRatio = 2):
    best = eq.copy()
    best.condense()
    bestCost = eq.getCost()
    queue = PriorityQueue()
    hashes = HashBank()
    queue.push((bestCost, eq.getHash, eq))
    hashes.addHash(eq.getHash())

    step = 0
    while(not(queue.isEmpty()) and (maxSteps == None or step < maxSteps)):
        options = applyAllRules(queue.pop()[2])
        for option in options:
            if(not(option.condense())):
                continue
            cost = option.getCost()
            if(not(hashes.checkAndAdd(option.getHash())) and (maxCostRatio == None or cost < tuple(map(lambda i: i * maxCostRatio, bestCost)))):
                if(cost < bestCost):
                    best = option
                    bestCost = cost
                queue.push((option.getCost(), option.getHash(), option))

        step += 1

    return(best)


# +, -, *, /
addRule('a * 0', '0', False)
addRule('a + 0', 'a', False)
addRule('0 + a', 'a', False)
addRule('a - 0', 'a', False)
addRule('a * 1', 'a', False)
addRule('a / 1', 'a', False)
addRule('a - a', '0', False)
addRule('a / a', '1', False)
addRule('a + a', '2 * a', True)
addRule('a * (-1)', '0 - a', True)
addRule('(-1) * a', '0 - a', True)
addRule('a * b + a * c', 'a * (b + c)', True)
addRule('a * b - a * c', 'a * (b - c)', True)
addRule('a * b', 'b * a', False)
addRule('a + b', 'b + a', False)
addRule('a - (b + c)', '(a - b) - c', True)
addRule('a - (b - c)', '(a - b) + c', True)
addRule('(a + b) + c', 'a + (b + c)', True)
addRule('(a + b) - c', '(a - c) + b', True)
addRule('(a - b) - c', '(a - c) - b', False)
addRule('a / b + c / b', '(a + c) / b', True)
addRule('a / b - c / b', '(a - c) / b', True)
addRule('(a / b) * c', '(a * c) / b', True)
addRule('(a / b) / c', '(a / c) / b', False)
addRule('(a * b) * c', '(a * c) * b', False)
addRule('(a / b) / c', 'a / (b * c)', True)
addRule('a * b + a', '(b + 1) * a', True)
addRule('a * b - a', '(b - 1) * a', True)
addRule('a / b + c', '(a + b * c) / b', False)
addRule('a / b - c', '(a - b * c) / b', False)
addRule('a * b + c', '(a + c / b) * b', False)

# ^
addRule('a ^ 0', '1', False)
addRule('a ^ 1', 'a', False)
addRule('a ^ (-1)', '1 / a', True)
addRule('a * a', 'a ^ 2', False)
addRule('a ^ b * a', 'a ^ (b + 1)', False)
addRule('a ^ b * a ^ c', 'a ^ (b + c)', True)
addRule('(a ^ b) ^ c', 'a ^ (b * c)', True)
addRule('a ^ b', '1 / (a ^ (0 - b))', True)
addRule('1 / (a ^ b)', 'a ^ (0 - b)', True)
addRule('a ^ (b - c)', '(a ^ b) / (a ^ c)', True)
addRule('a ^ b / a', 'a ^ (b - 1)', False)
addRule('a / (a ^ b)', 'a ^ (1 - b)', False)
