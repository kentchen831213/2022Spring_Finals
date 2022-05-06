"""
Ball.py
---------
A custom class specific for bouncing_ball.py
"""
import random
from tkinter import Canvas

import numpy as np

POPULATION = 5
W_WIDTH = 800
W_HEIGHT = 600
BALL_OFFSET = 1
BALL_SIZE = 10
X_SPEED = 3
Y_SPEED = 3
FRAME_RATE = 1 / 240
INFECTED_CASE = 2
MASK_PROTECTION_RATE = 0.66
# color codes:
HEALTHY = '#aac6ca'
INFECTED = '#bb641d'
RECOVERED = '#cb8ac0'


def get_random_num(min_int, max_int, exclude_zero=True):
    random_num = list(range(min_int, max_int + 1))
    if exclude_zero:
        random_num.remove(0)
    return random.choice(random_num)


class Ball:
    def __init__(self, canvas, x, y, diameter, x_speed, y_speed, color, mask, vaccine, time, protect_rate):
        # self.ball = None
        # self.y_coord = None
        # self.x_coord = None
        # self.ball_position = None
        self.color = color
        self.canvas = canvas
        self.x = x
        self.y = y
        self.diameter = diameter
        self.image = canvas.create_oval(x, y, x + diameter, y + diameter, fill=color, width=0)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.mask = mask
        self.vaccine = vaccine
        self.time = time
        self.protect_rate = protect_rate

        # self.ball_position = []
        # for i in range(POPULATION + INFECTED_CASE):
        #     self.x_coord, self.y_coord = get_random_num(0, W_WIDTH, False), get_random_num(0, W_HEIGHT, False)
        #     if i <= POPULATION:
        #         self.ball_position.append = Canvas.create_oval(self.canvas,
        #                                                        self.x_coord,
        #                                                        self.y_coord,
        #                                                        self.x_coord + self.diameter,
        #                                                        self.y_coord + self.diameter,
        #                                                        fill=HEALTHY, width=0)
        #     else:
        #         self.ball_position.append = Canvas.create_oval(self.canvas,
        #                                                        self.x_coord,
        #                                                        self.y_coord,
        #                                                        self.x_coord + self.diameter,
        #                                                        self.y_coord + self.diameter,
        #                                                        fill=INFECTED, width=0)

    def move(self):
        # Boundary collision detection
        min_x, min_y, max_x, max_y = self.canvas.bbox(self.image)
        if (max_x >= self.canvas.winfo_width()-1 and self.x_speed > 0) or (min_x < 0 and self.x_speed < 0):
            self.x_speed = -self.x_speed
        if (max_y >= self.canvas.winfo_height()-1 and self.y_speed > 0) or (min_y < 0 and self.y_speed < 0):
            self.y_speed = -self.y_speed
        self.canvas.move(self.image, self.x_speed, self.y_speed)

    def ball_collide(self):
        pass



