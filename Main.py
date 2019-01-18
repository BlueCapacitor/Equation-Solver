'''
Created on Oct 22, 2018

@author: Gosha
'''

from Parser import *

if __name__ == '__main__':
    while(True):
        equation = input("Equation ")
        print(parse(equation).show())
