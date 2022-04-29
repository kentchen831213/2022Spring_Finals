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
BALL_SIZE = 5
X_SPEED = 2
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
    random_speed_list = list(range(-base_speed, base_speed + 1))
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
    infected = []
    ball_position = []
    for i in range(POPULATION + INFECTED_CASE):
        x_coord, y_coord = random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        if i < POPULATION:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY)
            ball_position.append(Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY))
        else:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED)
            ball_position.append(Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED))
            infected.append(i+1)  # The
        print(ball_position[i], ball_position[i].x, ball_position[i].y)
        overlap_balls = canvas.find_overlapping(*canvas.bbox(ball_position[i].image))

        # Replace the ball that is overlapping with another
        if len(overlap_balls) >= 2:  # The length of tuple suggested an overlap issue between two or more balls
            # Move the last rendered ball to a new random location
            canvas.moveto(overlap_balls[1],
                          x=random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1),
                          y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))

        print(overlap_balls, len(overlap_balls))
    print("end")

    while True:
        window.after(1)  # the tkinter built-in delay function, the frame is updated 1 frame/ms
        # for key, val in ball_position.items():
        #     ball_position[key].move()

        # Have all balls moving
        for i in range(len(ball_position)):
            ball_position[i].move()

            # Ball collision detection
            collide = list(canvas.find_overlapping(*canvas.bbox(ball_position[i].image)))
            if len(collide) >= 2:
                # When collided, expected ball to bounce off
                ball_position[i].x_speed *= -1
                ball_position[i].y_speed *= -1
                print(collide, ball_position[collide[0] - 1].x_speed, ball_position[collide[0] - 1].y_speed,
                      ball_position[collide[1] - 1].x_speed, ball_position[collide[1] - 1].y_speed)
                # for j in range(len(collide)):
                #     ball_position[collide[j] - 1].x_speed *= -1
                #     ball_position[collide[j] - 1].y_speed *= -1

                # Check if the infected ball(s) is involved in a collision
                check = any(ball_id in collide for ball_id in infected)
                if check:
                    # Once confirmed, removed the infected ones since
                    for k in range(len(infected)):
                        if infected[k] in collide:
                            collide.remove(infected[k])
                    for m in range(len(collide)):
                        canvas.itemconfig(ball_position[collide[m]-1].image, fill=INFECTED)
                        infected.append(collide[m])
                # print(infected)

        window.update()

    window.mainloop()


if __name__ == '__main__':
    main()
