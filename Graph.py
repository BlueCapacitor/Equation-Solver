'''
Created on Feb 29, 2020

@author: Gosha
'''

import turtle

from Aditional_Math import *
from TK_Turtle_Canvas import TurtleCanvas
from Tree import Tree


# with open("./setup", 'r') as f:
#     exec(f.read())
class Graph(TurtleCanvas):

    def __init__(self, TCid):
        super().__init__(TCid)
        self.window.title("Graph | id: " + str(TCid))

        self.Xmin = -10
        self.Xmax = 10
        self.Ymin = -10
        self.Ymax = 10

        self.t.speed(0)
        self.t.hideturtle()

        self.drawCommands = []

    def draw(self):
        self.t.clear()

        for command in self.drawCommands:
            command()

    def translateX(self, x):
        windowX = self.t.getscreen().window_width()
        xRange = self.Xmax - self.Xmin
        xCenter = (self.Xmax + self.Xmin) / 2
        return((x - xCenter) / xRange * windowX)

    def translateY(self, y):
        windowY = self.t.getscreen().window_height()
        yRange = self.Ymax - self.Ymin
        yCenter = (self.Ymax + self.Ymin) / 2
        return((y - yCenter) / yRange * windowY)

    def translatePosition(self, x, y):
        return(self.translateX(x), self.translateY(y))

    def SxAxesPos(self):
        return(clamp(self.translateY(0), -self.t.getscreen().window_height() / 2 + 10, self.t.getscreen().window_height() / 2 - 10))

    def SyAxesPos(self):
        return(max(-self.t.getscreen().window_width() / 2 + 10, min(self.t.getscreen().window_width() / 2 - 10, self.translateX(0))))

    def drawAxies(self, color = (0, 0, 0), width = 2, alternateLableHeights = True):
        windowX = self.t.getscreen().window_width()
        windowY = self.t.getscreen().window_height()

        self.t.color(color)
        self.t.width(width)

        self.t.up()
        self.t.goto(-windowX / 2, self.SxAxesPos())
        self.t.pendown()
        self.t.goto(windowX / 2, self.SxAxesPos())

        self.t.up()
        self.t.goto(self.SyAxesPos(), -windowY / 2)
        self.t.pendown()
        self.t.goto(self.SyAxesPos(), windowY / 2)

        self.tickMarks(alternateLableHeights = alternateLableHeights)

    def increment(self, density = 20):
        return(10 ** round(log10((self.Xmax - self.Xmin) / density)), 10 ** round(log10((self.Ymax - self.Ymin) / density)))

    def tickMarks(self, density = 20, height = 5, rounding = 4, alternateLableHeights = True):
        windowX = self.t.getscreen().window_width()
        windowXRange = self.Xmax - self.Xmin

        increment = self.increment(density)
        xRange = sorted(list(fRange(0, self.Xmin, -increment[0])) + list(fRange(increment[0], self.Xmax, increment[0])))
        yRange = sorted(list(fRange(0, self.Ymin, -increment[1])) + list(fRange(increment[1], self.Ymax, increment[1])))

        opositeSideX = -self.t.getscreen().window_width() / 2 + 40 >= self.SxAxesPos()
