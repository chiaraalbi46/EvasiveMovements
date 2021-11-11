import numpy as np
import pandas as pd
import json
# from utils.read_csv import load_data_for_video
import os
import argparse
import math
import cv2
from matplotlib import pyplot as plt
from create_csv_file import right_slash
from load_dataset import convert_to_vector


# fx : Focal length in pixels along x axis.
# cx : Optical center along x axis, defined in pixels (usually close to width/2).

# C:\Users\ninad\Desktop\video_guida\summarize_test.csv
def get_coordinates(csv_path):
    csv_path = right_slash(csv_path)
    data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["image_path", "predicted", "real"])

    predicted = []
    real = []
    path = []
    for k in range(len(data_df['predicted'].values)):
        predicted.append(convert_to_vector(data_df['predicted'].values[k]))
        real.append(convert_to_vector(data_df['real'].values[k]))
        #new_path = start_path + '/'.join(data_df['image_path'][k].split('/')[5:])
        if 'flip' in data_df['image_path'][k]:
            #   print('path', val_path)
            new_path = data_df['image_path'][k].replace("left_frames_flip_processed", "left_frames_flip")
        else:
            new_path = data_df['image_path'][k]
        path.append(new_path)

    return predicted, real, path


def get_data_proj(data):
    # # Focal length of the left eye in pixels
    focal = 675
    optical_x = 654
    optical_y = 370
    K = np.array([[round(focal, 2), 0, round(optical_x, 2)],
                  [0, round(focal, 2), round(optical_y, 2)],
                  [0, 0, 1]])

    t = np.array([0, 0, 0])
    R = np.identity(3)

    world2cam = np.hstack((R, np.dot(-R, t).reshape(3, -1)))
    P = np.dot(K, world2cam)

    data_proj = []
    for i in range(len(data)):  # cambia per ogni video
        tmp = []
        for j in data[i]:
            # print(j)
            new_point_pj = np.dot(P, [-j[0], -1, j[1], 1])
            tmp.append(new_point_pj / (new_point_pj[2]))
        data_proj.append(tmp)
    return data_proj


def get_data_proj_2(data):
    # arr_y = []

    # arr_y.append(- np.ones((1, len(i['Future'])))[0])

    f = 675
    cx = 654  # 334.25
    cy = 370  # 186.25

    width = cx * 2
    height = cy * 2

    p_width = 1280  # 2560
    p_height = 720

    data_proj = []

    for j in range(len(data)):
        tmp = []
        for i in range(len(data[j])):
            canvas_x = ((data[j][i][0] * f) / - data[j][i][1])
            # canvas_y = ((data[j][i][1] * f) / - data[j][i])
            canvas_y = ((-1 * f) / - data[j][i][1])

            # NDC system
            ndc_x = (canvas_x + cx) / width
            ndc_y = (canvas_y + cy) / height

            # Raster space
            raster_x = math.floor(ndc_x * p_width)
            raster_y = math.floor((1 - ndc_y) * p_height)

            tmp.append([raster_x, raster_y])

        data_proj.append(tmp)
    return data_proj


