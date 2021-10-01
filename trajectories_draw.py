import cv2, os, math, tqdm
import pandas as pd
import numpy as np
import json
#from utils.read_csv import load_data_for_video
import pyzed.sl as sl
import argparse

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

def image_coordinates(path_json):
    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,  # Use HD720 video mode (default fps: 60)
                                    coordinate_units=sl.UNIT.METER,
                                    coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)
    # Create a ZED camera object
    zed = sl.Camera()
    camera_pose = sl.Pose()  # zed_pose

    cam_params = zed.get_camera_information().calibration_parameters

    # Open the camera
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()
    # Focal length of the left eye in pixels
    focal_x = cam_params.left_cam.fx
    focal_y = cam_params.left_cam.fy

    optical_x = cam_params.left_cam.fx
    optical_y = cam_params.left_cam.fy

    K = np.array([[focal_x,       0,  optical_x],
                  [      0, focal_y,  optical_y],
                  [      0,       0,         1]])

    #R = camera_pose.get_rotation_matrix(sl.Rotation()).r
    #t = camera_pose.get_translation(sl.Translation()).get()
    #world2cam = np.hstack((R, np.dot(-R, t).reshape(3,-1)))
    # todo usare file csv con dati predetti

    #path_frame = 'C:/Users/ninad/Desktop/video_guida/json/video29_traj.json'
    future, frame_ind = get_coordinates(path_json)
    # ora faccio solo su un frame : selezionare frame_path e coordinate

    trasf_cord = []
    for i in range(len(future)):
        if frame_ind[i] == 330:
            trasf_cord = future[i]


    array_image_c = []
    for i in range(len(trasf_cord)):
        P = np.dot(K, [trasf_cord[i][0], trasf_cord[i][1], 1] )
        array_image_c.append(P)
    print('array_image', array_image_c)

# def save_video(video_name, csv_path, len_seq, model_type):
#     data_df = pd.read_csv(csv_path, error_bad_lines=False, names=["image_path", "predicted", "real"])
#
#     image_path = data_df['image_path'].values
#     predicted, real = load_data_for_video(csv_path, len_seq)
#     video_img = []
#
#     for i in tqdm.tqdm(range(len(image_path))):
#
#         img = cv2.imread(image_path[i].strip(), -1)
#         img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
#         height, width, _ = img.shape
#         size = (width, height)
#
#         x, y = 600, 450  # (x, y) coordinate punto corrente
#         cv2.circle(img, (x, y), 3, (0, 255, 0), 1)
#
#         for j, item in enumerate(predicted[i]):
#             x = math.ceil(item[0])
#             y = math.ceil(item[1])
#             img[y - 1:y + 1, x - 1:x + 1] = [0, 0, 255]
#             if (j < (len(predicted[i]) - 1)):
#                 next_x = math.ceil(predicted[i][j + 1][0])
#                 next_y = math.ceil(predicted[i][j + 1][1])
#                 cv2.line(img, (x, y), (next_x, next_y), (0, 0, 255), 2)
#
#         for j, item in enumerate(real[i]):
#             x = int(item[0])
#             y = int(item[1])
#             img[y - 1:y + 1, x - 1:x + 1] = [255, 255, 255]
#             if (j < (len(real[i]) - 1)):
#                 next_x = int(real[i][j + 1][0])
#                 next_y = int(real[i][j + 1][1])
#                 cv2.line(img, (x, y), (next_x, next_y), (255, 255, 255), 2)
#
#         font = cv2.FONT_HERSHEY_SIMPLEX
#         cv2.putText(img, 'CNN+LSTM', (100, 100), font, 1, (0, 0, 255), 2, cv2.LINE_AA)
#         cv2.putText(img, 'Ground Truth', (100, 150), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
#         cv2.putText(img, 'Starting Point', (100, 200), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
#
#         video_img.append(img)
#
#     writer = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
#     for i in tqdm.tqdm(range(len(video_img))):
#         writer.write(video_img[i])
#     writer.release()
#     print()
#     print("Create video and store it in " + video_name)

#/home/aivdepth/datasets/images_dataset/normal/video29/left_frames_processed
def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")
    parser.add_argument("--json_path", dest="json_p", default=None, help="Path of the json file of trajectory")
    args = parser.parse_args()
    image_coordinates(path_json=args.json_p)

if __name__ == "__main__":
    main()