#         print(self.SxAxesPos())

        lower = False

        for x in xRange:
            tx = self.translateX(x)
            self.t.up()
            self.t.goto(tx, self.SxAxesPos() - height)
            self.t.down()
            self.t.goto(tx, self.SxAxesPos() + height)
            self.t.up()
            if(lower and alternateLableHeights):
                self.t.goto(tx, self.SxAxesPos() - (height + 25) * (int(not(opositeSideX)) * 2 - 1))
            else:
                self.t.goto(tx, self.SxAxesPos() - (height + 15) * (int(not(opositeSideX)) * 2 - 1))
            self.t.write(str(round(x, rounding)), True, "center", ("Arial", 10))
            if(self.t.xcor() - tx >= (self.increment()[0]) / windowXRange * windowX / 3):
                lower = not(lower)

        for y in yRange:
            ty = self.translateY(y)
            self.t.up()
            self.t.goto(self.SyAxesPos() - height, ty)
            self.t.down()
            self.t.goto(self.SyAxesPos() + height, ty)
            self.t.up()
            self.t.goto(self.SyAxesPos() - height - 5, ty)
            self.t.write(str(round(y, rounding)), True, "right", ("Arial", 10))

    def plot(self, f, color = (0, 0, 1), width = 2, samples = 100, verbose = False, treatExceptionsAsUndefined = True):
        if(issubclass(type(f), Tree)):
            f = equationToFunction(f)

        dx = (self.Xmax - self.Xmin) / samples

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        x = self.Xmin
        while(x <= self.Xmax):
            x += dx
            try:
                y = f(x)
                if(verbose):
                    print("Plotting: %s, %s" % (x, y))
                if(clamp(x, self.Xmin, self.Xmax) == x and clamp(y, self.Ymin, self.Ymax) == y):
                    self.t.goto(self.translatePosition(x, y))
                    self.t.down()
                else:
                    self.t.up()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s: %s : %s")
                if(not(treatExceptionsAsUndefined)):
                    raise
                self.t.up()

    def slopeTick(self, x, y, s, length = 10):
        posX = self.translateX(x)
        posY = self.translateY(y)

        self.t.up()

        if(s != None):
            dx = length / sqrt(s ** 2 + 1)
            dy = s * dx

            self.t.goto(posX - dx / 2, posY - dy / 2)
            self.t.down()
            self.t.goto(posX + dx / 2, posY + dy / 2)

        else:
            sides = 10
            for a in range(sides + 1):
                self.t.goto(posX + cos(a * 2 * pi / sides) * length / 2, posY + sin(a * 2 * pi / sides) * length / 2)
                self.t.down()

    def drawSlopeFeild(self, f, density = 20, color = (1, 0, 0), width = 2, length = 10):
        increment = self.increment(density)
        xRange = list(fRange(0, self.Xmin, -increment[0])) + list(fRange(increment[0], self.Xmax, increment[0]))
        yRange = list(fRange(0, self.Ymin, -increment[1])) + list(fRange(increment[1], self.Ymax, increment[1]))

        self.t.color(color)
        self.t.width(width)

        for x in xRange:
            for y in yRange:
                try:
                    s = f(x, y)
                except(Exception):
                    s = None
                self.slopeTick(x, y, s, length = length)

    def solveSlopeFeild(self, f, xi, yi, color = (0, 1, 0), width = 2, d = 0.01, sThreashold = 350):
        x = xi
        y = yi

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        Xrange = self.Xmax - self.Xmin
        Yrange = self.Ymax - self.Ymin

        while(x <= self.Xmax + Xrange and y <= self.Ymax + Yrange and x >= self.Xmin - Xrange and y >= self.Ymin - Yrange):
            try:
                s = f(x, y)
            except Exception:
                break
            if(abs(s) > sThreashold):
                break
            y += s / sqrt(s ** 2 + 1) * d
            x += 1 / sqrt(s ** 2 + 1) * d
            self.t.goto(self.translatePosition(x, y))
            self.t.down()

        self.t.up()
        x = xi
        y = yi

        while(x <= self.Xmax + Xrange and y <= self.Ymax + Yrange and x >= self.Xmin - Xrange and y >= self.Ymin - Yrange):
            try:
                s = f(x, y)
            except Exception:
                break
            if(abs(s) > sThreashold):
                break
            y -= s / sqrt(s ** 2 + 1) * d
            x -= 1 / sqrt(s ** 2 + 1) * d
            self.t.goto(self.translatePosition(x, y))
            self.t.down()

    def clear(self):
        self.drawCommands = []
        self.t.clear()

    def bind(self, key, action):
        self.t.getscreen().onkey(action, key)

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

    def bindReset(self):
        self.t.getscreen().onkey(self.draw, 'r')

    def bindMovements(self, step = 1, zoomStep = 1):
        self.t.getscreen().onkey(lambda: self.move(-step, 0, 0, self.draw), "Left")
        self.t.getscreen().onkey(lambda: self.move(step, 0, 0, self.draw), "Right")
        self.t.getscreen().onkey(lambda: self.move(0, step, 0, self.draw), "Up")
        self.t.getscreen().onkey(lambda: self.move(0, -step, 0, self.draw), "Down")
        self.t.getscreen().onkey(lambda: self.move(0, 0, -zoomStep, self.draw), "=")
        self.t.getscreen().onkey(lambda: self.move(0, 0, zoomStep, self.draw), "-")
        self.t.getscreen().onkey(lambda: self.resetPosition(), "o")

    def plotPolar(self, f, color = (0, 0, 1), width = 2, dScale = 1, verbose = False):
        d = dScale * ((self.Xmax - self.Xmin) + (self.Ymax - self.Ymin)) / 10000

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        theta = 0
        for _ in range(10000):
            theta += d
            try:
                r = f(theta)
                if(verbose):
                    print("Plotting: %s, %s" % (theta, r))

                self.t.goto(self.translatePosition(cos(theta) * r, sin(theta) * r))
                self.t.down()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s" % (theta))
                self.t.up()

        self.t.up()
        theta = 0
        for _ in range(10000):
            theta -= d
            try:
                r = f(theta)
                if(verbose):
                    print("Plotting: %s, %s" % (theta, r))

                self.t.goto(self.translatePosition(cos(theta) * r, sin(theta) * r))
                self.t.down()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s" % (theta))
                self.t.up()

    def plotParametric(self, f, color = (0, 0, 1), width = 2, dScale = 1, verbose = False):
        d = dScale * ((self.Xmax - self.Xmin) + (self.Ymax - self.Ymin)) / 10000

        self.t.up()
        self.t.color(color)
        self.t.width(width)

        for t in fRange(-10000 * d, 10000 * d, d):
            try:
                x, y = f(t)
                if(verbose):
                    print("Plotting: %s, %s" % (x, y))

                self.t.goto(self.translatePosition(x, y))
                self.t.down()
            except Exception:
                if(verbose):
                    print("Plot undefined at %s" % (t))
                self.t.up()

    def plotPoint(self, point, color = (1, 0, 1), size = 10):
        self.t.up()
        self.t.color(color)
        self.t.goto(self.translatePosition(*point))
        self.t.dot(size)

    def plotPoints(self, f, xCoords, color = (1, 0, 1), size = 10):
        for x in xCoords:
            self.plotPoint((x, f(x)), color, size)
