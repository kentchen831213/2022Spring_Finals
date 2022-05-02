from tkinter import *
from typing import List, Any
import time
import ball
from ball import *
import random
from random import sample
import matplotlib.pyplot as plt
from math import sqrt
from collections import deque

SIMULATION_NUM = 1
POPULATION = 100
W_WIDTH = 1000
W_HEIGHT = 800
BALL_OFFSET = 1
BALL_SIZE = 5
X_SPEED = 2
Y_SPEED = 2
RECOVER_TIME = 8
FRAME_RATE = 1 / 240
INFECTED_CASE = 1
MASK_PROTECTION_RATE = 0.83
# color codes:
HEALTHY = '#aac6ca'
INFECTED = '#bb641d'
RECOVERED = '#cb8ac0'
MASK = False
VACCINE = False
RATE_MASK = 0.8


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


# def is_ball_collision(the_canvas, ball_coord: list):
#     for i in range(len(ball_coord)):
#         collide_ball_id = the_canvas.find_overlapping(*the_canvas.bbox(ball_coord[i].image))


def close_window(root):
    root.destroy()


# hypothesis2:  testing how many wearing mask can prevent epidemic
def mask_test():

    # wearing mask or not
    rate_list = [0, 1]

    # define a mask_list
    mask_list = random.choices(rate_list, weights=[1-RATE_MASK, RATE_MASK], k=POPULATION+INFECTED_CASE)
    prepare_graph(canvas, mask_list, 0)


def prepare_graph(curcanvas, having_mask, vaccine1):

    start_time = time.time()
    for i in range(POPULATION + INFECTED_CASE):
        x_coord, y_coord = random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        if i < POPULATION:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY)
            ball_position.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY, having_mask[i], VACCINE))
            # print("test123")
            # print(having_mask[i])
            if having_mask[i]:
                mask.append(i+1)
        else:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED)
            ball_position.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, INFECTED, having_mask[i], VACCINE))
            cur_time = time.time()
            infected.append(i + 1)  # The
            infected_queue.append([i + 1, cur_time])

        # print(ball_position[i], ball_position[i].x, ball_position[i].y)
        overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ball_position[i].image))

        # Replace the ball that is overlapping with another
        if len(overlap_balls) >= 2:  # The length of tuple suggested an overlap issue between two or more balls
            # Move the last rendered ball to a new random location
            curcanvas.moveto(overlap_balls[1],
                          x=random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1),
                          y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))

        # print(overlap_balls, len(overlap_balls))
    # print("end")


def update_record(record: dict, curr_infected: list, curr_recovered: list):
    record["frame"] += 1
    record["timeline"].append(record["frame"])
    record["curr_infected"].append(len(curr_infected))
    record["curr_recovered"].append(len(curr_recovered))
    record["curr_healthy"].append((POPULATION+INFECTED_CASE)-len(curr_infected)-len(curr_recovered))


def plot_result(record: dict, simulation_number):
    plt.figure(figsize=(15, 8))
    plt.plot(record["timeline"], record["curr_infected"], color=INFECTED, label="Infected")
    plt.plot(record["timeline"], record["curr_recovered"], color=RECOVERED, label="Recovered")
    plt.plot(record["timeline"], record["curr_healthy"], color=HEALTHY, label="Healthy")
    plt.xlabel("Frames elapsed")
    plt.ylabel("Number of cases")
    plt.figtext(0.02, 0.02,
                s="Mask-wearing percentage: {0}\nMask protection rate: {1}".format(RATE_MASK, MASK_PROTECTION_RATE))
    plt.title("Initial healthy: {0}\nInitial infected: {1}".format(POPULATION, INFECTED_CASE), loc="left")
    plt.title("Change over frames {}".format(simulation_number+1))
    plt.legend(bbox_to_anchor=(1.01, 1))
    plt.savefig("result_graph/result_{}.png".format(simulation_number+1))
    # plt.show()


