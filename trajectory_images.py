import argparse
import pandas as pd
from load_dataset import convert_to_vector
import matplotlib.pyplot as plt


def plot_traj(csv_path):
    #csv_path = 'summarize_test.csv'
    data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["image_path", "predicted", "real"])
    #print(data_df)

    predicted = []
    real = []
    for k in range(len(data_df['predicted'].values)):
        predicted.append(convert_to_vector(data_df['predicted'].values[k]))
        real.append(convert_to_vector(data_df['real'].values[k]))

    #print('REAL', ((real[0])) , '\n')
    #print('pred', ((predicted[0]))  , '\n')

    # #fig = plt.figure(figsize=(15, 15))
    ax = plt.axes()
    for i in range(len(real)):
        for j in range(len(real[i])):
            #print(real[i][j][0], real[i][j][1])
            plt.plot(real[i][j][0], real[i][j][1], color="green", marker=".", linestyle="")
            plt.plot(predicted[i][j][0], predicted[i][j][1], color="magenta", marker="*", linestyle="")  # linestyle=""

    # Give labels
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    #plt.ylim([1, -80])
    #plt.xlim([-10, 70])
    # plt.gca().invert_yaxis() # origine asse z (y) in basso a sinistra
    plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plots the real and predicted trajectories using the csv file")

    parser.add_argument("--csv_path", dest="path", default=None, help="Path of the csv file")
    args = parser.parse_args()
    plot_traj(csv_path=args.path)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
