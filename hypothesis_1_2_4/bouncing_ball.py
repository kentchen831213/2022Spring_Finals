from tkinter import *
from typing import List, Any
import time
import ball
from ball import *
import random
from random import sample
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
from collections import deque

HYPOTHESIS = "hypothesis4"
SIMULATION_NUM = 100
POPULATION = 100
INFECTED_CASE = 2
W_WIDTH = 1000
W_HEIGHT = 800
BALL_OFFSET = 1
BALL_SIZE = 5
X_SPEED = 2
Y_SPEED = 2
RECOVER_TIME = 8
FRAME_RATE = 1 / 240
RATE_MASK = 1.0
RATE_VACCINE = 0.5
MASK_PROTECTION_RATE = 0.66
VACCINE_PROTECTION_RATE = 0.72
DECREASE_RATE = 0.2
# color codes:
HEALTHY = '#aac6ca'
INFECTED = '#bb641d'
RECOVERED = '#cb8ac0'
MASK = False
VACCINE = False


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


def close_window(root):
    """
    This function is to close the simulation window
    :param root: the window to simulate Epidemic transmission
    :return:
    """
    root.destroy()


# hypothesis1: Assume wearing a facemask is mandated, a sweet spot for vaccination coverage rate exists
def vaccine_test():
    """
    This function is prepare all the parameters for hypothesis1(vaccine test)
    :return: None
    """
    # all people wearing mask
    mask_list = [1]*(POPULATION+INFECTED_CASE)
    # taking vaccine or not
    rate_list = [0, 1]
    vaccine_list = random.choices(rate_list, weights=[1-RATE_VACCINE, RATE_VACCINE], k=POPULATION+INFECTED_CASE)
    prepare_graph(canvas, mask_list, vaccine_list)


# hypothesis2:  testing how many wearing mask can prevent epidemic
def mask_test():
    """
    This function is prepare all the parameters for hypothesis2(mask test)
    :return: None
    """
    # all people not taking vaccine
    vaccine_list = [0]*(POPULATION+INFECTED_CASE)
    # wearing mask or not
    rate_list = [0, 1]
    # define a mask_list
    mask_list = random.choices(rate_list, weights=[1-RATE_MASK, RATE_MASK], k=POPULATION+INFECTED_CASE)
    prepare_graph(canvas, mask_list, vaccine_list)


# hypothesis4: Will vaccine effectiveness degradation affect curve-flattening?
def decrease_protect_test():
    """
    This function is prepare all the parameters for hypothesis4(vaccine protection decrease test)
    :return: None
    """
    # all people wearing mask
    mask_list = [1] * (POPULATION + INFECTED_CASE)
    # taking vaccine or not
    rate_list = [0, 1]
    vaccine_list = random.choices(rate_list, weights=[1 - RATE_VACCINE, RATE_VACCINE], k=POPULATION + INFECTED_CASE)
    prepare_graph(canvas, mask_list, vaccine_list)


def prepare_graph(curcanvas, having_mask, having_vaccine):

    for i in range(POPULATION + INFECTED_CASE):
        x_coord, y_coord = random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        if i < POPULATION:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, HEALTHY)

            # if taking vaccine, put the current time and protection rate
            if having_vaccine[i]:
                ball_position.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY, having_mask[i], having_vaccine[i], time.time(), VACCINE_PROTECTION_RATE))
            else:
                ball_position.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY, having_mask[i], having_vaccine[i], 0, 0))

            if having_mask[i]:
                mask.append(i+1)
            if having_vaccine[i]:
                vaccine.append(i+1)
        else:
            # ball_position[i] = Ball(canvas, x_coord, y_coord, 10, dx, dy, INFECTED)
            ball_position.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, INFECTED, having_mask[i], having_vaccine[i], time.time(), VACCINE_PROTECTION_RATE))
            cur_time = time.time()
            infected.append(i + 1)  # The
            infected_queue.append([i + 1, cur_time])

        overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ball_position[i].image))

        # Replace the ball that is overlapping with another
        if len(overlap_balls) >= 2:  # The length of tuple suggested an overlap issue between two or more balls
            # Move the last rendered ball to a new random location
            curcanvas.moveto(overlap_balls[1],
                          x=random.randint(BALL_OFFSET, W_WIDTH - BALL_SIZE - 1),
                          y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))


