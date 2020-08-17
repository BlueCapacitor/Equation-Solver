'''
Created on May 20, 2020

@author: Gosha
'''

import turtle

from Aditional_Math import *
import tkinter as tk


class TurtleCanvas(object):

    def __init__(self, TCid, buttons = []):
        self.TCid = TCid

        self.window = tk.Tk()
        self.window.title("Turtle Canvas | id: " + str(TCid))

        self.frame = tk.Frame(self.window, bg = "Black")
        self.frame.pack(expand = True, fill = tk.BOTH)

        self.idLabel = tk.Label(self.frame, text = "id: " + str(TCid))
        self.idLabel.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 4, pady = (4, 2))

        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row = 1, column = 0, columnspan = 1 + len(buttons), sticky = tk.NSEW, padx = 4, pady = (2, 4))

        self.buttons = {}
        for i in range(len(buttons)):
            name, function = list(buttons.items())[i]

            button = tk.Button(self.frame, text = name, command = function)
            button.grid(row = 0, column = i + 1, sticky = tk.NSEW, padx = (0, 4), pady = (4, 2))
            self.buttons[name] = button

        self.frame.rowconfigure(0, weight = 0)
        self.frame.rowconfigure(1, weight = 1)

        self.frame.columnconfigure(0, weight = 1)
        for column in range(1, len(buttons) + 1):
            self.frame.columnconfigure(column, weight = 0)

        self.t = turtle.RawTurtle(self.canvas)
        self.screen = self.t.getscreen()

        self.recenter()

    def recenter(self, *_):
        self.screen.setworldcoordinates(0, 128, 128, 0)
        self.screenWidth = self.canvas.winfo_width() * 9 / 20
        self.screenHeight = self.canvas.winfo_height() * 13 / 20
        self.xScale = self.screenWidth / 130.05
        self.yScale = self.screenHeight / 132.6
        self.GMScale = sqrt(self.xScale * self.yScale)
        self.window.update()
