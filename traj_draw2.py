import tqdm
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

        # for i in range(len(d)):
        #     data.append(d[i]['Future'])
        #     frame_index.append(d[i]['Frame'])
    return d #data, frame_index


def get_path_frame(frame_index):
    path = ''

    if frame_index < 100:
        path = 'frame00' + str(frame_index)
    elif 100 <= frame_index < 1000:
        path = 'frame0' + str(frame_index)
    # elif 1000 <= k < 10000:
    #     path = 'frame' + str(k)

    return path
def image_coordinates():  # video_path, path_calib_j, path_json):
    video_path = 'C:/Users/ninad/Desktop/video_guida/194/video194.avi'
    path = 'C:/Users/ninad/Desktop/video_guida/194/left_frames/'
    # with open('C:/Users/ninad/Desktop/video178.json') as json_file:
    #     d = json.load(json_file)
    #     xdata = []
    #     ydata = []
    #     zdata = []
    #     for i in range(len(d)):
    #         xdata.append(d[i]['cords'][0])
    #         ydata.append(d[i]['cords'][1])
    #         zdata.append(d[i]['cords'][2])
    d = get_coordinates('C:/Users/ninad/Desktop/video_guida/194/video194_traj.json')

    #data, frame_index = get_coordinates('C:/Users/ninad/Desktop/video_guida/194/video194_traj.json')
#todo ciclo frame

    #
    # # Focal length of the left eye in pixels
    focal = 675
    # #focal_m = 0.0212   # metri
    #
    optical_x = 654
    optical_y = 370
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

    t = np.array([0, 0, 0])
    R = np.identity(3)

    world2cam = np.hstack((R, np.dot(-R, t).reshape(3, -1)))
    P = np.dot(K, world2cam)
    #
    #
    vn = os.path.split(video_path)
    video_name = vn[1].split('.')
    video_name = video_name[0].split('_')[0]

    # Matrice di proiezione
    # P = np.array([[675,   0, 654,   0], [0, 675, 370,   0], [0,   0,   1,   0]])
    # P = np.array([[675, 0, 654, 0], [0, 675, 370,  -675], [0, 0, 1, 0]])

    array_image_c = []
    new_dict = {'Frame': 0, 'Data': []}
    # array_image_c_TR = []
    for i in range(len(d)):  # cambia per ogni video
        # new_point_pj = np.dot(P, [xdata[i], -1, zdata[i], 1])
        tmp = []
        for j in d[i]['Future']:
            new_point_pj = np.dot(P, [j[0], -0.8, j[1], 1])
            tmp.append(new_point_pj / new_point_pj[2])
        new_dict['Frame'] = d[i]['Frame']
        new_dict['Data'] = tmp

        array_image_c.append(new_dict)
        new_dict = {}

            # new_point_pj_TR = np.dot(P, [xdata_tr[i], -1, zdata_tr[i], 1])
            # array_image_c_TR.append(new_point_pj_TR / new_point_pj_TR[2])

#
    dirs = os.listdir(path)
    n = 0
    video_img = []
    size = (0, 0)
    path_result = 'C:/Users/ninad/Desktop/video_guida/result_194/'
    for d in dirs:
        if n < len(array_image_c):
            ind = array_image_c[n]['Frame']
            path_frame = get_path_frame(ind)
            if path_frame == d.split('.')[0] :
                path_image = path + d
                print(path_image)

                img = cv2.imread(path_image.strip(), -1)
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                x, y = 660, 600  # (x, y) coordinate punto corrente

                height, width, _ = img.shape
                size = (width, height)

                for i in range(len(array_image_c[n]['Data'])):
                    x = int(array_image_c[n]['Data'][i][0])
                    y = int(array_image_c[n]['Data'][i][1])
                    # img[y - 1:y + 1, x - 1:x + 1] = [0, 0, 255]
                    print('x', x, 'y', y)
                    cv2.circle(img, (x, y), 3, (0, 0, 255), 4)

                    if (i< (len(array_image_c[n]['Data']) - 1)):
                        next_x = math.ceil(array_image_c[n]['Data'][i + 1][0])
                        next_y = math.ceil(array_image_c[n]['Data'][i + 1][1])
                        cv2.line(img, (x, y), (next_x, next_y), (0, 255, 0), 2)
                name = path_result + 'result' + path_frame + '.png'
                cv2.imwrite(name, img)
                n += 1


#                 font = cv2.FONT_HERSHEY_SIMPLEX
#                 cv2.putText(img, 'CNN+LSTM', (100, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
#                 cv2.putText(img, 'Ground Truth', (100, 150), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(img, 'Starting Point', (100, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
#
#                 video_img.append(img)
#
# #
#
#     writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
#     for i in tqdm.tqdm(range(len(video_img))):
#         writer.write(video_img[i])
#         print('o', video_img[i])
#     writer.release()
#     print()
#     print("Create video and store it in " + video_name)

#         cv2.imshow('img', img)
#         cv2.waitKey(0)
#     # Save image
#     # cv2.imwrite("result.png", img)
#
#     # ax = plt.axes()
#     # plt.plot(np.array(m[0][:, 0]), np.array(m[0][:, 1]), color="magenta", marker=".")  # , linestyle="")
#     #
#     # # plt.plot(np.array(future)[get_ind_m][:, 0], np.array(future)[get_ind_m][:, 1], color="magenta", marker=".")  # , linestyle="")
#     # #  plt.plot(np.array(array_image_c)[:, 0], np.array(array_image_c)[:, 1], color="green", marker=".")  # , linestyle="")
#     # # plt.plot(np.array(array_image_c_TR)[:, 0], np.array(array_image_c_TR)[:, 1], color="magenta", marker=".")  # , linestyle="")
#     #
#     # ax.set_xlabel('x')
#     # ax.set_ylabel('z')
#     # # plt.ylim([0, 2500])
#     # # plt.xlim([0, 2500])
#     # # plt.gca().invert_xaxis() # origine asse z (y) in basso a sinistra
#     # plt.gca().invert_yaxis()
#     # plt.show()
#
# #  #return array_image_c
#
# # python trajectories_draw.py --json_path /home/aivdepth/datasets/images_dataset/normal/video29/
# # def main():
# #     parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")
# #     parser.add_argument("--json_path", dest="json_p", default=None, help="Path of the json file of trajectory")
# #     args = parser.parse_args()
# #     image_coordinates(path_json=args.json_p)

if __name__ == "__main__":
    # main()
    image_coordinates()
