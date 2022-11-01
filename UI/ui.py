'''
Created on May 21, 2020

@author: Gosha
'''

import clipboard

from Core import tree as TreeM
from Core.equationParser import parse
from Core.tree import Tree
from Graphing2D.graph import Graph
from Graphing3D.geometry import Point, Camera, Direction
from Graphing3D.graph3D import Graph3D
from Graphing3D.objects import DCamera
from TurtleCanvas.tKTurtleCanvas import TurtleCanvas
from UI import actions
import tkinter as tk

LaTeXFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output.txt"
htmlFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/output_equation.html"
htmlTemplateFile = "/Users/gosha/Google Drive/Programming/EclipseProjects/IMPP4/html_output_equation_template.html"

latexMode = "html"


class UI():

    def __init__(self):
        self.drawingWindows = {}

        self.window = tk.Tk()
        self.window.title("MultiMath")

        self.mainFrame = tk.Frame(self.window)
        self.mainFrame.grid(row = 0, column = 0)
        for i in range(3):
            self.mainFrame.rowconfigure(i, weight = 1)
        for i in range(2):
            self.mainFrame.columnconfigure(i, weight = 1)

        notationOptions = ["Prefix", "Infix", "Postfix", "LaTeX", "HTML"]

        self.action = tk.StringVar(self.window)
        self.action.trace('w', self.changeAction)
        self.actionSelect = tk.OptionMenu(self.mainFrame, self.action, value = None)
        self.actionSelect.grid(row = 0, column = 0)

        self.actionSelect['menu'].delete(0, 'end')
        for category in actions.categories:
            submenu = tk.Menu(self.mainFrame)

            for actionName in actions.categories[category]:
                submenu.add_command(label = actionName, command = tk._setit(self.action, actionName))

            self.actionSelect['menu'].add_cascade(label = category, menu = submenu)

        self.notationVar = tk.StringVar(self.window)
        self.notationVar.trace('w', self.changeNotation)
        notationSelect = tk.OptionMenu(self.mainFrame, self.notationVar, *notationOptions)
        self.notationVar.set("Infix")
        notationSelect.grid(row = 0, column = 2)

        runButton = tk.Button(self.mainFrame, text = "Run", command = self.runCurrentAction)
        runButton.grid(row = 0, column = 1)

        copyOutputText = lambda: clipboard.copy(outputText["text"])

        self.outerOutputFrame = tk.Frame(self.mainFrame)

        outputCanvas = tk.Canvas(self.outerOutputFrame)
        outputScrollbar = tk.Scrollbar(self.outerOutputFrame, orient = tk.HORIZONTAL, command = outputCanvas.xview)
        outputScrollbar.pack(side = tk.BOTTOM)
        outputCanvas.pack()
        outputCanvas.config(xscrollcommand = outputScrollbar.set)

        outputFrame = tk.Frame(outputCanvas)
        outputFrame.grid(row = 0, column = 0, sticky = tk.EW)
        outputText = tk.Button(outputFrame, command = copyOutputText)
        outputText.grid(row = 0, column = 0, sticky = tk.EW)

        self.setOutputText = lambda text: outputText.config(text = text)

        outputText.bind(copyOutputText)

        self.action.set("Parse")

#       ══════════════════════════════════════════════════

        menubar = tk.Menu()

        NewMenu = tk.Menu()
        NewMenu.add_command(label = "New Turtle Canvas", command = self.newTurtleCanvas)
        NewMenu.add_command(label = "New graph", command = self.newGraph)
        NewMenu.add_command(label = "New 3D graph", command = self.newGraph3D)
        menubar.add_cascade(label = "New", menu = NewMenu)

        self.window.config(menu = menubar)

#       ══════════════════════════════════════════════════

        self.window.mainloop()

    def changeAction(self, *_):
        self.destroyAllArguments()
        requestedArguments = actions.actions[self.action.get()].requestedArguments
        for requestedArgument in requestedArguments:
            actions.arguments.append(UIArgument(requestedArgument, self))
        if(actions.actions[self.action.get()].outputType == None):
            self.outerOutputFrame.grid_remove()
        else:
            self.outerOutputFrame.grid(row = 1 + len(actions.arguments), column = 0, columnspan = 3, sticky = tk.EW)

    def runCurrentAction(self):
        actionFunc = actions.actions[self.action.get()]
        actionFunc(self.setOutputText)

    def destroyAllArguments(self):
        for arg in actions.arguments:
            arg.delete()
        actions.arguments = []

    def changeNotation(self, *_):
        if(self.notationVar.get().lower() == "latex"):
            TreeM.notation = "latex"
            actions.latexMode = "app"
        elif(self.notationVar.get().lower() == "html"):
            TreeM.notation = "latex"
            actions.latexMode = "html"
        else:
            TreeM.notation = self.notationVar.get().lower()

    def newTurtleCanvas(self):
        windowID = max(list(self.drawingWindows.keys()) + [-1]) + 1

        self.drawingWindows[windowID] = TurtleCanvas(windowID)

    def newGraph(self):
        windowID = max(list(self.drawingWindows.keys()) + [-1]) + 1

        self.drawingWindows[windowID] = Graph(windowID)

    def newGraph3D(self):
        windowID = max(list(self.drawingWindows.keys()) + [-1]) + 1

        graph = Graph3D(windowID)
        graph.linkCamera(DCamera(Camera(Point([0, 0, 0]), Direction([0, 0, 0]))))
        graph.refresh()
        self.drawingWindows[windowID] = graph