def image_coordinates(csv_path, p_result):  # video_path, path_calib_j, path_json):
    # video_path = 'C:/Users/ninad/Desktop/video_guida/194/video194.avi'

    # start_path = 'C:/Users/ninad/Desktop/frame_dataset/'
    # csv_path = 'C:/Users/ninad/Desktop/video_guida/summarize_test.csv '

    predicted, real, path = get_coordinates(csv_path)

    pred_proj = get_data_proj_2(predicted)
    real_proj = get_data_proj_2(real)
    print('real: ', real_proj)

    # pred_proj = get_data_proj(predicted)
    # real_proj = get_data_proj(real)

    # #
    # vn = (path[0]).split('/')
    # vn = vn[len(vn) - 3]
    video_img = []
    size = (0, 0)

    for j in range(len(real_proj)):
        path_frame = path[j]
        print('Path_frame: ', path_frame)
        if os.path.exists(path_frame):

            img = cv2.imread(path_frame.strip(), -1)
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            height, width, _ = img.shape
            size = (width, height)

            for i in range(len(real_proj[j])):
                x_real = int(real_proj[j][i][0])
                y_real = int(real_proj[j][i][1])

                x_pred = int(pred_proj[j][i][0])
                y_pred = int(pred_proj[j][i][1])

                # print('x', x, 'y', y)
                if (i % 10) == 0:   # prendo ogni 10 frame 
                    cv2.circle(img, (x_real, y_real), 3, (0, 0, 255), 4)

                if i < 10:  # prendo i primi 10 punti
                    cv2.circle(img, (x_pred, y_pred), 3, (0, 255, 0), 4)

                if (i < (len(real_proj[j]) - 1)):
                    next_x_real = math.ceil(real_proj[j][i + 1][0])
                    next_y_real = math.ceil(real_proj[j][i + 1][1])
                    if (i % 10) == 0:
                       cv2.line(img, (x_real, y_real), (next_x_real, next_y_real), (0, 0, 222), 2)

                    next_x_pred = math.ceil(pred_proj[j][i + 1][0])
                    next_y_pred = math.ceil(pred_proj[j][i + 1][1])
                    if i < 10:
                       cv2.line(img, (x_pred, y_pred), (next_x_pred, next_y_pred), (0, 222, 0), 2)
            ap = path_frame.split('/')
            name_frame = ap[len(ap) - 1]
            path_result = p_result + '/' + ap[len(ap) - 3] + '/'

            #path_result = '/'.join(ap[:len(ap) - 5]) + '/result/' + ap[len(ap) - 3] + '/'
            print(path_result)
            if not os.path.exists(path_result):
                os.makedirs(path_result)
            # print(path_result)
            name = path_result + name_frame

                #cv2.imwrite(name, img)
               # video_img.append(img)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, 'Ground Truth', (100, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.putText(img, 'Predicted', (100, 150), font, 1, (0, 258, 0), 2, cv2.LINE_AA)

            cv2.imwrite(name, img)


#                 video_img.append(img)
#
# #
#
    # writer = cv2.VideoWriter('video_name.avi', cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
    # for i in tqdm.tqdm(range(len(video_img))):
    #     writer.write(video_img[i])
    #     #print('o', video_img[i])
    # writer.release()
    print()
    print("Create video and store it in " + 'video_name')

#         cv2.imshow('img', img)
#         cv2.waitKey(0)

#
# def main():
#     parser = argparse.ArgumentParser(description="Create the trajectories' file from a csv file of a video sequence")
#     parser.add_argument("--csv_path", dest="csv_p", default=None, help="Path of the csv file of trajectory")
#     parser.add_argument("--start_path", dest="start_p", default=None, help="Initial path, where the dataset is located")
#     parser.add_argument("--result_p", dest="result_p", default=None, help="Initial path, where the dataset is located")
#
#     args = parser.parse_args()
#     image_coordinates(start_path=args.start_p, csv_path=args.csv_p, p_result=args.result_p)
#
# # plot_image.py --csv_path /andromeda/datasets/rc_car_maneuvers/aivdepth/test_results/single_frame/grafici/summarize_test.csv --result_p /andromeda/datasets/rc_car_maneuvers/video_finale/grafici/
# if __name__ == '__main__':
#     main()
if __name__ == "__main__":
    # #main()
    # start_path = 'C:/Users/ninad/Desktop/frame_dataset/'
    #finale_prova_reali\futuri_30
    csv_path = 'C:/Users/ninad/Desktop/finale_prova_reali/futuri_30/summarize_test.csv'
    path_result = 'C:/Users/ninad/Desktop/finale_prova_reali/futuri_30/'
    # #get_coordinates(start_path, csv_path)
    image_coordinates(csv_path, path_result)
