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

    with open('C:/Users/ninad/Desktop/video178.json') as json_file:
         d = json.load(json_file)
         xdata = []
         ydata = []
         zdata = []
         for i in range(len(d)):
             xdata.append(d[i]['cords'][0])
             ydata.append(d[i]['cords'][1])
             zdata.append(d[i]['cords'][2])

    data, frame_index = get_coordinates('C:/Users/ninad/Desktop/video_guida/194/video194_traj.json')
    m = []
    for i in range(len(data)):
        if frame_index[i] == 530:
            m.append(data[i])
    print(len(m))
    m = np.array(m)

    # with open('C:/Users/ninad/Desktop/video_guida/json/video29_TR.json') as json_file:
    #      d = json.load(json_file)
    #      xdata_tr = []
    #      ydata_tr  = []
    #      zdata_tr  = []
    #      for i in range(len(d)):
    #          xdata_tr .append(d[i]['cords'][0])
    #          ydata_tr .append(d[i]['cords'][1])
    #          zdata_tr .append(d[i]['cords'][2])

    # immagine path
    path = 'C:/Users/ninad/Desktop/video_guida/194/frame0530.png'

    # # Focal length of the left eye in pixels
    focal = 675
    # #focal_m = 0.0212   # metri
    #
    optical_x = 654
    optical_y = 450
    #
    # # optical_x_m = (optical_x * focal_m) / focal
    # # optical_y_m = (optical_y * focal_m) / focal
    # # #
    # # K = np.array([[round(focal_m, 2), 0, round(optical_x_m, 2)],
    # #                [0, round(focal_m, 2), round(optical_y_m, 2)],
    # #               [0, 0, 1]])
    #
    K = np.array([[-round(focal, 2), 0, round(optical_x, 2)],
                                  [0, round(focal, 2), round(optical_y, 2)],
                                  [0, 0, 1]])

    t = np.array([0, 0 ,0])
    #R = np.identity(3)

    R = np.array([[1, 0, 0], [0, 0, 0], [0, 0, 1]])

    world2cam = np.hstack((R, np.dot(-R, t).reshape(3, -1)))
    P = np.dot(K, world2cam)
    #
    #
    # vn = os.path.split(video_path)
    # video_name = vn[1].split('.')
    # video_name = video_name[0].split('_')[0]
    #

    # Matrice di proiezione
    # P = np.array([[675,   0, 654,   0], [0, 675, 370,   0], [0,   0,   1,   0]])
    #P = np.array([[675, 0, 654, 0], [0, 675, 370,  -675], [0, 0, 1, 0]])

    array_image_c =  []
   # array_image_c_TR = []
    for i in range(len(m[0])):  # cambia per ogni video
        #new_point_pj = np.dot(P, [xdata[i], -1, zdata[i], 1])
        new_point_pj = np.dot(P, [m[0][i][0], -1, m[0][i][1], 1])
        array_image_c.append(new_point_pj/new_point_pj[2])
        # new_point_pj_TR = np.dot(P, [xdata_tr[i], -1, zdata_tr[i], 1])
        # array_image_c_TR.append(new_point_pj_TR / new_point_pj_TR[2])

    print('array', array_image_c)

    img = cv2.imread(path.strip(), -1)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    width = 1280
    higth = 720

    for i in range(len(array_image_c)):
        x = int(array_image_c[i][0])
        y = int(array_image_c[i][1])
        #img[y - 1:y + 1, x - 1:x + 1] = [0, 0, 255]
        print('x', x, 'y', y)
        cv2.circle(img, (x, y), 3, (0, 0, 255), 4)

        # x_TR = int(array_image_c_TR[i][0])
        # y_TR = int(array_image_c_TR[i][1])
        # # img[y - 1:y + 1, x - 1:x + 1] = [0, 0, 255]
        # cv2.circle(img, (x_TR, y_TR), 6, (0, 255, 0), 4)

        # print('x', x_TR, 'y', y_TR)

        if (i < (len(array_image_c) - 1)):
                    next_x = math.ceil(array_image_c[i+1][0])
                    next_y = math.ceil(array_image_c[i+1][1])
                    cv2.line(img, (x, y), (next_x, next_y), (0, 255, 0), 2)


   # cv2.circle(img, (1391, 664), 3, (0, 255, 0), 4)
    #cv2.circle(img, (819, 477), 3, (255, 0, 0), 4)




   # cv2.circle(img, (675, 715), 10, (255, 0, 0), 4)
    cv2.imshow('img', img)
    cv2.waitKey(0)

    print('xdata', xdata)
    print('zdata', zdata)

    # Save image
    #cv2.imwrite("result.png", img)

    ax = plt.axes()
    #plt.plot(np.array(m[0][:, 0]), np.array(m[0][:,1]), color="magenta", marker=".")  # , linestyle="")

    #plt.plot(np.array(future)[get_ind_m][:, 0], np.array(future)[get_ind_m][:, 1], color="magenta", marker=".")  # , linestyle="")
  #  plt.plot(np.array(array_image_c)[:, 0], np.array(array_image_c)[:, 1], color="green", marker=".")  # , linestyle="")
   # plt.plot(np.array(array_image_c_TR)[:, 0], np.array(array_image_c_TR)[:, 1], color="magenta", marker=".")  # , linestyle="")

    ax.set_xlabel('x')
    ax.set_ylabel('z')
    #plt.ylim([0, 2500])
   # plt.xlim([0, 2500])
    #plt.gca().invert_xaxis() # origine asse z (y) in basso a sinistra
    plt.gca().invert_yaxis()
   # plt.show()
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