def update_record(record: dict, curr_infected: list, curr_recovered: list):
    record["frame"] += 1
    record["timeline"].append(record["frame"])
    record["curr_infected"].append(len(curr_infected))
    record["curr_recovered"].append(len(curr_recovered))
    record["curr_healthy"].append((POPULATION+INFECTED_CASE)-len(curr_infected)-len(curr_recovered))


def refresh_graph(number_infect, total_infected_people, hy4):
    """
    :param number_infect: the number of infected people
    :param total_infected_people:
    :return: [max_infect_time], calculate the max infected people and correspond time,
    """
    max_infect_time = [(0, 0)]
    while len(infected) > 0:
        window.after(1)  # the tkinter built-in delay function, the frame is updated 1 frame/ms
        timer = time.time()

        # Have all balls moving
        for i in range(len(ball_position)):
            ball_position[i].move()

            # Ball collision detection
            collide = list(canvas.find_overlapping(*canvas.bbox(ball_position[i].image)))
            if len(collide) >= 2:
                # When collided, expected ball to bounce off
                ball_position[i].x_speed *= -1
                ball_position[i].y_speed *= -1

                # Check if the infected ball(s) is involved in a collision
                check = any(ball_id in collide for ball_id in infected)
                if check:
                    # Once confirmed, removed the infected ones since
                    for k in range(len(infected)):
                        if infected[k] in collide:
                            collide.remove(infected[k])
                    for m in range(len(collide)):
                        if collide[m] not in recovered:
                            # if people wearing mask
                            if collide[m] in mask:
                                infected_rate = [0, 1]
                                mask_list = random.choices(infected_rate, weights=[MASK_PROTECTION_RATE, 1-MASK_PROTECTION_RATE])
                                # if peopel wearning mask but still be infected
                                if mask_list[0]:
                                    # if people taking vaccine
                                    if collide[m] in vaccine:
                                        cur_protect_rate = ball_position[collide[m]-1].protect_rate
                                        vaccine_list = random.choices(infected_rate, weights=[cur_protect_rate, 1-cur_protect_rate])
                                        # if people taking vaccine still be infected
                                        if vaccine_list[0]:
                                            canvas.itemconfig(ball_position[collide[m] - 1].image, fill=INFECTED)
                                            infected_time = time.time()
                                            infected.append(collide[m])
                                            total_infected_people += 1
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
                                        total_infected_people += 1
                                        infected_queue.append([collide[m], infected_time])
                                        if len(infected) > number_infect:
                                            number_infect = len(infected)
                                            max_time = time.time()
                                            max_infect_time = [(number_infect, max_time)]
                            else:
                                canvas.itemconfig(ball_position[collide[m]-1].image, fill=INFECTED)
                                infected_time = time.time()
                                infected.append(collide[m])
                                total_infected_people += 1
                                infected_queue.append([collide[m], infected_time])
                                if len(infected) > number_infect:
                                    number_infect = len(infected)
                                    max_time = time.time()
                                    max_infect_time = [(number_infect, max_time)]

            # infected people while be recovered in 8 sec
            while infected_queue and timer-RECOVER_TIME >= infected_queue[0][1]:
                infected_queue.pop(0)
                cur_ball = infected.pop(0)
                canvas.itemconfig(ball_position[cur_ball-1].image, fill=RECOVERED)
                recovered.append(cur_ball)

            # hypothesis 4, decrease the protection rate of taking vaccine people every 5 seconds
            if hy4:
                cur_time = time.time()
                for idx in range(len(vaccine)):
                    if cur_time-ball_position[vaccine[idx]-1].time >= 5:
                        if ball_position[vaccine[idx]-1].protect_rate > DECREASE_RATE:
                            ball_position[vaccine[idx] - 1].time = cur_time
                            ball_position[vaccine[idx]-1].protect_rate -= DECREASE_RATE

        update_record(plot_info, infected, recovered)
        window.update()

    close_window(window)
    window.mainloop()
    return max_infect_time, total_infected_people


