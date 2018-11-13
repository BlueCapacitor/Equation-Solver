'''
Created on Oct 22, 2018

@author: gosha
'''

from Parser import *

if __name__ == '__main__':
    while(True):
        equation = raw_input("Equation ")
        print(showTree(parse(equation)))
