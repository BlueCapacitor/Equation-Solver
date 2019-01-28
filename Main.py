'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import parse
from Newtons_Method import Newtons_Method

if __name__ == '__main__':
    while(True):
        equation = input("Equation: ")
        name = input("Var Name: ")
        print(Newtons_Method(parse(equation), name))
