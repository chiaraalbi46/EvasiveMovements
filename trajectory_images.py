import argparse
import pandas as pd
from load_dataset import convert_to_vector
import matplotlib.pyplot as plt
import numpy as np
from create_csv_file import right_slash
from comet_ml import Experiment
# import matplotlib as mpl
#
# mpl.use('Agg')
#C:\Users\ninad\Desktop\video_guida\csv\summarize_test.csv
#C:\Users\ninad\Desktop\datasets\images_dataset\normal\video88\left_frames_processed
#/home/aivdepth/datasets/images_dataset/normal/video88/left_frames/frame0290.png
#row_csv = 447 -1 #(?)


#>python trajectory_images.py --row_csv 447 --csv_path C:\Users\ninad\Desktop\video_guida\csv\summarize_test.csv

def plot_traj(row_csv, csv_path):
    csv_path = right_slash(csv_path)
    # csv_path = 'summarize_test.csv'
#    csv_path = 'C:/Users/ninad/Desktop/video_guida/csv/summarize_test.csv'
    row_csv = int(row_csv) - 1  # parte da 0
    data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["image_path", "predicted", "real"])
    # print(data_df)

    predicted = []
    real = []
    for k in range(len(data_df['predicted'].values)):
        predicted.append(convert_to_vector(data_df['predicted'].values[k]))
        real.append(convert_to_vector(data_df['real'].values[k]))
    #print(predicted)
    spl = np.array(data_df['image_path'])[446].split('/')
    vid_name = spl[len(spl) - 4] + '/' + spl[len(spl) - 3] + '/' + spl[len(spl) - 2] + '/' + spl[len(spl) - 1]

    plt.title(vid_name)
    # # #fig = plt.figure(figsize=(15, 15))
    ax = plt.axes()

    # print(real[i][j][0], real[i][j][1])
    plt.plot(real[row_csv][:, 0], real[row_csv][:, 1], color="green", marker=".") #, linestyle="")
    plt.plot(predicted[row_csv][:, 0], predicted[row_csv][:, 1], color="magenta", marker=".")#, linestyle="")  # linestyle=""

    # Give labels
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    plt.ylim([0, -8])
    plt.xlim([-4, 4])
    # plt.gca().invert_yaxis() # origine asse z (y) in basso a sinistra
    plt.show()


# def plot_data(real, predicted, experiment, k, l, path, epoch, type_name):  # plotta singole 'righe' csv (real, predicted)
def plot_data(real, predicted, experiment, k, l, path, it):
    fig = plt.figure()

    ax = plt.axes()

    # print("Real x: ", real[:, 0])
    # print("Real y: ", real[:, 1])

    zero = np.zeros((1, 2))  # zero è sempre l'origine del tratto
    r = np.concatenate((zero, real), axis=0)
    # p = np.concatenate((zero, predicted), axis=0)

    plt.plot(r[:, 0], r[:, 1], color="green", marker=".")
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

    # Per avere scala 'quadrata'
    y_end = np.min([np.min(predicted[:, 1]), np.min(real[:, 1])])  # max y (y è negativa)
    x_end = y_end / 2
    plt.xlim([x_end, - x_end])
    plt.ylim([0, y_end])

    plt.gca().invert_yaxis()  # origine asse z (y) in basso a sinistra
    # name = epoch  # + type_name + 'fig_' + str(k)
    name = 'it_' + str(it) + '_fig_' + str(k)

    if k < 10:
        name = 'it_' + str(it) + '_fig_000' + str(k)
    elif 10 <= k < 100:
        name = 'it_' + str(it) + '_fig_00' + str(k)
    elif 100 <= k < 1000:
        name = 'it_' + str(it) + '_fig_0' + str(k)

    # if k < 10:
    #     name = epoch + type_name + 'fig_000' + str(k)
    # elif 10 <= k < 100:
    #     name = epoch + type_name + 'fig_00' + str(k)
    # elif 100 <= k < 1000:
    #     name = epoch + type_name + 'fig_0' + str(k)

    experiment.log_figure(figure_name=name, figure=plt, step=l)
    fig.clear()
    plt.close(fig)
    # plt.show()
#
#
def main():
    parser = argparse.ArgumentParser(description="Plots the real and predicted trajectories using the csv file")
    parser.add_argument("--row_csv", dest="row_csv", default=0, help="Select the line of the CSV file")
    parser.add_argument("--csv_path", dest="path", default=None, help="Path of the csv file")

    args = parser.parse_args()

    plot_traj(row_csv=args.row_csv, csv_path=args.path)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
