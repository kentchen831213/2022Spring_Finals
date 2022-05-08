import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate(i) -> None:
    """real time getting the infected people, healthy people and recovered people data
    :param i:
    :return: None
    """
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['infected']
    y2 = data['recovered']
    y3 = data['healthy']
    infected = "infected: " + str(y1.values[-1])
    recovered = "recovered: " + str(y2.values[-1])
    healthy = "healthy:" + str(y3.values[-1])

    plt.cla()
    plt.plot(x, y1, label=infected)
    plt.plot(x, y2, label=recovered)
    plt.plot(x, y3, label=healthy)
    plt.xlabel("Change over time")
    plt.ylabel("Number of People")

    plt.legend(loc='upper left')
    plt.tight_layout()


def plt_hp3() -> None:
    """
    plotting the graph for infected people, healthy people and recovered people
    :return: None
    """
    plt.style.use('fivethirtyeight')

    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plt_hp3()
