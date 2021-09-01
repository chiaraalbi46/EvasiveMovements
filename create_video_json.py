'''
Recupero delle coordinate e dell'angolo di rotazione della camera per ogni frame e creazione del file json
associato al video in esame con queste informazioni.
'''

import sys
import pyzed.sl as sl
import json
import os
import argparse
import platform


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def create_video_json(video_path, dest_folder, step):
    # Set configuration parameters
    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,  # Use HD720 video mode (default fps: 60)
                                    coordinate_units=sl.UNIT.METER,
                                    coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)

    print("Using SVO file: {0}".format(video_path))
    init_params.set_from_svo_file(video_path)
    spl = video_path.split(os.sep)  # '/'
    vid_name = spl[len(spl) - 1]
    spl1 = vid_name.split('.')
    vname = spl1[0]
    print(vname)
    final_name = vname + '.json'

    if platform.system() is 'Windows' and '\\' in dest_folder:
        dest_folder = dest_folder.replace('\\', '/')
        print("dest folder traformato: ", dest_folder)

    json_path = dest_folder + final_name  # slash
    print(json_path)
    images_path = dest_folder + 'left_frames/'
    if not os.path.exists(images_path):
        print("Creo la cartella left frames")
        os.mkdir(images_path)

    # Create a ZED camera object
    zed = sl.Camera()

    # Initialize images
    image = sl.Mat()
    # image_r = sl.Mat()

    # Open the camera
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS:
        print(repr(status))
        exit()

    # Enable positional tracking with default parameters
    tracking_params = sl.PositionalTrackingParameters()
    zed.enable_positional_tracking(tracking_params)

    camera_pose = sl.Pose()  # zed_pose
    runtime = sl.RuntimeParameters()

    # camera_info = zed.get_camera_information()

    py_translation = sl.Translation()

    nf = zed.get_svo_number_of_frames()
    print(nf)
    i = 0
    array_json = []
    while i < nf:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:  # frame

            # tracking_state = zed.get_position(camera_pose)
            tracking_state = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:

                print("FRAME: ", i)

                if i % int(step) == 0:
                    # Rotation
                    eul = camera_pose.get_euler_angles()

                    # Display the translation and timestamp
                    translation = py_translation
                    tx = round(camera_pose.get_translation(translation).get()[0], 3)
                    ty = round(camera_pose.get_translation(translation).get()[1], 3)
                    tz = round(camera_pose.get_translation(translation).get()[2], 3)
                    print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz,
                                                                                           camera_pose.timestamp.get_seconds()))

                    if tx == -0.0:
                        tx = 0.0
                    if ty == -0.0:
                        ty = 0.0
                    if tz == -0.0:
                        tz = 0.0
                    if eul[1] == -0.0:
                        eul[1] = 0.0

                    dict_frame = {'Frame': i, 'cords': [tx, ty, tz], 'angle': eul[1]}
                    array_json.append(dict_frame)

                    # Salvo il left frame
                    zed.retrieve_image(image, sl.VIEW.LEFT)
                    image_name = 'frame' + str(i)
                    if i < 10:
                        image_name = 'frame000' + str(i)
                    elif 10 <= i < 100:
                        image_name = 'frame00' + str(i)
                    elif 100 <= i < 1000:
                        image_name = 'frame0' + str(i)

                    print("Writing image: ", image_name)
                    im = os.path.join(images_path, image_name + '.png')
                    # print(os.path.join(images_path, image_name))

                    if not os.path.exists(im):
                        image.write(im)
                    else:
                        print("NON RICREO")

            i += 1

    if not os.path.isfile(json_path):
        write_json(array_json, json_path)  # lo creo
        # write_json({'X_array': x_array, 'Z_array': z_array, 'Y_rot': y_rot}, name)  # lo creo

    else:
        print("Il file : ", json_path, " è già presente")
        val = input("Vuoi sovrascrivere? yes/no:")
        # print(val)
        if val == 'yes' or val == 'Y' or val == 'y':
            os.remove(json_path)
            write_json(array_json, json_path)  # lo creo

    # Disable positional tracking and close the camera
    zed.disable_positional_tracking()
    zed.close()


def folder_process(folder, dest_folder, step):
    # per adesso manterrei la scansione 'normal' e casi manovre... poi vediamo
    print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:
        print("Subdir: ", d)
        sub_dir = os.listdir(folder + d)
        dest_path = dest_folder + d
        # print("Dest path: ", dest_path)
        for s in sub_dir:
            # print('\t', s)
            svo_path = os.path.join(folder, d, s)
            # print("SVOpath: ", svo_path)
            if platform.system() == 'Windows' and '\\' in svo_path:
                svo_path = svo_path.replace('\\', '/')
            print("\t SVOpath: ", svo_path)
            create_video_json(svo_path, dest_folder, step)


def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video", dest="input", default=None, help="Path of the svo video")
    parser.add_argument("--dest", dest="dest", default=None,
                        help="Path to the destination folder for the video json file")
    parser.add_argument("--step", dest="step", default=10, help="Sampling rate")

    args = parser.parse_args()
    if os.path.isdir(args.input):
        # esecuzione su cartella (e sottocartelle)
        folder_process(folder=args.input, dest_folder=args.dest, step=args.step)
    else:
        # esecuzione singolo video
        create_video_json(video_path=args.input, dest_folder=args.dest, step=args.step)

    # ES1: python create_video_json.py --video 'D:\Dataset_Evasive_Movements\video\svo_cut\z_normal\video26.svo'
    # --dest 'C:\Users\chiar\PycharmProjects\EvasiveMovements\datasets\images_dataset\video26\'

    # ES2: python create_video_json.py --video 'D:\Dataset_Evasive_Movements\video\svo_cut\'
    # --dest 'C:\Users\chiar\PycharmProjects\EvasiveMovements\datasets\images_dataset\'


if __name__ == '__main__':
    main()
