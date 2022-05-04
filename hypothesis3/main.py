from threading import Thread
from bouncing_ball_hp3 import bouncing_ball_hp3
from plt_hp3 import plt_hp3
from multiprocessing import Process



if __name__ == '__main__':
    p1 = Process(target = bouncing_ball_hp3)
    p2 = Process(target = plt_hp3)
    p1.start()
    p2.start()
