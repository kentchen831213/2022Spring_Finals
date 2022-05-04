from tkinter import *
from typing import List, Any
import time
from ball import *
import random
from random import sample, randrange
import matplotlib.pyplot as plt
from math import sqrt
from collections import deque
import csv


SIMULATION_NUM = 1
INITIAL_INFECTED = 2
INITIAL_POPULATION = 100
TRAVELER = 5
RECOVER_TIME = 8
FLIGHT_TIME = 8
W_WIDTH = 1000
W_HEIGHT = 800
BALL_OFFSET = 1
BALL_SIZE = 5
X_SPEED = 3
Y_SPEED = 3
# color codes:
HEALTHY_COLOR = '#aac6ca'
INFECTED_COLOR = '#bb641d'
RECOVERED_COLOR = '#cb8ac0'
TRAVELER_COLOR = '#0084FF'
CSV_FILE = 'data.csv'
RESULT_CSV_FILE = 'result.csv'


def get_random(base_speed: int, exclude_zero=True) -> int:
    """The helper function to randomly assign a speed value for one axis of the ball
    To ensure the ball is always moving, zero is taken away from the generated list
    :param: Base_speed: a non-zero integer given by the user
    :param: Include_zero: To include zero in the random pool or not. By default False
    :return: An int for moving value
    """
    random_speed_list = list(range(-base_speed, base_speed + 1))
    if exclude_zero:
        # Remove zero
        random_speed_list.remove(0)
    return sample(random_speed_list, 1).pop()


def fix_overlap(curcanvas, ob, i):
    overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ob[i].image))
    # Keep moving the ball till the position that is not overlapping with other balls
    while len(overlap_balls) >= 2:
        curcanvas.moveto(overlap_balls[-1],
                    x=random.randint(BALL_OFFSET, (W_WIDTH-20)/2 - BALL_SIZE - 1),
                    y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))
        overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ob[i].image))

def close_window(root):
    root.destroy()

def prepare_graph(curcanvas, ball_objects, infected, infected_queue):

    # creating ball by ball
    for i in range(int((INITIAL_POPULATION + INITIAL_INFECTED)/2)):
        # set the position
        x_coord, y_coord = random.randint(BALL_OFFSET, (W_WIDTH-20)/2 - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        # set the speed
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY_COLOR))
        fix_overlap(curcanvas, ball_objects, i)
        # creating ball by ball
    for i in range(int((INITIAL_POPULATION + INITIAL_INFECTED)/2),(INITIAL_POPULATION + INITIAL_INFECTED)):
        # set the position
        x_coord, y_coord = random.randint(BALL_OFFSET+W_WIDTH/2+10, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        # set the speed
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        # print()
        if i < INITIAL_POPULATION:
            ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY_COLOR))
        else:
            ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, INFECTED_COLOR))
            cur_time = time.time()
            infected.append(i + 2) 
            infected_queue.append([i + 2, cur_time])
        fix_overlap(curcanvas, ball_objects, i)
    return ball_objects, infected, infected_queue


# def update_record(record: dict, curr_infected: list, curr_recovered: list):
#     record["frame"] += 1
#     record["timeline"].append(record["frame"])
#     record["curr_infected"].append(len(curr_infected))
#     record["curr_recovered"].append(len(curr_recovered))
#     record["curr_healthy"].append((INITIAL_POPULATION+INITIAL_INFECTED)-len(curr_infected)-len(curr_recovered))


# def plot_result(record: dict, simulation_number):
#     plt.figure(figsize=(15, 8))
#     plt.plot(record["timeline"], record["curr_infected"], color=INFECTED_COLOR, label="Infected")
#     plt.plot(record["timeline"], record["curr_recovered"], color=RECOVERED_COLOR, label="Recovered")
#     plt.plot(record["timeline"], record["curr_healthy"], color=HEALTHY_COLOR, label="Healthy")
#     plt.xlabel("Frames elapsed")
#     plt.ylabel("Number of cases")
#     plt.figtext(0.02, 0.02,
#                 s="Mask-wearing percentage: {0}\nMask protection rate: {1}".format(RATE_MASK, MASK_PROTECTION_RATE))
#     plt.title("Initial healthy: {0}\nInitial infected: {1}".format(INITIAL_POPULATION, INITIAL_INFECTED), loc="left")
#     plt.title("Change over frames {}".format(simulation_number+1))
#     plt.legend(bbox_to_anchor=(1.01, 1))
#     plt.savefig("result_graph/result_{}.png".format(simulation_number+1))
#     # plt.show()


def output_csv(x_value, infected, recovered, initial_infected, initial_population, fieldnames, filename):
    total_infected_num = len(infected)
    total_recovered_num = len(recovered)-1
    total_healthy_num = initial_infected + initial_population - total_infected_num - total_recovered_num
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "infected": total_infected_num,
            "recovered": total_recovered_num,
            "healthy":total_healthy_num
        }

        csv_writer.writerow(info)

        x_value += 1
    return x_value


def output_result_csv(i, recovered, rate, fieldnames, filename):
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "no.": i,
            "recovered": recovered,
            "healthy": INITIAL_INFECTED + INITIAL_POPULATION - recovered,
            "rate":rate
        }

        csv_writer.writerow(info)


