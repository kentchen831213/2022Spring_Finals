import pandas as pd
import matplotlib.pyplot as plt
import sys


def making_hist(csv_name) -> None:
    """plotting the histogram of infected rate for the simulations
    :param csv_name: the csv file that store the information for each simulation
    :return: None
    """
    df = pd.read_csv(csv_name, usecols=['rate'])

    print("Statistics of the simulation: ")
    print(df.describe())

    plt.hist(df['rate'], bins=10)
    plt.show()


def computing_mean(csv_name) -> None:
    """calculating the mean total infected people for all simulations
    :param csv_name: the csv file that store the information for each simulation
    :return: None
    """
    df = pd.read_csv(csv_name, usecols=['recovered'])

    print("The mean total infected people for each simulation is: ", df.mean().values[0])


if __name__ == '__main__':
    file = sys.argv[1]
    computing_mean(file)
    making_hist(file)
