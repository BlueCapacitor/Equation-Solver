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
lg = lambda a, b: log(a, b)
root = lambda a, b: b ** (1 / a)

opp_functions = {'^': exp, '_': lg, '√': root, '*': mult, '/': div, '+': add, '-': sub, '=': sub}
ord_op = [['^', '_', '√'], ['*', '/'], ['+', '-'], '=']
