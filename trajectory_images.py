import argparse
import pandas as pd
from load_dataset import convert_to_vector
import matplotlib.pyplot as plt
from comet_ml import Experiment
# import matplotlib as mpl
#
# mpl.use('Agg')


def plot_traj(csv_path):
    # csv_path = 'summarize_test.csv'
    data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["image_path", "predicted", "real"])
    # print(data_df)

    predicted = []
    real = []
    for k in range(len(data_df['predicted'].values)):
        predicted.append(convert_to_vector(data_df['predicted'].values[k]))
        real.append(convert_to_vector(data_df['real'].values[k]))

    # print('REAL', ((real[0])) , '\n')
    # print('pred', ((predicted[0]))  , '\n')

    # #fig = plt.figure(figsize=(15, 15))
    ax = plt.axes()
    for i in range(len(real)):
        for j in range(len(real[i])):
            # print(real[i][j][0], real[i][j][1])
            plt.plot(real[i][j][0], real[i][j][1], color="green", marker=".", linestyle="")
            plt.plot(predicted[i][j][0], predicted[i][j][1], color="magenta", marker="*", linestyle="")  # linestyle=""

    # Give labels
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    # plt.ylim([1, -80])
    # plt.xlim([-10, 70])
    # plt.gca().invert_yaxis() # origine asse z (y) in basso a sinistra
    plt.show()


def plot_data(real, predicted, experiment, k, l, path, epoch, type_name):  # plotta singole 'righe' csv (real, predicted)
    ax = plt.axes()

    plt.plot(real[:, 0], real[:, 1], color="green", marker=".")
    plt.plot(predicted[:, 0], predicted[:, 1], color="magenta", marker="*")  # linestyle=""

    # Give labels
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    plt.grid(True)

    spl = path.split('/')
    vid_name = spl[len(spl) - 4] + '/' + spl[len(spl) - 3] + '/' + spl[len(spl) - 2] + '/' + spl[len(spl) - 1]

    plt.title(vid_name)
    # plt.ylim([1, -80])
    # plt.xlim([-10, 70])
    plt.gca().invert_yaxis()  # origine asse z (y) in basso a sinistra
    name = epoch  # + type_name + 'fig_' + str(k)

    # if k < 10:
    #     name = epoch + type_name + 'fig_000' + str(k)
    # elif 10 <= k < 100:
    #     name = epoch + type_name + 'fig_00' + str(k)
    # elif 100 <= k < 1000:
    #     name = epoch + type_name + 'fig_0' + str(k)

    experiment.log_figure(figure_name=name, figure=plt, step=l)
    plt.figure().clear()
    # plt.show()


def main():
    parser = argparse.ArgumentParser(description="Plots the real and predicted trajectories using the csv file")

    parser.add_argument("--csv_path", dest="path", default=None, help="Path of the csv file")
    args = parser.parse_args()
    plot_traj(csv_path=args.path)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
