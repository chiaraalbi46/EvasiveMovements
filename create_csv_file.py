import csv
import json
import re
import os
import argparse
import sys

SCALE_PERCENT = 12.5
K = float(SCALE_PERCENT / 100)
offset = 60
b = True
ext = '.jpg'

CSV_DATASET_PATH = os.path.join('datasets', 'csv_dataset')


def create_csv(seq_path, depth, data_type, len_seq):
    dir_name = os.path.dirname(os.path.abspath('__file__'))

    if depth == 'True':

        save_dir = os.path.join(dir_name, CSV_DATASET_PATH, 'depth', data_type)
        save_path = os.path.join(save_dir, data_type + '_' + str(
            len_seq) + '_sequence_d.csv')

    elif depth == 'False':

        save_dir = os.path.join(dir_name, CSV_DATASET_PATH, 'no_depth', data_type)
        save_path = os.path.join(save_dir, data_type + '_' + str(
            len_seq) + '_sequence.csv')
    else:

        print('Choose if --depth is True or False')
        exit()

    with open(save_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        for seq in os.listdir(seq_path):
            path = seq_path + seq + '/'  # path to i-th sequence
            data = json.load(open(path + "trajectories.json"))
            for frame in data.keys():

                cord = []
                if len(data[frame]["object_0"]["future"]) >= len_seq:  # number of predictions >= len_seq
                    for k in range(0, len_seq):
                        cord.append(data[frame]["object_0"]["future"][k])

                    string = frame.split("_")
                    result = re.match('\d+', string[1])

                    # number = (int(result.group()) + 1)
                    number = int(result.group())
                    n = str(number)
                    spl = path.split('/')
                    name = spl[len(spl) - 2] + "frame" + n + ext

                    if depth == 'True':
                        img_path = os.path.join(path, "frames/", name)
                        depth_path = os.path.join(path, "depth_frames/", name)

                        if os.path.exists(img_path) and os.path.exists(depth_path):
                            lines = [path, img_path, depth_path, cord]
                            filewriter.writerow(lines)
                    else:

                        img_path = os.path.join(path, "frames/", name)
                        # print("Frame: ", img_path)

                        if os.path.exists(img_path):
                            lines = [path, img_path, cord]  # rivedere se serve path
                            filewriter.writerow(lines)
                            # print("Si frame")
                        # else:
                            # print("No frame")


def main():
    parser = argparse.ArgumentParser(description="Create the CSV file from video sequences")
    parser.add_argument("--input_path", dest="input", default=None, help="Path of the folder with video sequences")
    parser.add_argument("--depth", dest="depth", default='False', help="Choose if use depth or not")
    parser.add_argument("--type", dest="data_type", default=None, help="Choose the dataset: train, validation, test")
    parser.add_argument("--len_seq", dest="len_seq", default=None, help="Define the number of predicted coords to consider")

    args = parser.parse_args()

    create_csv(seq_path=args.input, depth=args.depth, data_type=args.data_type, len_seq=int(args.len_seq))


if __name__ == '__main__':
    main()