'''
Created on Jan 25, 2019

@author: gosha
'''

symbols = {"blank": [" "],
           "digit": ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'],
           "operation": ['^', '*', '/', '÷', '+', '-', '='],
           "decimal": ['.'],
           "parentheses": ['(', ')']}

add = lambda a, b: a + b
sub = lambda a, b: a - b
mult = lambda a, b: a * b
div = lambda a, b: a / b
exp = lambda a, b: a ** b

opp_functions = {"^": exp, "*": mult, "/": div, "÷": div, "+": add, "-": sub}
