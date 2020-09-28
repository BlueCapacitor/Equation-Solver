'''
Created on Apr 19, 2020

@author: Gosha
'''

import functools
import os

from Core import tree as TreeM
from Core.pattern import Pattern
from Core.tree import Tree
from Graphing2D.graph import Graph
from Graphing3D.geometry import Camera, Point, Direction, Triangle
from Graphing3D.graph3D import Graph3D
from Graphing3D.objects import DSurface, DCamera
from Graphing3D.predefinedObjects import sphereUV
from Math.aditionalMath import cplxRound
from Math.simplification import simplify
from Math.solver import Solver, NumSolver
from Math.symbolicCalculus import symDerivative

LaTeXFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output.txt"
htmlFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output_equation.html"
htmlTemplateFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/html_output_equation_template.html"

latexMode = "html"

categories = {"Symbolic math": [], "Graphing": [], "Graphing 3D": []}
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

            elif(wrapper.outputType == complex):
                out = func(*inputArguments)
                if(out == out.real):
                    setOutputText(out.real)
                elif(out == out.imag * 1j):
                    setOutputText("%s * i" % (out.imag))
                elif(out.imag > 0):
                    setOutputText("%s + %s * i" % (out.real, out.imag))
                elif(out.imag < 0):
                    setOutputText("%s - %s * i" % (out.real, 0 - out.imag))

            elif(wrapper.outputType in [Tree, Pattern]):
                setOutputText(displayEquation(func(*inputArguments)))

        wrapper.requestedArguments = requestedArguments
        wrapper.outputType = outputType

        name = ' '.join((func.__name__[2:]).split('_'))

        actions[name] = wrapper
        categories[category].append(name)
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


@requestArguments("Symbolic math", [("Equation:", Tree)], Tree)
def UIParse(eq):
    return(eq)


@requestArguments("Symbolic math", [("Equation:", Tree), ("Round To:", int, 4)], complex)
def UIEval(eq, roundTo):
    return(cplxRound(eq.evaluate(), roundTo))


@requestArguments("Symbolic math", [("Equation:", Tree)], float)
def UINumSolve(eq):
    solver = NumSolver(eq)
    return(solver.solve())


@requestArguments("Symbolic math", [("Equation:", Tree), ("Order:", int, 1), ("Simplify:", bool, True)], Tree)
def UISymDer(eq, order, sim):
    if(len(eq.surfaces) > 1):
        respectTo = input("With respect to:")
    else:
        respectTo = None
    der = symDerivative(eq, respectTo = respectTo, n = order, sim = sim)
    return(der)


@requestArguments("Symbolic math", [("Equation:", Tree), ("Max Steps:", int, 200), ("Max Cost Ratio:", float, 2)], Tree)
def UISimplify(eq, maxSteps, maxCostRatio):
    return(simplify(eq, maxSteps = maxSteps, maxCostRatio = maxCostRatio))


@requestArguments("Symbolic math", [("Equation:", Tree)], str)
def UIGetObjects(eq):
    return(str(eq.surfaces))

# ══════════════════════════════════════════════════


@requestArguments("Graphing", [("graph ID:", Graph, 0)], None)
def UIRedraw(graph):
    graph.draw()


@requestArguments("Graphing", [("graph ID:", Graph, 0)], None)
def UIReset(graph):
    graph.clear()


@requestArguments("Graphing", [("Color:", "color", (0, 0, 0)), ("graph ID:", Graph, 0)], None)
def UIDraw_Axies(color, graph):
    graph.drawAxies(color = color)
    graph.drawCommands.append(lambda: graph.drawAxies(color = color))


@requestArguments("Graphing", [("y(x):", Tree), ("Color:", "color", (0, 0, 1)), ("graph ID:", Graph, 0)], None)
def UIPlot(eq, color, graph):
    graph.plot(eq, color = color)
    graph.drawCommands.append(lambda: graph.plot(eq, color = color))


@requestArguments("Graphing", [("r(θ):", Tree), ("From:", float, -100), ("To:", float, 100), ("Color:", "color", (1, 0, 1)), ("graph ID:", Graph, 0)], None)
def UIPlot_Polar(eq, fromT, toT, color, graph):
    graph.plotPolar(eq, tRange = (fromT, toT), color = color)
    graph.drawCommands.append(lambda: graph.plotPolar(eq, tRange = (fromT, toT), color = color))


@requestArguments("Graphing", [("x(t):", Tree), ("y(t):", Tree), ("From:", float, -100), ("To:", float, 100), ("Color:", "color", (1, 0, 0)), ("graph ID:", Graph, 0)], None)
def UIPlot_Parametric(eqX, eqY, fromT, toT, color, graph):
    graph.plotParametric([eqX, eqY], tRange = (fromT, toT), color = color)
    graph.drawCommands.append(lambda: graph.plotParametric([eqX, eqY], tRange = (fromT, toT), color = color))


@requestArguments("Graphing", [("dy/dx:", Tree), ("Error » Undef:", bool, True), ("Color:", "color", (0, 1, 1)), ("graph ID:", Graph, 0)], None)
def UIPlot_Slope_Field(slopeFunc, errorAction, color, graph):
    graph.drawSlopeFeild(slopeFunc, color = color, treatExceptionsAsUndefined = errorAction)
    graph.drawCommands.append(lambda: graph.drawSlopeFeild(slopeFunc, color = color, treatExceptionsAsUndefined = errorAction))


@requestArguments("Graphing", [("dy/dx:", Tree), ("Initial x:", float, 0), ("Initial y:", float, 0), ("Color:", "color", (1, 0, 0)), ("graph ID:", Graph, 0)], None)
def UISolve_Slope_Field(slopeFunc, xi, yi, color, graph):
    graph.solveSlopeFeild(slopeFunc, xi, yi, color = color)
    graph.drawCommands.append(lambda: graph.solveSlopeFeild(slopeFunc, xi, yi, color = color))


@requestArguments("Graphing", [("X:", float, 0), ("Y:", float, 0), ("Color:", "color", (1, 0, 1)), ("graph ID:", Graph, 0)], None)
def UIPlot_Point(x, y, color, graph):
    graph.plotPoint((x, y), color = color)
    graph.drawCommands.append(lambda: graph.plotPoint((x, y), color = color))


@requestArguments("Graphing 3D", [("3D graph ID:", Graph3D, 0)], None)
def UIClear_Camera(graph):
    graph.dCam.clear()


@requestArguments("Graphing 3D", [("FPS:", float, 0), ("3D graph ID:", Graph3D, 0)], None)
def UIRefresh(fps, graph):
    graph.update()
    graph.setUpdateFrequency(fps)


@requestArguments("Graphing 3D", [("Center:", Point, [0, 0, 0]), ("r:", float), ("su:", int, 10), ("sv:", int, 10), ("3D graph ID:", Graph3D, 0)], None)
def UIPlace_Sphere(center, r, su, sv, graph):
    sphere = sphereUV(center, r, (su, sv))
    surface = DSurface(sphere, border = (0, 1, 0))
    graph.dCam.show(surface)
    graph.update()


@requestArguments("Graphing 3D", [("Vertex:", Point), ("Vertex:", Point), ("Vertex:", Point), ("3D graph ID:", Graph3D, 0)], None)
def UIPlace_Triangle(A, B, C, graph):
    triangle = Triangle(None, A, B, C)
    surface = DSurface([triangle])
    graph.dCam.show(surface)
    graph.update()
