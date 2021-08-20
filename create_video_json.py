'''
Recupero delle coordinate e dell'angolo di rotazione della camera per ogni frame e creazione del file json
associato al video in esame con queste informazioni.
'''

import sys
import pyzed.sl as sl
import json
import os
import argparse


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def create_video_json(video_path, dest_folder):

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
    json_path = dest_folder + final_name  # devo avere messo lo slah in pathToTrajDir !
    print(json_path)

    # Create a ZED camera object
    zed = sl.Camera()

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
                # Rotation
                eul = camera_pose.get_euler_angles(False)

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
                # print('dict', dict_frame)
                array_json.append(dict_frame)
                # print('array_j', array_json)

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


def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video_path", dest="input", default=None, help="Path of the svo video")
    parser.add_argument("--dest_folder", dest="dest", default=None,
                        help="Path to the destination folder for the video json file")

    args = parser.parse_args()

    create_video_json(video_path=args.input, dest_folder=args.dest)


if __name__ == '__main__':
    main()

