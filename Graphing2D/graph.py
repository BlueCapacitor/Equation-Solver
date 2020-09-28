'''
Created on Feb 29, 2020

@author: Gosha
'''

from Core.tree import Tree
from Math.aditionalMath import *
from TurtleCanvas.tKTurtleCanvas import TurtleCanvas


class Graph(TurtleCanvas):

    def __init__(self, windowID):
        buttons = {"Redraw": self.draw, "Clear": self.clear, "Undo": self.undo}

        super().__init__(windowID, buttons = buttons)
        self.window.title("Graph | id: %s" % (self.windowID))

        self.Xmin = -10
        self.Xmax = 10
        self.Ymin = -10
        self.Ymax = 10

        self.t.speed(0)
        self.t.hideturtle()

        self.screen.tracer(0, 0)

        self.lastDrawID = -1

        self.window.bind("<Configure>", self.recenter)

        self.drawCommands = []
        self.clearedItems = []

        self.bindMovements()

    def draw(self):
        self.lastDrawID += 1
        drawID = self.lastDrawID

        self.t.clear()

        for i in range(len(self.drawCommands)):

            command = self.drawCommands[i]

            self.window.title("Graph | id: %s | %s%%" % (self.windowID, round(100 * i / len(self.drawCommands))))

            command()
            self.update()

            if(self.lastDrawID > drawID):
                return

        self.window.title("Graph | id: %s" % (self.windowID))

    def undo(self):
        if(len(self.drawCommands) > 0):
            self.drawCommands = self.drawCommands[:-1]
        else:
            self.drawCommands = self.clearedItems
            self.clearedItems = []

        self.draw()

    def translateX(self, x):
        xRange = self.Xmax - self.Xmin
        return((x - self.Xmin) / xRange * self.screenWidth)

    def translateY(self, y):
        yRange = self.Ymax - self.Ymin
        return((self.Ymax - y) / yRange * self.screenHeight)

    def translatePosition(self, x, y):
        return(self.translateX(x), self.translateY(y))

    def SxAxesPos(self):
        return(clamp(self.translateY(0), 10, self.screenHeight - 10))

    def SyAxesPos(self):
        return(clamp(self.translateX(0), 10, self.screenWidth - 10))

    def drawAxies(self, color = (0, 0, 0), width = 2, alternateLableHeights = True):
        windowX = self.screenWidth
        windowY = self.screenHeight

        self.t.color(color)
        self.t.width(width)

        self.t.up()
        self.t.goto(0, self.SxAxesPos())
        self.t.pendown()
        self.t.goto(windowX, self.SxAxesPos())

        self.t.up()
        self.t.goto(self.SyAxesPos(), 0)
        self.t.pendown()
        self.t.goto(self.SyAxesPos(), windowY)

        self.tickMarks(alternateLableHeights = alternateLableHeights)

        self.update()

    def increment(self, density = 20):
        return(findNiceNumber((self.Xmax - self.Xmin) / density), findNiceNumber((self.Ymax - self.Ymin) / density))

    def tickMarks(self, density = 20, height = 5, alternateLableHeights = True):
        windowX = self.screenWidth
        windowXRange = self.Xmax - self.Xmin

        increment = self.increment(density)
        xRange = list(fRange(0, self.Xmin, -increment[0])) + list(fRange(increment[0], self.Xmax, increment[0]))
        yRange = list(fRange(0, self.Ymin, -increment[1])) + list(fRange(increment[1], self.Ymax, increment[1]))

        opositeSideX = 40 >= self.SxAxesPos()

        alternate = max(map(lambda x: len(str(x)), xRange)) >= increment[0] * windowX / windowXRange * 0.4

        lower = True

        for x in xRange:
            tx = self.translateX(x)
            self.t.up()
            self.t.goto(tx, self.SxAxesPos() - height)
            self.t.down()
            self.t.goto(tx, self.SxAxesPos() + height)
            self.t.up()
            if(lower and alternateLableHeights):
                self.t.goto(tx, self.SxAxesPos() - (height + 5) * (int(not(opositeSideX)) * 2 - 1))
            else:
                self.t.goto(tx, self.SxAxesPos() - (height + 15) * (int(not(opositeSideX)) * 2 - 1))
            roundTo = 5 - floor(log10(abs(increment[0])))
            self.t.write(str(round(x, roundTo)), True, "center", ("Arial", 10))
            if(alternate):
                lower = not(lower)

        for y in yRange:
            ty = self.translateY(y)
            self.t.up()
            self.t.goto(self.SyAxesPos() - height, ty)
            self.t.down()
            self.t.goto(self.SyAxesPos() + height, ty)
            self.t.up()
            self.t.goto(self.SyAxesPos() - height - 5, ty)
            roundTo = 5 - floor(log10(abs(increment[1])))
            self.t.write(str(round(y, roundTo)), True, "right", ("Arial", 10))

    def plot(self, f, color = (0, 0, 1), width = 2, samples = 300, verbose = False, treatExceptionsAsUndefined = True):
        if(issubclass(type(f), Tree)):
            f = equationToFunction(f)

        dx = (self.Xmax - self.Xmin) / samples / self.xScale

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        for x in fRange(self.Xmin, self.Xmax, dx):
            try:
                y = f(x)
                yR = y.real

                if(verbose):
                    print("Plotting: %s, %s" % (x, yR))
                if(clamp(x, self.Xmin, self.Xmax) == x and clamp(yR, self.Ymin, self.Ymax) == yR):
                    self.t.goto(self.translatePosition(clamp(x, self.Xmin, self.Xmax), clamp(yR, self.Ymin, self.Ymax)))

                    if(yR != y):
                        self.t.color(list(map(lambda c: (2 / 3) + c / 3, color)))
                    else:
                        self.t.color(color)
                    self.t.down()
                else:
                    self.t.up()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s" % (x))
                if(not(treatExceptionsAsUndefined)):
                    raise
                self.t.up()

        self.update()

    def slopeTick(self, x, y, s, density = 20):
        self.t.up()
        length = ((self.increment(density)[0] * (self.increment(density)[1])) ** 0.5) / 2

        if(s != None):
            dx = length / ((s ** 2 + 1) ** 0.5)
            dy = s * dx

            self.t.goto(self.translateX(x - dx / 2), self.translateY(y - dy / 2))
            self.t.down()
            self.t.goto(self.translateX(x + dx / 2), self.translateY(y + dy / 2))

        else:
            sides = 10
            for a in range(sides + 1):
                self.t.goto(self.translateX(x + cos(a * 2 * pi / sides) * length / 2), self.translateY(y + sin(a * 2 * pi / sides) * length / 2))
                self.t.down()

    def drawSlopeFeild(self, f, density = 20, color = (0, 1, 1), width = 2, treatExceptionsAsUndefined = True):
        if(issubclass(type(f), Tree)):
            f = equationToFunction(f)

        increment = self.increment(density)
        xRange = list(fRange(0, self.Xmin, -increment[0])) + list(fRange(increment[0], self.Xmax, increment[0]))
        yRange = list(fRange(0, self.Ymin, -increment[1])) + list(fRange(increment[1], self.Ymax, increment[1]))

        self.t.color(color)
        self.t.width(width)

        for x in xRange:
            for y in yRange:
                try:
                    s = f(x = x, y = y)
                except(Exception):
                    if(not(treatExceptionsAsUndefined)):
                        raise
                    s = None
                self.slopeTick(x, y, s, density = density)

        self.update()

    def solveSlopeFeild(self, f, xi, yi, color = (1, 0, 0), width = 2, d = 0.01, sThreashold = 350, verbose = False):
        if(issubclass(type(f), Tree)):
            f = equationToFunction(f)

        x = xi
        y = yi

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        Xrange = self.Xmax - self.Xmin
        Yrange = self.Ymax - self.Ymin

        while(x <= self.Xmax + Xrange and y <= self.Ymax + Yrange and x >= self.Xmin - Xrange and y >= self.Ymin - Yrange):
            try:
                s = f(x = x, y = y)
            except Exception:
                break
            if(abs(s) > sThreashold):
                break
            y += s / ((s ** 2 + 1) ** 0.5) * d
            x += 1 / ((s ** 2 + 1) ** 0.5) * d

            if(verbose):
                print("Plotting (%s, %s)" % (x, y))

            self.t.goto(self.translatePosition(x, y))
            self.t.down()

        self.t.up()
        x = xi
        y = yi

        while(x <= self.Xmax + Xrange and y <= self.Ymax + Yrange and x >= self.Xmin - Xrange and y >= self.Ymin - Yrange):
            try:
                s = f(x = x, y = y)

                if(abs(s) > sThreashold):
                    break
                y -= s / ((s ** 2 + 1) ** 0.5) * d
                x -= 1 / ((s ** 2 + 1) ** 0.5) * d
            except Exception:
                break

            if(verbose):
                print("Plotting (%s, %s)" % (x, y))

            self.t.goto(self.translatePosition(x, y))
            self.t.down()

        self.update()

    def clear(self):
        self.clearedItems = list(self.drawCommands)
        self.drawCommands = []
        self.t.clear()
        self.update()

    def bind(self, action, key):
        self.window.bind(key, action)

    def move(self, x, y, zoom):
        xRange = self.Xmax - self.Xmin
        yRange = self.Ymax - self.Ymin

        self.Xmin += x * xRange / 8
        self.Xmax += x * xRange / 8
        self.Ymin += y * yRange / 8
        self.Ymax += y * yRange / 8

        xCenter = (self.Xmin + self.Xmax) / 2
        yCenter = (self.Ymin + self.Ymax) / 2

        self.Xmin = xCenter + (self.Xmin - xCenter) * ((10 ** (1 / 3)) ** zoom)
        self.Xmax = xCenter + (self.Xmax - xCenter) * ((10 ** (1 / 3)) ** zoom)
        self.Ymin = yCenter + (self.Ymin - yCenter) * ((10 ** (1 / 3)) ** zoom)
        self.Ymax = yCenter + (self.Ymax - yCenter) * ((10 ** (1 / 3)) ** zoom)
        self.draw()

    def resetPosition(self):
        self.Xmin = -10
        self.Xmax = 10
        self.Ymin = -10
        self.Ymax = 10
        self.draw()

    def bindRedraw(self):
        self.bind(lambda _: self.draw(), 'r')

    def bindMovements(self, step = 1, zoomStep = 1):
        self.bind(lambda _: self.move(-step, 0, 0), "<Left>")
        self.bind(lambda _: self.move(step, 0, 0), "<Right>")
        self.bind(lambda _: self.move(0, step, 0), "<Up>")
        self.bind(lambda _: self.move(0, -step, 0), "<Down>")
        self.bind(lambda _: self.move(0, 0, -zoomStep), "=")
        self.bind(lambda _: self.move(0, 0, zoomStep), "-")
        self.bind(lambda _: self.resetPosition(), "o")

    def plotPolar(self, f, tRange = (-32 * pi, 32 * pi), color = (1, 0, 1), width = 2, dScale = 1, verbose = False, treatExceptionsAsUndefined = True):
        if(issubclass(type(f), Tree)):
            f = equationToFunction(f)
        p = lambda t: (cos(t) * f(t), sin(t) * f(t))
        self.plotParametric(p, tRange = tRange, color = color, width = width, dScale = dScale, verbose = verbose, treatExceptionsAsUndefined = treatExceptionsAsUndefined)

    def plotParametric(self, f, tRange = (-100, 100), color = (1, 0, 0), width = 2, dScale = 1, verbose = False, treatExceptionsAsUndefined = True):
        d = dScale * ((self.Xmax - self.Xmin) * (self.Ymax - self.Ymin)) ** 0.02 / 20
        if(type(f) in (tuple, list)):
            if(issubclass(type(f[0]), Tree)):
                f[0] = equationToFunction(f[0])
            if(issubclass(type(f[1]), Tree)):
                f[1] = equationToFunction(f[1])

            g = f
            f = lambda t: (g[0](t), g[1](t))

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        for t in fRange(tRange[0], tRange[1], d):
            try:
                x, y = f(t)
                xR, yR = x.real, y.real

                if(xR != x or yR != y):
                    self.t.color(list(map(lambda c: (2 / 3) + c / 3, color)))
                else:
                    self.t.color(color)

                if(verbose):
                    print("Plotting: %s, %s" % (cplxRound(x, 3), y))

                if(clamp(xR, self.Xmin, self.Xmax) == xR and clamp(yR, self.Ymin, self.Ymax) == yR):
                    self.t.goto(self.translatePosition(xR, yR))
                    self.t.down()
                else:
                    self.t.up()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s" % (t))
                self.t.up()
                if(not(treatExceptionsAsUndefined)):
                    raise

        self.update()

    def plotPoint(self, point, color = (1, 0, 1), size = 10):
        self.t.up()
        self.t.color(color)
        self.t.goto(self.translatePosition(*point))
        self.t.dot(size)

        self.update()

    def plotPoints(self, f, xCoords, color = (1, 0, 1), size = 10):
        for x in xCoords:
            self.plotPoint((x, f(x)), color, size)

        self.update()

    def update(self):
        self.screen.update()
