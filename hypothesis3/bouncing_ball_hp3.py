from tkinter import *
from typing import List, Tuple
import time
from ball import *
import random
from random import sample, randrange
import csv

INITIAL_INFECTED = 2
INITIAL_POPULATION = 100
RECOVER_TIME = 8
FLIGHT_TIME = 8
W_WIDTH = 1000
W_HEIGHT = 800
BALL_OFFSET = 1
BALL_SIZE = 5
X_SPEED = 1
Y_SPEED = 1
# color codes:
HEALTHY_COLOR = '#aac6ca'
INFECTED_COLOR = '#bb641d'
RECOVERED_COLOR = '#cb8ac0'
TRAVELER_COLOR = '#0084FF'
CSV_FILE = 'data.csv'
RESULT_CSV_FILE = 'result.csv'


def get_random(base_speed: int, exclude_zero=True) -> int:
    """Randomly assign a speed value for one axis of the ball
    To ensure the ball is always moving, zero is taken away from the generated list
    :param: Base_speed: a non-zero integer given by the user
    :param: exclude_zero: To include zero in the random pool or not. By default, False
    :return: An int for moving value
    >>> get_random(3) != 0
    True
    >>> 4 >= get_random(4) >= -4
    True
    """
    random_speed_list = list(range(-base_speed, base_speed + 1))
    if exclude_zero:
        # Remove zero
        random_speed_list.remove(0)
    return sample(random_speed_list, 1).pop()


def fix_overlap(curcanvas: object, ob_list: List, position: int, left: float, right: float,
                bottom: int, up: int) -> None:
    """Keep moving the ball till the place that is not overlapping with other balls
    :param curcanvas: the canvas which the ball is on
    :param ob_list: a list of ball objects
    :param position: the position in the list where the ball object is
    :param left: the left boundary on the canvas to move the ball to
    :param right: the right boundary on the canvas to move the ball to
    :param bottom: the bottom boundary on the canvas to move the ball to
    :param up: the upper boundary on the canvas  to move the ball to
    :return: None
    """
    overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ob_list[position].image))
    while len(overlap_balls) >= 2:
        curcanvas.moveto(overlap_balls[-1],
                         x=random.randint(left, right),
                         y=random.randint(bottom, up))
        overlap_balls = curcanvas.find_overlapping(*curcanvas.bbox(ob_list[position].image))


def close_window(root):
    root.destroy()


def prepare_graph(curcanvas, ball_objects: List, infected: List,
                  infected_queue: List[List]) -> Tuple[List, List, List]:
    """ Prepare the initial graph and put in ball by ball
    :param curcanvas: the canvas which the ball is on
    :param ball_objects: a list of ball objects
    :param infected: a list that store the index of infected balls
    :param infected_queue: a list that store the index of infected balls and their infected time for calculating when it
            will be recovered
    :return:
        - ball_objects - a list of ball objects
        - infected - a list that store the index of infected balls
        - infected_queue - a list that store the index of infected balls and their infected time for calculating when it
            will be recovered
    """
    # creating ball by ball
    for i in range(int((INITIAL_POPULATION + INITIAL_INFECTED) / 2)):
        # set the position
        x_coord, y_coord = random.randint(BALL_OFFSET, (W_WIDTH - 20) / 2 - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        # set the speed
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)
        ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY_COLOR))
        fix_overlap(curcanvas, ball_objects, i, BALL_OFFSET, (W_WIDTH - 20) / 2 - BALL_SIZE - 1,
                    BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        # creating ball by ball
    for i in range(int((INITIAL_POPULATION + INITIAL_INFECTED) / 2), (INITIAL_POPULATION + INITIAL_INFECTED)):
        # set the position
        x_coord, y_coord = random.randint(BALL_OFFSET + W_WIDTH / 2 + 10, W_WIDTH - BALL_SIZE - 1), \
                           random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
        # set the speed
        dx, dy = get_random(X_SPEED, True), get_random(Y_SPEED, True)

        if i < INITIAL_POPULATION:
            ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, HEALTHY_COLOR))
        else:
            ball_objects.append(Ball(curcanvas, x_coord, y_coord, 10, dx, dy, INFECTED_COLOR))
            cur_time = time.time()
            infected.append(i + 2)
            infected_queue.append([i + 2, cur_time])
        fix_overlap(curcanvas, ball_objects, i, BALL_OFFSET + W_WIDTH / 2 + 10, W_WIDTH - BALL_SIZE - 1,
                    BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)

    return ball_objects, infected, infected_queue


def output_csv(x_value: int, infected: List, recovered: List, initial_infected: int, initial_population: int,
               fieldnames: List, filename: str) -> int:
    """for each movement of the balls output the result to csv file for real time plotting
    :param x_value: the index of the movement
    :param infected: the current infected balls
    :param recovered: the current recovered balls
    :param initial_infected: the initial infected balls
    :param initial_population: the initial healthy balls
    :param fieldnames: the field names in the csv file
    :param filename: the csv file name to store the information
    :return: the next index value
    """
    total_infected_num = len(infected)
    total_recovered_num = len(recovered) - 1
    total_healthy_num = initial_infected + initial_population - total_infected_num - total_recovered_num
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "x_value": x_value,
            "infected": total_infected_num,
            "recovered": total_recovered_num,
            "healthy": total_healthy_num
        }

        csv_writer.writerow(info)

        x_value += 1
    return x_value