def plot_result(record: dict, simulation_number, key):
    plt.figure(figsize=(15, 8))
    plt.plot(record["timeline"], record["curr_infected"], color=INFECTED, label="Infected")
    plt.plot(record["timeline"], record["curr_recovered"], color=RECOVERED, label="Recovered")
    plt.plot(record["timeline"], record["curr_healthy"], color=HEALTHY, label="Healthy")
    plt.xlabel("Frames elapsed")
    plt.ylabel("Number of cases")
    if key == "hypothesis1":
        plt.figtext(0.01, 0.01,
                    s=f"Mask-wearing percentage: {RATE_MASK}\nMask protection rate: {MASK_PROTECTION_RATE}\nVaccine "
                      f"coverage rate: {RATE_VACCINE}\nVaccine protection rate: {VACCINE_PROTECTION_RATE}")
    elif key == "hypothesis2":
        plt.figtext(0.02, 0.02,
                    s="Mask-wearing percentage: {0}\nMask protection rate: {1}".format(RATE_MASK, MASK_PROTECTION_RATE))
    elif key == "hypothesis4":
        plt.figtext(0.01, 0.01,
                    s=f"Vaccine coverage rate: {RATE_VACCINE}\nVaccine protection rate: {VACCINE_PROTECTION_RATE}\n"
                    f"Protection rate decreases each 5 seconds\nDecrease rate: {DECREASE_RATE}")
    plt.title("Initial healthy: {0}\nInitial infected: {1}".format(POPULATION, INFECTED_CASE), loc="left")
    plt.title("Change over frames {}".format(simulation_number+1))
    plt.legend(bbox_to_anchor=(1.01, 1))
    plt.savefig("result_graph/{}_result_{}.png".format(key, simulation_number+1))


def plot_simulation_result(key):

    if key == "hypothesis1":
        print("hypothesis1 summary:")
        print("the cover rate of vaccine is {}".format(RATE_VACCINE))
    elif key == "hypothesis2":
        print("hypothesis2 summary:")
        print("the cover rate of mask is {}".format(RATE_MASK))
    elif key == "hypothesis4":
        print("hypothesis4 summary:")
        print("the decrease rate of vaccine protection is {}".format(DECREASE_RATE))

    #  plot the simulation result for each hypothesis
    plt.hist(sloop, bins=7, density=True)
    plt.figure()
    plt.show()
    print("{} person be infected every seconds".format(sum(sloop) / SIMULATION_NUM))
    print("average healthy rate is {}".format(sum(avg_healthy) / SIMULATION_NUM))
    print("average infected rate is {}\n".format(sum(avg_infected) / SIMULATION_NUM))


if __name__ == '__main__':

    # define sloop to calculate the curve of graph
    sloop = []
    avg_healthy = []
    avg_infected = []

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

        # prepare all the list that need to record the infected and recovered people
        infected = []
        infected_queue = []
        recovered = []
        ball_position = []
        mask = []
        vaccine = []
        max_number_infect = 0
        total_infected_case = 0
        start_time = time.time()

        # hypothesis1
        if HYPOTHESIS == "hypothesis1":
            vaccine_test()
            max_number_infect, total_infected_case = refresh_graph(max_number_infect, INFECTED_CASE, False)

        # hypothesis2
        elif HYPOTHESIS == "hypothesis2":
            mask_test()
            max_number_infect, total_infected_case = refresh_graph(max_number_infect, INFECTED_CASE, False)

        # hypothesis4
        elif HYPOTHESIS == "hypothesis4":
            decrease_protect_test()
            max_number_infect, total_infected_case = refresh_graph(max_number_infect, INFECTED_CASE, True)

        if max_number_infect[0][0] == 0:
            continue
        else:
            cur_sloop = (max_number_infect[0][0]-INFECTED_CASE)/(max_number_infect[0][1]-start_time)
            if len(sloop) == 0 or cur_sloop > max(sloop):
                plot_result(plot_info, i, HYPOTHESIS)
            avg_healthy.append(POPULATION+INFECTED_CASE-total_infected_case)
            avg_infected.append(total_infected_case)
            sloop.append(cur_sloop)

    # plot simulation result for each hypothesis
    plot_simulation_result(HYPOTHESIS)


