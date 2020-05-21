'''
Created on Apr 19, 2020

@author: Gosha
'''

import functools
import os

from Graph import Graph
from Pattern import Pattern
from Simplification import simplify
from Solver import Solver, NumSolver
from Symbolic_Calculus import symDerivative
from Tree import Tree
import Tree as TreeM

LaTeXFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output.txt"
htmlFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output_equation.html"
htmlTemplateFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/html_output_equation_template.html"

latexMode = "html"

categories = {"Symbolic math": [], "Graphing": []}
actions = {}
arguments = []


def requestArguments(category, requestedArguments, outputType = None):

    def requestArgumentsDecorator(func):

        @functools.wraps(func)
        def wrapper(setOutputText):
            inputArguments = map(lambda arg: arg.get(), arguments)

            if(wrapper.outputType == None):
                setOutputText('')

                func(*inputArguments)
            elif(wrapper.outputType == str):
                setOutputText(str(func(*inputArguments)))

            elif(wrapper.outputType == int):
                setOutputText(int(func(*inputArguments)))

            elif(wrapper.outputType == float):
                setOutputText(func(*inputArguments))

            elif(wrapper.outputType in [Tree, Pattern]):
                setOutputText(displayEquation(func(*inputArguments)))

        wrapper.requestedArguments = requestedArguments
        wrapper.outputType = outputType
        actions[func.__name__[2:]] = wrapper
        categories[category].append(func.__name__[2:])
        return(wrapper)

    return(requestArgumentsDecorator)


def displayEquation(eq):
    if(TreeM.notation == "latex"):
        if(latexMode == "app"):
            f = open(LaTeXFile, 'w')
            f.write(str(eq))
            f.close()
            os.system("osascript ./display_latex.scpt")
        else:
            templatef = open(htmlTemplateFile, 'r')
            template = templatef.read()
            templatef.close()
            f = open(htmlFile, 'w')
            f.write(template.format(*[str(eq)]))
            f.close()
        return('')
    else:
        return(str(eq))

# ══════════════════════════════════════════════════


@requestArguments("Symbolic math", [("Equation: ", Tree)], Tree)
def UIParse(eq):
    return(eq)


@requestArguments("Symbolic math", [("Equation: ", Tree)], float)
def UIEval(eq):
    return(eq.evaluate())


@requestArguments("Symbolic math", [("Equation: ", Tree)], float)
def UINumSolve(eq):
    solver = NumSolver(eq)
    return(solver.solve())


@requestArguments("Symbolic math", [("Equation: ", Tree), ("Order: ", int, 1), ("Simplify: ", bool, True)], Tree)
def UISymDer(eq, order, sim):
    if(len(eq.objects) > 1):
        respectTo = input("With respect to: ")
    else:
        respectTo = None
    der = symDerivative(eq, respectTo = respectTo, n = order, sim = sim)
    return(der)


@requestArguments("Symbolic math", [("Equation: ", Tree), ("Max Steps: ", int, 200), ("Max Cost Ratio: ", float, 2)], Tree)
def UISimplify(eq, maxSteps, maxCostRatio):
    return(simplify(eq, maxSteps = maxSteps, maxCostRatio = maxCostRatio))


@requestArguments("Graphing", [("Graph ID: ", Graph)], None)
def UIRedraw(graph):
    graph.draw()


@requestArguments("Graphing", [("Graph ID: ", Graph)], None)
def UIReset(graph):
    graph.clear()


@requestArguments("Graphing", [("Graph ID: ", Graph)], None)
def UIBind_Movements(graph):
    graph.bindMovements()
    graph.drawCommands.append(graph.bindMovements)


@requestArguments("Graphing", [("Graph ID: ", Graph)], None)
def UIDraw_Axies(graph):  # later implement a color picker
    graph.drawAxies()
    graph.drawCommands.append(graph.drawAxies)


@requestArguments("Graphing", [("Equation: ", Tree), ("Graph ID: ", Graph)], None)
def UIPlot(eq, graph):  # later implement a color picker
    graph.plot(eq)
    graph.drawCommands.append(lambda: graph.plot(eq))