class UIArgument():

    def __init__(self, args, UIObject):
        self.UIObject = UIObject

        if(len(args) == 2):
            self.text, self.argType = args
            self.default = None
        elif(len(args) == 3):
            self.text, self.argType, self.default = args

        row = len(actions.arguments) + 1
        self.label = tk.Label(UIObject.mainFrame, text = self.text)
        self.label.grid(row = row, column = 0, sticky = tk.EW)

        self.interface = None

        self.get = lambda: self.argType(self.interface.get())

        if(self.argType == bool):
            self.var = tk.BooleanVar(UIObject.window)
            self.interface = tk.Checkbutton(UIObject.mainFrame, variable = self.var)
            self.get = lambda: self.var.get()
            if(self.default is True):
                self.interface.select()
            if(self.default is False):
                self.interface.deselect()
            self.interface.grid(row = row, column = 1)

        if(self.argType == str):
            self.interface = tk.Entry(UIObject.mainFrame)
            if(self.default != None):
                self.interface.insert(tk.END, self.default)
            self.interface.grid(row = row, column = 1)

        if(self.argType == Tree):
            self.interface = tk.Entry(UIObject.mainFrame)
            if(self.default != None):
                self.interface.insert(tk.END, self.default)
            self.interface.grid(row = row, column = 1)

            self.get = lambda: parse(self.interface.get())

        if(self.argType == float):

            def validate(value):
                if(value in ['', '-']):
                    return(True)

                try:
                    float(value)
                    return(True)
                except Exception:
                    return(False)

            reg = UIObject.window.register(validate)
            self.interface = tk.Entry(UIObject.mainFrame, validate = "key", validatecommand = (reg, '%P'))
            if(self.default != None):
                self.interface.insert(tk.END, str(self.default))
            self.interface.grid(row = row, column = 1)

        if(self.argType == int):

            def validate(value):
                if(value in ['', '-']):
                    return(True)

                try:
                    return(float(value) == int(value))
                except Exception:
                    return(False)

            reg = UIObject.window.register(validate)
            self.interface = tk.Entry(UIObject.mainFrame, validate = "key", validatecommand = (reg, '%P'))
            if(self.default != None):
                self.interface.insert(tk.END, str(self.default))
            self.interface.grid(row = row, column = 1)

        if(self.argType in (TurtleCanvas, Graph, Graph3D)):

            def validate(value):
                if(value in ['']):
                    return(True)

                try:
                    return(float(value) == int(value) and int(value) >= 0)
                except Exception:
                    return(False)

            reg = UIObject.window.register(validate)
            self.interface = tk.Entry(UIObject.mainFrame, validate = "key", validatecommand = (reg, '%P'))
            if(self.default != None):
                self.interface.insert(tk.END, str(self.default))
            self.interface.grid(row = row, column = 1)

            self.get = lambda: self.UIObject.drawingWindows[int(self.interface.get())]

        if(self.argType == "color"):
            self.interface = tk.Frame(UIObject.mainFrame)
            self.interface.grid(row = row, column = 1)

            self.colorEntries = {}

            for i in range(3):
                c = ['R', 'G', 'B'][i]

                def validate(value):
                    if(value in ['']):
                        return(True)

                    try:
                        float(value)
                        return(float(value) >= 0 and float(value) <= 1)

                    except Exception:
                        return(False)

                reg = UIObject.window.register(validate)
                self.colorEntries[c] = tk.Entry(self.interface, validate = "key", validatecommand = (reg, '%P'))

                if(self.default != None):
                    self.colorEntries[c].insert(tk.END, str(self.default[i]))

                self.colorEntries[c].grid(row = 0, column = i)

            self.get = lambda: [float(self.colorEntries[c].get()) for c in ['R', 'G', 'B']]

        if(self.argType == Point):
            self.interface = tk.Frame(UIObject.mainFrame)
            self.interface.grid(row = row, column = 1)

            self.coordEntries = {}

            for i in range(3):
                c = ['X', 'Y', 'Z'][i]

                def validate(value):
                    if(value in ['', '-']):
                        return(True)

                    try:
                        float(value)
                        return(True)
                    except Exception:
                        return(False)

                reg = UIObject.window.register(validate)
                self.coordEntries[c] = tk.Entry(self.interface, validate = "key", validatecommand = (reg, '%P'))

                if(self.default != None):
                    self.coordEntries[c].insert(tk.END, str(self.default[i]))

                self.coordEntries[c].grid(row = 0, column = i)

            self.get = lambda: Point([float(self.coordEntries[c].get()) for c in ['X', 'Y', 'Z']])

    def delete(self):
        self.label.destroy()
        self.interface.destroy()
