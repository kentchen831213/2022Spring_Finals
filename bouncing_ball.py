from tkinter import *
from typing import List, Any

import ball
from ball import *
import random
from random import sample
from math import sqrt

POPULATION = 50
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


def get_random(base_speed: int, exclude_zero=True) -> int:
    """The helper function to randomly assign a speed value for one axis of the ball
    To ensure the ball is always moving, zero is taken away from the generated list
    :param: Base_speed: a non-zero integer given by the user
    :param: Include_zero: To include zero in the random pool or not. By default False
    :return: An int for moving value
    TODO: If a numpy.random.randint() might speed up the process
    TODO: A try, exception might needed if the base_speed was a negative number or invalid input(str, special char)
    TODO: A ball only moves horizontally or vertically still exists, need some help for solving this issue
    """
    random_speed_list = list(range(-base_speed, base_speed+1))
    if exclude_zero:
        # Remove zero
        random_speed_list.remove(0)
    return sample(random_speed_list, 1).pop()


def is_ball_collision(the_canvas, ball_coord: list):
    for i in range(len(ball_coord)):
        collide_ball_id = the_canvas.find_overlapping(*the_canvas.bbox(ball_coord[i].image))



def main():
    # Initialize a window
    window = Tk()
    window.geometry("800x600")
    window.resizable(False, False)

    # A canvas inside window
    canvas = Canvas(window, width=W_WIDTH, height=W_HEIGHT, bg="white")
    canvas.pack()

    # Place the preferable healthy balls and infected balls on the canvas
    # ball_position = {}
    ball_position = []
    for i in range(POPULATION+INFECTED_CASE):
        x_coord, y_coord = random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        if i < POPULATION:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY)
            ball_position.append(Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY))
        else:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED)
            ball_position.append(Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED))

    while True:
        # window.upadte()
        window.after(2)  # the tkinter built-in delay function, the frame is updated 1 frame/ms
        # for key, val in ball_position.items():
        #     ball_position[key].move()

        # ball collision
        for i in range(len(ball_position)):
            ball_position[i].move()
            ball_id = canvas.find_overlapping(*canvas.bbox(ball_position[i].image))
            # x_min, y_min, x_max, y_max = canvas.bbox(ball_position[i].image)
            # for j in range(i+1, len(ball_position)):
            #     ball_id = canvas.find_overlapping(x_min, y_min, x_max, y_max)
            # print(ball_id)
            if len(ball_id) >= 2 and ball_id[1] is not None:
                ball_position[i].x_speed = -ball_position[i].x_speed
                ball_position[i].y_speed = -ball_position[i].y_speed
                # ball_position[j].x_speed = -ball_position[j].x_speed
                # ball_position[j].y_speed = -ball_position[j].y_speed
            window.update()

    window.mainloop()


if __name__ == '__main__':
    main()