def output_result_csv(i: int, recovered: int, rate: float, fieldnames: List, filename: str) -> None:
    """for each simulation output the result
    :param i: the index of the simulation
    :param recovered: total recovered balls
    :param rate: number of balls getting infected per second
    :param fieldnames: the field names in the csv file
    :param filename: the csv file name to store the information
    :return: None
    """
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "no.": i,
            "recovered": recovered,
            "healthy": INITIAL_INFECTED + INITIAL_POPULATION - recovered,
            "rate": rate
        }

        csv_writer.writerow(info)


def refresh_graph(window, infected: List, infected_queue: List, recovered: List, ball_objects: List, curcanvas,
                  initial_infected: int, initial_population: int, fieldnames: List, filename: str,
                  traveler_num: int) -> Tuple[int, Tuple]:
    """keep the ball bouncing on the canvas till there's no infected balls
    :param window: the window for the graph
    :param infected: the current infected balls
    :param infected_queue: a list that store the index of infected balls and their infected time for calculating when it
            will be recovered
    :param recovered: the current recovered balls
    :param ball_objects: a list of ball objects
    :param curcanvas: the canvas which the ball is on
    :param initial_infected: the initial infected balls
    :param initial_population: the initial healthy balls
    :param fieldnames: the field names in the csv file
    :param filename: the csv file name to store the information
    :param traveler_num: number of balls getting to travel from one side of canvas to the other entered by the user
    :return:
        - number of total people that recovered
        - calculate the max infected people and correspond time
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
                                peak_reach_time = (len(infected), max_time - start_time)

            # RECOVER: infected people while be recovered in 10 sec
            while infected_queue and timer - RECOVER_TIME >= infected_queue[0][1]:
                infected_queue.pop(0)
                cur_ball = infected.pop(0)
                curcanvas.itemconfig(ball_objects[cur_ball - 2].image, fill=RECOVERED_COLOR)
                recovered.append(cur_ball)

            # Switch people between two countries
            if time.time() - initial_time >= FLIGHT_TIME:
                initial_time = time.time()
                attendants = []
                while len(attendants) < traveler_num:
                    attendant = randrange(0, 101)
                    if ball_objects[attendant] not in attendants:
                        attendants.append(ball_objects[attendant])
                        if attendants[-1].x > 500:
                            curcanvas.moveto(attendants[-1].image,
                                             x=random.randint(BALL_OFFSET, (W_WIDTH - 20) / 2 - BALL_SIZE - 1),
                                             y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))
                            fix_overlap(curcanvas, attendants, -1, BALL_OFFSET + W_WIDTH / 2 + 10,
                                              W_WIDTH - BALL_SIZE - 1, BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)
                        else:
                            curcanvas.moveto(attendants[-1].image,
                                             x=random.randint(BALL_OFFSET + W_WIDTH / 2 + 10, W_WIDTH - BALL_SIZE - 1),
                                             y=random.randint(BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1))
                            fix_overlap(curcanvas, attendants, -1, BALL_OFFSET, (W_WIDTH - 20) / 2 - BALL_SIZE - 1,
                                        BALL_OFFSET, W_HEIGHT - BALL_SIZE - 1)

        # output data to csv for plotting the graph
        x_value = output_csv(x_value, infected, recovered, initial_infected, initial_population, fieldnames, filename)

        window.update()

    close_window(window)
    window.mainloop()
    return len(recovered) - 1, peak_reach_time


def bouncing_ball_hp3(simulation_num: int, traveler_num: int) -> None:
    """use balls bouncing on the canvas to simulate the covid 19 spread
    :param simulation_num: number of times to simulate entered by the user
    :param traveler_num: number of balls getting to travel from one side of canvas to the other entered by the user
    :return: None
    """
    fieldnames = ["no.", "recovered", "healthy", "rate"]
    with open(RESULT_CSV_FILE, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    for i in range(simulation_num):
        # Initialize a window
        window = Tk()
        window.geometry("1000x800")
        window.resizable(False, False)

        # A canvas inside window
        canvas = Canvas(window, width=W_WIDTH, height=W_HEIGHT, bg="white")
        canvas.pack()
        canvas.create_rectangle(490, 0, 510, W_HEIGHT)

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

        total_infected, peak = refresh_graph(window, infected, infected_queue, recovered, ball_objects, canvas,
                                             INITIAL_INFECTED, INITIAL_POPULATION, fieldnames, CSV_FILE, traveler_num)

        fieldnames = ["no.", "recovered", "healthy", "rate"]
        output_result_csv(i, total_infected, peak[0] / peak[1], fieldnames, RESULT_CSV_FILE)


def validate_input() -> Tuple[int, int]:
    """
    Allow users to input the simulation number and number of people that could travel for a certain period of time
    Validate the input and ask the user to input again if needed
    :return:
        - sim_num - simulation number
        - trav_num - number of people that could travel for a certain period of time
    """
    while True:
        try:
            sim_num = int(input('Please enter simulation number: '))
        except ValueError:
            print('Please enter a valid number')
            continue
        else:
            break

    while True:
        try:
            trav_num = int(
                input('Please enter how many people could travel per a period of time (number between 0 and 100): '))
        except ValueError:
            print('Please enter a valid number between 0 and 100')
            continue
        else:
            if trav_num > 100 or trav_num < 0:
                print('Please enter a valid number between 0 and 100')
                continue
            break
    return sim_num, trav_num


if __name__ == '__main__':
    s_num, t_num = validate_input()
    bouncing_ball_hp3(s_num, t_num)
