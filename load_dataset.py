# Load dataset versione singleframe

import pandas as pd
import os
import numpy as np
import cv2
import platform
import argparse
import json


# IMAGE_HEIGHT = 720
# IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 90
IMAGE_WIDTH = 160
IMAGE_CHANNELS = 3


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_data_singleframe(csv_path, len_sequence):

    data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["video_dir", "path_frame", "past_point", "future_point"])

    video_dir = data_df['video_dir'].values
    path_frame = data_df['path_frame'].values
    data_dimension = len(path_frame)
    print(data_dimension)

    images_c = np.zeros([data_dimension, IMAGE_HEIGHT, IMAGE_WIDTH, IMAGE_CHANNELS])
    tensor_list = np.zeros([data_dimension, len_sequence, 2])

    # per understanding.py
    # path_frame[0] = 'C:/Users/chiar/Desktop/frame0090.png'
    # images_c[0] = load_image(image_file=path_frame[0])
    # print("DATAAAAA: ", data_df["future_point"][0])
    # tensor_list[0] = convert_to_vector(string=data_df["future_point"][0])

    for i in range(data_dimension):
        if os.path.exists(path_frame[i]):
            images_c[i] = load_image(image_file=path_frame[i])
            tensor_list[i] = convert_to_vector(string=data_df["future_point"][i])


    # da  [batch_size, depth, height, width, channels] in [batch_size, channels, depth, height, width] per nn.Conv2
    images_c = np.moveaxis(images_c, -1, 1)

    # TODO: poi fare anche per i punti del passato
    # TODO: capire
    #         train_images = np.moveaxis(imm_train, -1, 1)
    #         valid_images = np.moveaxis(imm_valid, -1, 1)
    return images_c, tensor_list, path_frame


def load_image(image_file):
    print("Image file: ", image_file)
    img = cv2.imread(image_file)
    # img = cv2.imread(image_file.strip(), -1)

    # height = img.shape[0]
    # width = img.shape[1]
    # img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)  # bo

    return img


def convert_to_vector(string):  # video ?
    tmp = list(string)
    i = 0
    final = []

    while i != len(tmp):
        if tmp[i] == '[':
            pair = []
            number = ' '
            while tmp[i] != ']':
                if tmp[i] == '[' or tmp[i] == ' ':
                    i += 1
                elif tmp[i] == ',':

                    n = float(number)
                    # if video:
                    #     n = float(number)
                    # else:
                    #     n = int(number)

                    number = ' '
                    pair.append(n)
                    i += 1
                else:
                    number += tmp[i]
                    i += 1
            if number != ' ':
                pair.append(float(number))
                # if video:
                #     pair.append(float(number))
                # else:
                #     pair.append(int(number))

                final.append(pair)
        i += 1

    final = np.asarray(final)

    return final


if __name__ == '__main__':
    # csv_path = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/csv_dataset/train
    # /train_config2_10_sequence.csv' load_data_singleframe(csv_path, 9)
    parser = argparse.ArgumentParser(description="Load dataset from csv file.")

    parser.add_argument("--csv", dest="input",
                        default='C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/csv_dataset/train'
                                '/train_config2_10_sequence.csv',
                        help="Path to the csv file")
    parser.add_argument("--len", dest="len", default=10, help="Lenght of future vector")
    # non potrebbe prenderlo dal nome del file csv ??
    args = parser.parse_args()

    load_data_singleframe(csv_path=args.input, len_sequence=args.len)



