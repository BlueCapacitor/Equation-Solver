'''
Created on Oct 22, 2018

@author: gosha
'''

import Parser

if __name__ == '__main__':
    while(True):
        equation = input("Equation")
        Parser.parse(equation)