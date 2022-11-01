'''
Created on Aug 17, 2020

@author: Gosha
'''

from math import pi, sqrt
import turtle

from numpy import isfinite, isnan

from Graphing3D.screen3D import Screen3D
from TurtleCanvas.tKTurtleCanvas import TurtleCanvas


class Graph3D(Screen3D):

    def __init__(self, windowID, scale = 250, camera = None, bindTurn = "mouse", canvas = None):
        super().__init__(windowID)
        self.window.title("3D Graph | id: %s" % (self.windowID))
