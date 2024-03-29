'''
Created on Jan 25, 2019

@author: Gosha
'''

from math import pi, e, log

symbols = {"blank": [" "],
           "digit": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
           "operation": ['_', '√', '^', '*', '/', '+', '-', '='],
           "decimal": ['.'],
           "parentheses": ['(', ')']}

expressions = {"int": lambda x: int(x) == x,
               "even": lambda x: int(x / 2) == x / 2,
               "odd": lambda x: int((x + 1) / 2) == (x + 1) / 2}

fixSymbols = {"pi": pi, 'π': pi,
              'e': e,
              'i': 1j,
              '÷': '/', ':': '/',
              "log": '_', 'lg': '_',
              "rt": '√', "root": '√',
              "pow": '^', "exp": '^'}

latexOperations = {'+': "{0}+{1}",
                   '-': "{0}-{1}",
                   '*': "{0}*{1}",
                   '/': "\\frac{{{0}}}{{{1}}}",
                   '^': "{{{0}}}^{{{1}}}",
                   '_': "\log_{0}{{({1})}}",
                   '√': "\sqrt[{0}]{{{1}}}",
                   'ln': "\ln{{({0})}}"}
fastLatexOperations = {'+': ['', '+', ''],
                       '-': ['', '-', ''],
                       '*': ['', '*', ''],
                       '/': ["\\frac{", "}{", "}"],
                       '^': ["{", "}^{", "}"],
                       '_': ["\\log_{", "}{", "}"],
                       '√': ["\\sqrt[", "]{", "}"],
                       'ln': ["\\ln{", "}"]}

numbersToSymbols = {round(e, 12): 'e', round(pi, 12): 'π'}

add = lambda a, b: a + b
sub = lambda a, b: a - b
mult = lambda a, b: a * b
div = lambda a, b: a / b
exp = lambda a, b: a ** b
lg = lambda a, b: log(b, a)
root = lambda a, b: b ** (1 / a)

revsub = lambda a, b: b - a
revdiv = lambda a, b: b / a
revlog = lambda a, b: log(a, b)
revexp = lambda a, b: b ** a

opp_functions = {'^': exp, '_': lg, '√': root, '*': mult, '/': div, '+': add, '-': sub, '=': sub}
opp_symbols = {value: key for key, value in opp_functions.items()}
ord_op = [['^', '_', '√'], ['*', '/'], ['+', '-'], '=']
symetric_op = ['*', '+']
ord_op_numbers = {'^': 3, '_': 3, '√': 3, '*': 2, '/': 2, '+': 1, '-': 1, '=': 0}
op_costs = {'^': 3.6, '_': 5, '√': 3, '*': 3.7, '/': 3.5, '+': 4, '-': 4, '=': 0}

inverse = {add: (sub, sub), sub: (add, revsub), mult: (div, div), div: (mult, revdiv), exp: (root, revlog), lg: (root, revexp)}

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

# change to dictionary
direct_rules = {("x = n", ("n")),
                ("a * x = n", ("n / a")),
                ("a * x + b = n", ("(n - b) / a")),
                ("a / x + b = n", ("(n - b) * a")),
                ("x ^ $odd-e$ = n", ("e √ n")),
                ("x ^ $even-e$ = n", ("e √ n", "0 - e √ n")),  # modify later to give all complex results
                ("a * x ^ 2 + b * x + c = n", ("(0 - b + 2 √ (b ^ 2 - 4 * a * (c - n))) / (2 * a)", "(0 - b - 2 √ (b ^ 2 - 4 * a * (c - n))) / (2 * a)"))}

# special case = [operation, special case, on the left, on the right, result or 'x']
special_cases = [['+', 0, True, True, 'x'], ['-', 0, False, True, 'x'], ['*', 0, True, True, 0], ['*', 1, True, True, 'x'], ['^', 0, False, True, 1], ['^', 0, True, False, 0], ['^', 1, True, False, 1], ['^', 1, False, True, 'x'], ['/', 0, True, False, 0], ['-', '=', None, None, 0], ['/', '=', None, None, 1], ['_', '=', None, None, 1], ['_', 1, False, True, 0]]

transpose = lambda ls: [[l[i] for l in ls] for i in range(len(ls))]
merge = lambda ls, f: list(map(f, transpose(ls)))


def binEncode(i, minBits):
    if(i >= 0):
        return('0' * (minBits - len(bin(i)[2:] + '0')) + bin(i)[2:] + '0')
    else:
        return('0' * (minBits - len(bin(1 - i)[2:] + '1')) + bin(1 - i)[2:] + '1')


def rec(x, f, n):
    if(n == 0):
        return(x)
    else:
        return(rec(f(x), f, n - 1))


class Base:

    def p(self, requiredV, text):  # verbosity: 0: None, 1: Steps, 2: Explanation for steps, 3: Debug/inner workings
        if(self.verbosity >= requiredV):
            print(text)
