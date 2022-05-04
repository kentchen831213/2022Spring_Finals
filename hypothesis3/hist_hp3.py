import pandas as pd
import matplotlib.pyplot as plt

def making_hist(csv_name):
    df=pd.read_csv(csv_name, usecols=['healthy'])

    # print(df.describe())

    # plt.hist(df['rate'],bins=10)
    # plt.show()

    print(df.mean())

if __name__ == '__main__':
    making_hist('result_5.csv')