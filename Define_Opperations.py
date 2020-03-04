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

fixSymbols = {"#pi": pi, '#π': pi,
              '#e': e,
              '#i': 1j,
              '÷': '/', ':': '/',
              "log": '_', 'lg': '_',
              "rt": '√', "root": '√',
              "pow": '^', "exp": '^'}

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
ord_op_numbers = {'^': 3, '_': 3, '√': 3, '*': 2, '/': 2, '+': 1, '-': 1, '=': 0}

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
# special_cases = [['+', 0, True, True, 'x']]
special_cases = []


class Base:

    def p(self, requiredV, text):  # verbosity: 0: None, 1: Steps, 2: Explanation for steps, 3: Debug/inner workings
        if(self.verbosity >= requiredV):
            print(text)
