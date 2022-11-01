'''
Created on Aug 17, 2020

@author: Gosha
'''

from math import pi, sqrt, ceil
import turtle

from numpy import isfinite, isnan

from Graphing3D.geometry import Point
from TurtleCanvas.tKTurtleCanvas import TurtleCanvas


class Screen3D(TurtleCanvas):

    def __init__(self, windowID, scale = 250, camera = None, bindTurn = "mouse", canvas = None):
        super().__init__(windowID)
        self.window.title("3D Screen | id: %s" % (self.windowID))

        self.t.hideturtle()

        self.dCam = camera
        self.scale = scale

        self.updateDelay = 0
        self.updaterActive = False

        self.t.getscreen().tracer(0, 0)

        self.window.bind("<Configure>", self.recenter)

        if(bindTurn == "mouse"):
            self.window.bind('<Motion>', self.mouseMove)

            self.canvas._root().bind("<Up>", lambda _: self.move([0, 0, 1]))
            self.canvas._root().bind("<Down>", lambda _: self.move([0, 0, -1]))
            self.canvas._root().bind("<Right>", lambda _: self.move([-1, 0, 0]))
            self.canvas._root().bind("<Left>", lambda _: self.move([1, 0, 0]))

        else:
            self.canvas._root().bind("<Up>", lambda _: self.tilt(0 - pi / 32))
            self.canvas._root().bind("<Down>", lambda _: self.tilt(pi / 32))
            self.canvas._root().bind("<Right>", lambda _: self.turn(pi / 32))
            self.canvas._root().bind("<Left>", lambda _: self.turn(0 - pi / 32))

    def unlinkCamera(self):
        self.dCam = None

    def linkCamera(self, camera):
        self.dCam = camera

    def draw(self, dTriangle):
        dTriangle.draw(self, self.dCam.camera, self.scale)

    def update(self):
        self.t.clear()
        if(self.dCam != None):
            dTriangles = []
            for dSurface in self.dCam.surfaces:
                dTriangles += dSurface.extractDTriangles()

            dTriangles.sort(key = lambda dTriangle: sum([self.dCam.camera.depth(point) for point in dTriangle.triangle.points]))

            for dTriangle in dTriangles:
                self.draw(dTriangle)

        self.refresh()

        if(self.updateDelay > 0 and not(self.updaterActive)):
            self.window.after(ceil(self.updateDelay), self.update)

    def refresh(self):
        self.screen.update()

    def setUpdateFrequency(self, frequency):
        self.updateDelay = 1000 / frequency if frequency > 0 else 0
        self.update()

    def tilt(self, amount = pi / 16):
        if(self.dCam != None):
            self.dCam.camera.orientation.u += amount

    def turn(self, amount = pi / 16):
        if(self.dCam != None):
            self.dCam.camera.orientation.v += amount

    def move(self, amount = [0, 0, 0]):
        if(self.dCam != None):
            self.dCam.camera.location += Point(amount)

    def mouseMove(self, event):
        x, y = event.x, event.y
        if(self.dCam != None):
            self.dCam.camera.orientation.v = (x - self.width() / 2) * 0.01
            self.dCam.camera.orientation.u = 0 - (y - self.height() / 2) * 0.01
            self.dCam.camera.orientation.w = 0

    def checkBounds(self, point2D, margin = (0, 0)):
        if(not(isfinite(point2D[0]) and isfinite(point2D[1]))):
            return(False)

        if(point2D[0] < margin[0] - self.width() * 0.5):
            return(False)
        if(point2D[0] > self.width() * 0.5 - margin[0]):
            return(False)

        if(point2D[1] < margin[1] - self.height() * 0.5):
            return(False)
        if(point2D[1] > self.height() * 0.5 - margin[1]):
            return(False)

        return(True)

    def maxDistToCent(self):
        return(sqrt(self.screen.screensize()[0] ** 2 + self.screen.screensize()[1] ** 2))

    def width(self):
        return(self.canvas.winfo_width())

    def height(self):
        return(self.canvas.winfo_height())

    def updateLoop(self):
        while(True):
            self.update()

    def project(self, point):
        assert self.dCam != None, "No linked camera"
        return(self.dCam.camera.project(point))

    def toScreenCoords(self, point):
        position = self.project(point)
        return([position[0] * self.scale, position[1] * self.scale])

    def target(self, point, other):
        cam = self.dCam.camera
        if(cam.depth(point) < 0.001):
            if(cam.depth(other) < 0.001):
                return

            dilationFactor = cam.depth(other) / (cam.depth(other) - cam.depth(point)) - 0.001

            point = point * dilationFactor + other * (1 - dilationFactor)

        elif(cam.depth(other) < 0.001):
            dilationFactor = cam.depth(point) / (cam.depth(point) - cam.depth(other)) - 0.001

            other = other * dilationFactor + point * (1 - dilationFactor)

        position = self.toScreenCoords(point)

        if(isnan(position[0]) or isnan(position[1])):
            return

#         self.t.goto(*position)

        if(self.checkBounds(position)):
            return((position, None))

        else:
            otherPosition = self.toScreenCoords(other)

            if(isnan(otherPosition[0]) or isnan(otherPosition[1])):
                return

            a, b = position

            c, d = otherPosition

            T, B, R, L = self.height() * 0.5, 0 - self.height() * 0.5, self.width() * 0.5, 0 - self.width() * 0.5

            dilationFactor = 1
            side = None

            if(a < L and a != c):
                if(c < L):
                    return

                if(dilationFactor > (L - c) / (a - c)):
                    dilationFactor = (L - c) / (a - c)
                    side = Side(self, 'L')

            if(a > R and a != c):
                if(c > R):
                    return

                if(dilationFactor > (R - c) / (a - c)):
                    dilationFactor = (R - c) / (a - c)
                    side = Side(self, 'R')

            if(b < B and b != d):
                if(d < B):
                    return

                if(dilationFactor > (B - d) / (b - d)):
                    dilationFactor = (B - d) / (b - d)
                    side = Side(self, 'B')

            if(b > T and b != d):
                if(d > T):
                    return

                if(dilationFactor > (T - d) / (b - d)):
                    dilationFactor = (T - d) / (b - d)
                    side = Side(self, 'T')

            newPosition = dilationFactor * a + (1 - dilationFactor) * c, dilationFactor * b + (1 - dilationFactor) * d
            return((newPosition, side))


class Side(object):

    def __init__(self, screen, side):
        self.screen = screen
        self.side = side

        self.opposites = {'T': 'B', 'B': 'T', 'L': 'R', 'R': 'L'}

    def opposite(self):
        return(Side(self.screen, self.opposites[self.side]))

    def __eq__(self, other):
        return(type(other) == Side and self.screen == other.screen and self.side == other.side)

    def __neq__(self, other):
        return(not(self == other))

    def isOpposite(self, other):
        return(self.screen == other.screen and self.side == self.opposites[other.side])

    def isAdjacent(self, other):
        return(self.screen == other.screen and self.side != other.side and self.side != self.opposites[other.side])

    def coord(self):
        if(self.side == 'T'):
            return({'y': self.screen.height() * 0.5})
        if(self.side == 'B'):
            return({'y': 0 - self.screen.height() * 0.5})
        if(self.side == 'R'):
            return({'x': self.screen.width() * 0.5})
        if(self.side == 'L'):
            return({'x': 0 - self.screen.width() * 0.5})

    def intersection(self, other):
        if(not(self.isAdjacent(other))):
            return(None)
        out = self.coord()
        out.update(other.coord())
        return((out['x'], out['y']))
