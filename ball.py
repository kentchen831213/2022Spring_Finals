"""
Ball.py
---------
A custom class specific for bouncing_ball_hp2.py
"""
import random
from tkinter import Canvas
import numpy as np


def get_random_num(min_int, max_int, exclude_zero=True):
    random_num = list(range(min_int, max_int + 1))
    if exclude_zero:
        random_num.remove(0)
    return random.choice(random_num)


class Ball:

    infected = []
    recovered = []
    ball_position = []

    def __init__(self, canvas, x, y, diameter, x_speed, y_speed, color, mask=False, vaccine=False):
        # self.ball = None
        # self.y_coord = None
        # self.x_coord = None
        # self.ball_position = None
        self.color = color
        self.canvas = canvas
        self.x = x
        self.y = y
        if x>500:
            self.section = 'right'
        else:
            self.section = 'left'
        self.diameter = diameter
        self.image = canvas.create_oval(x, y, x + diameter, y + diameter, fill=color, width=2, outline='#F5F5F5')
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.mask = mask
        self.vaccine = vaccine

    def move(self):
        # Boundary collision detection
        min_x, min_y, max_x, max_y = self.canvas.bbox(self.image)
        if (max_x >= self.canvas.winfo_width()-1 and self.x_speed > 0) or (min_x < 0 and self.x_speed < 0):
            self.x_speed = -self.x_speed
        if (max_y >= self.canvas.winfo_height()-1 and self.y_speed > 0) or (min_y < 0 and self.y_speed < 0):
            self.y_speed = -self.y_speed
        self.canvas.move(self.image, self.x_speed, self.y_speed)

