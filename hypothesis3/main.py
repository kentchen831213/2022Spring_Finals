from bouncing_ball_hp3 import bouncing_ball_hp3
from plt_hp3 import plt_hp3
from multiprocessing import Process



if __name__ == '__main__':
    while True:
        try:
            simulation_num = int(input('Please enter simulation number: '))
        except:
            print('Please enter a valid number')
            continue
        else:
            break

    while True:
        try:
            traveler_num = int(input('Please enter how many people could travel per a period of time (number between 0 and 100): '))
        except:
            print('Please enter a valid number between 0 and 100')
            continue
        else:
            if traveler_num >100 or traveler_num <0:
                continue
            break
    p1 = Process(target = bouncing_ball_hp3, args=(simulation_num, traveler_num,))
    p2 = Process(target = plt_hp3)
    p1.start()
    p2.start()