def refresh_graph(window, infected, infected_queue, recovered, ball_objects, curcanvas, initial_infected, initial_population, fieldnames, filename):
    """
    :return: [peak_reach_time], calculate the max infected people and correspond time
    """
    peak_reach_time = (0, 0)
    initial_time = time.time()
    start_time = time.time()
    x_value = 0
    while len(infected) > 0:
        window.after(0)  # the tkinter built-in delay function, the frame is updated 1 frame/ms

        # Have all balls moving
        for i in range(len(ball_objects)):
            ball_objects[i].move()
            # define calculate timer
            timer = time.time()
            # Ball collision detection
            collide = list(curcanvas.find_overlapping(*curcanvas.bbox(ball_objects[i].image)))

            if len(collide) >= 2:
                # When collided, expected ball to bounce off
                ball_objects[i].x_speed *= -1
                ball_objects[i].y_speed *= -1

                # Check if the infected ball(s) is involved in a collision
                check = any(ball_id in collide for ball_id in infected)
                if check:
                    # Once confirmed, removed the infected ones since
                    for j in range(len(collide)):
                        if collide[j] not in recovered and collide[j] not in infected:
                            curcanvas.itemconfig(ball_objects[collide[j] - 2].image, fill=INFECTED_COLOR)
                            infected_time = time.time()
                            infected.append(collide[j])
                            infected_queue.append([collide[j], infected_time])
                            # update the current max number of infected people
                            if len(infected) > peak_reach_time[0]:
                                max_time = time.time()
                                peak_reach_time = (len(infected), max_time-start_time)

            # RECOVER: infected people while be recovered in 10 sec
            while infected_queue and timer-RECOVER_TIME >= infected_queue[0][1]:
                infected_queue.pop(0)
                cur_ball = infected.pop(0)
                curcanvas.itemconfig(ball_objects[cur_ball-2].image, fill=RECOVERED_COLOR)
                recovered.append(cur_ball)


            # Switch people between two countries
            if time.time()-initial_time>=FLIGHT_TIME:
                initial_time = time.time()
                attendants = []
                while len(attendants)<TRAVELER:
                    attendant = randrange(0, 101)
                    if ball_objects[attendant] not in attendants:
                        attendants.append(ball_objects[attendant])
                        if attendants[-1].x > 500:
                            curcanvas.moveto(attendants[-1].image,
                                x=random.randint(BALL_OFFSET, (W_WIDTH-20)/2 - BALL_SIZE - 1),
                                y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))
                            fix_overlap(curcanvas, attendants, -1)
                        else:
                            curcanvas.moveto(attendants[-1].image,
                                x=random.randint(BALL_OFFSET+W_WIDTH/2+10, W_WIDTH - BALL_SIZE - 1),
                                y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))

                            fix_overlap(curcanvas, attendants, -1)
                        # curcanvas.itemconfig(attendants[-1].image, outline=TRAVELER_COLOR)


        # output data to csv for plotting the graph
        x_value = output_csv(x_value, infected, recovered, initial_infected, initial_population, fieldnames, filename)


        window.update()

    close_window(window)
    window.mainloop()
    return len(recovered)-1, peak_reach_time


def bouncing_ball_hp3():

    fieldnames = ["no.", "recovered", "healthy", "rate"]
    with open(RESULT_CSV_FILE, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    for i in range(SIMULATION_NUM):
        # plot_info = {"frame": 0, "timeline": [],
        #              "curr_infected": [], "curr_recovered": [],
        #              "total_healthy": INITIAL_POPULATION, "curr_healthy": []}

        # info = {"recovered":[], "rate": []}

        # Initialize a window
        window = Tk()
        window.geometry("1000x800")
        window.resizable(False, False)

        # A canvas inside window
        canvas = Canvas(window, width=W_WIDTH, height=W_HEIGHT, bg="white")
        canvas.pack()
        canvas.create_rectangle(490,0,510,W_HEIGHT)

        # Place the preferable healthy balls and infected balls on the canvas
        infected = []
        infected_queue = []
        recovered = [1]
        ball_objects = []


        ball_objects, infected, infected_queue = prepare_graph(canvas, ball_objects, infected, infected_queue)

        fieldnames = ["x_value", "infected", "recovered", "healthy"]
        with open(CSV_FILE, 'w') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            csv_writer.writeheader()

        total_infected, peak = refresh_graph(window, infected, infected_queue, recovered, ball_objects, canvas, INITIAL_INFECTED, INITIAL_POPULATION, fieldnames, CSV_FILE)
        print(peak)
        # info["recovered"].append(total_infected)
        # info["rate"].append(peak[0]/peak[1])

        fieldnames = ["no.", "recovered", "healthy", "rate"]
        output_result_csv(i, total_infected, peak[0]/peak[1], fieldnames, RESULT_CSV_FILE)

        

    #     if max_number_infect[0][0] == 0:
    #         continue
    #     else:
    #         print("check {} slope".format(i+1))
    #         print((max_number_infect[0][0]-INITIAL_INFECTED)/(max_number_infect[0][1]-start_time), end="\n")
    #         cur_sloop = (max_number_infect[0][0]-INITIAL_INFECTED)/(max_number_infect[0][1]-start_time)
    #         if len(slope) == 0 or cur_sloop < min(slope):
    #             print("it's current smallest slope")
    #             # call plot_result()
    #             plot_result(plot_info, i)
    #         slope.append(cur_sloop)

    # print("average slope is {}".format(sum(slope)/SIMULATION_NUM))


if __name__ == '__main__':
    bouncing_ball_hp3()