def refresh_graph(number_infect):
    """
    :param number_infect: the number of infected people
    :return: [max_infect_time], calculate the max infected people and correspond time
    """
    while len(infected) > 0:
        window.after(1)  # the tkinter built-in delay function, the frame is updated 1 frame/ms
        # for key, val in ball_position.items():
        #     ball_position[key].move()

        # Have all balls moving
        for i in range(len(ball_position)):
            ball_position[i].move()

            # define calculate timer
            timer = time.time()
            # Ball collision detection
            collide = list(canvas.find_overlapping(*canvas.bbox(ball_position[i].image)))
            if len(collide) >= 2:
                # When collided, expected ball to bounce off
                ball_position[i].x_speed *= -1
                ball_position[i].y_speed *= -1
                # print(collide, ball_position[collide[0] - 1].x_speed, ball_position[collide[0] - 1].y_speed,
                #       ball_position[collide[1] - 1].x_speed, ball_position[collide[1] - 1].y_speed)
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
                        if collide[m] not in recovered:
                            if collide[m] in mask:
                                infected_rate = [0, 1]
                                mask_list = random.choices(infected_rate, weights=[MASK_PROTECTION_RATE, 1-MASK_PROTECTION_RATE])
                                if mask_list[0]:
                                    # print("check")
                                    # print(mask_list[0])
                                    canvas.itemconfig(ball_position[collide[m] - 1].image, fill=INFECTED)
                                    # plot_info["total_healthy"] -= len(infected)
                                    infected_time = time.time()
                                    infected.append(collide[m])
                                    infected_queue.append([collide[m], infected_time])
                                    # update the current max number of infected people
                                    if len(infected) > number_infect:
                                        number_infect = len(infected)
                                        max_time = time.time()
                                        max_infect_time = [(number_infect, max_time)]
                            else:
                                canvas.itemconfig(ball_position[collide[m]-1].image, fill=INFECTED)
                                infected_time = time.time()
                                infected.append(collide[m])
                                infected_queue.append([collide[m], infected_time])
                                if len(infected) > number_infect:
                                    number_infect = len(infected)
                                    max_time = time.time()
                                    max_infect_time = [(number_infect, max_time)]
                                # plot_info["total_healthy"] -= len(infected)
                # print(infected)

            # infected people while be recovered in 10 sec
            while infected_queue and timer-RECOVER_TIME >= infected_queue[0][1]:
                infected_queue.pop(0)
                cur_ball = infected.pop(0)
                canvas.itemconfig(ball_position[cur_ball-1].image, fill=RECOVERED)
                recovered.append(cur_ball)

        update_record(plot_info, infected, recovered)
        window.update()

    close_window(window)
    window.mainloop()
    return max_infect_time


if __name__ == '__main__':

    sloop = []
    # declare plot_info

    for i in range(SIMULATION_NUM):
        plot_info = {"frame": 0, "timeline": [],
                     "curr_infected": [], "curr_recovered": [],
                     "total_healthy": POPULATION, "curr_healthy": []}

        # Initialize a window
        window = Tk()
        window.geometry("1000x800")
        window.resizable(False, False)

        # A canvas inside window
        canvas = Canvas(window, width=W_WIDTH, height=W_HEIGHT, bg="white")
        canvas.pack()

        # Place the preferable healthy balls and infected balls on the canvas
        # ball_position = {}
        infected = []
        infected_queue = []
        recovered = []
        ball_position = []
        mask = []
        max_number_infect = 0
        start_time = time.time()
        # prepare_graph(canvas, [0]*(POPULATION+INFECTED_CASE), 0)

        # hypothesis2
        mask_test()
        max_number_infect = refresh_graph(max_number_infect)

        print("check {} sloop".format(i+1))
        print((max_number_infect[0][0]-INFECTED_CASE)/(max_number_infect[0][1]-start_time), end="\n")
        cur_sloop = (max_number_infect[0][0]-INFECTED_CASE)/(max_number_infect[0][1]-start_time)
        if len(sloop) == 0 or cur_sloop < min(sloop):
            print("it's current smallest sloop")
            # call plot_result()
            plot_result(plot_info, i)
        sloop.append(cur_sloop)

    print("average sloop is {}".format(sum(sloop)/SIMULATION_NUM))



