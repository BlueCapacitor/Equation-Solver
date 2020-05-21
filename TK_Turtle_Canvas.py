'''
Created on May 20, 2020

@author: Gosha
'''

import turtle

import tkinter as tk


class TurtleCanvas(object):

    def __init__(self, TCid):
        self.TCid = TCid

        self.window = tk.Tk()
        self.window.title("Turtle Canvas | id: " + str(TCid))
        self.frame = tk.Frame(self.window, bg = "Black")
        self.frame.pack(expand = True, fill = tk.BOTH)

        self.idLabel = tk.Label(self.frame, text = "id: " + str(TCid))
        self.idLabel.grid(row = 0, column = 0, sticky = tk.NSEW, padx = 4, pady = (4, 2))

        self.canvas = tk.Canvas(self.frame)
        self.canvas.grid(row = 1, column = 0, sticky = tk.NSEW, padx = 4, pady = (2, 4))

        self.frame.rowconfigure(0, weight = 0)
        self.frame.rowconfigure(1, weight = 1)

        self.frame.columnconfigure(0, weight = 1)

        self.t = turtle.RawTurtle(self.canvas)
