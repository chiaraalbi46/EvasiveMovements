import numpy as np
import json
# from utils.read_csv import load_data_for_video
import os
import argparse
import math
import cv2
from matplotlib import pyplot as plt


# fx : Focal length in pixels along x axis.
# cx : Optical center along x axis, defined in pixels (usually close to width/2).

def get_coordinates(path_json):
    with open(path_json) as json_file:
        d = json.load(json_file)
        data = []
        frame_index = []

        for i in range(len(d)):
            data.append(d[i]['Future'])
            frame_index.append(d[i]['Frame'])
    return data, frame_index


def image_coordinates():  # video_path, path_calib_j, path_json):

    with open('C:/Users/ninad/Desktop/video_guida/video257.json') as json_file:
         d = json.load(json_file)
         xdata = []
         ydata = []
         zdata = []
         for i in range(len(d)):
             xdata.append(d[i]['cords'][0])
             ydata.append(d[i]['cords'][1])
             zdata.append(d[i]['cords'][2])

    # immagine path
    path = 'C:/Users/ninad/Desktop/video_guida/frame0010.png'

    # # Focal length of the left eye in pixels
    # focal = 675
    # #focal_m = 0.0212   # metri
    #
    # optical_x = 654
    # optical_y = 370
    #
    # # optical_x_m = (optical_x * focal_m) / focal
    # # optical_y_m = (optical_y * focal_m) / focal
    # # #
    # # K = np.array([[round(focal_m, 2), 0, round(optical_x_m, 2)],
    # #                [0, round(focal_m, 2), round(optical_y_m, 2)],
    # #               [0, 0, 1]])
    #
    # K = np.array([[round(focal, 2), 0, round(optical_x, 2), 0],
    #                              [0, round(focal, 2), round(optical_y, 2), 0],
    #                              [0, 0, 1, 0]])
    #
    #
    # vn = os.path.split(video_path)
    # video_name = vn[1].split('.')
    # video_name = video_name[0].split('_')[0]
    #

    # Matrice di proiezione
    P = np.array([[675,   0, 654,   0], [0, 675, 370,   0], [0,   0,   1,   0]])
    #P = np.array([[675, 0, 654, 0], [0, 675, 370,  -675], [0, 0, 1, 0]])

    array_image_c =  []
    for i in range(len(xdata)):  # cambia per ogni video
        new_point_pj = np.dot(P, [xdata[i], -1, zdata[i], 1])
        array_image_c.append(new_point_pj/new_point_pj[2])
    print('array', array_image_c)

    img = cv2.imread(path.strip(), -1)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    x, y = 660, 600  # (x, y) coordinate punto corrente
    cv2.circle(img, (x, y), 6, (0, 255, 0), 4)
    width = 1280
    for i in array_image_c:
        x = int(i[0])
        y = int(i[1])
        #img[y - 1:y + 1, x - 1:x + 1] = [0, 0, 255]
        cv2.circle(img, (x, y), 6, (0, 0, 255), 4)
        print('x', x, 'y', y)

        # if (j < (len(array_image_c) - 1)):
        #             next_x = math.ceil(array_image_c[j + 1][0])
        #             next_y = math.ceil(array_image_c[j + 1][1])
        #             cv2.line(img, (x, y), (next_x, next_y), (0, 0, 255), 2)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    # Save image
    #cv2.imwrite("result.png", img)

    ax = plt.axes()

    #plt.plot(np.array(future)[get_ind_m][:, 0], np.array(future)[get_ind_m][:, 1], color="magenta", marker=".")  # , linestyle="")
    plt.plot(np.array(array_image_c)[:, 0], np.array(array_image_c)[:, 1], color="green", marker=".")  # , linestyle="")

    ax.set_xlabel('x')
    ax.set_ylabel('z')
    #plt.ylim([0, -8])
    #plt.xlim([-4, 4])
    # plt.gca().invert_yaxis() # origine asse z (y) in basso a sinistra
    plt.show()
   #  #return array_image_c


# python trajectories_draw.py --json_path /home/aivdepth/datasets/images_dataset/normal/video29/
# def main():
#     parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")
#     parser.add_argument("--json_path", dest="json_p", default=None, help="Path of the json file of trajectory")
#     args = parser.parse_args()
#     image_coordinates(path_json=args.json_p)

if __name__ == "__main__":
    # main()
    image_coordinates()
