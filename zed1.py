'''
Simile a zed.py, ma senza la parte di OpenGL.
C'è la possibilità di selezionare ogni quanto prendere i frames (campionamento)-
Una parte serve per la creazione dei file .json per le 'traiettorie' (va migliorata - inserendo una corrispondenza precisa tra frame e coordinate
--> poi su questi dati dobbiamo lavorare per creare i veri file di traiettorie (con past, present, future, origine che si aggiorna etc)
'''

import sys
import pyzed.sl as sl
import time
from datetime import datetime
import json
import os
import csv


# print(datetime.fromtimestamp(1485714600).strftime("%Y-%m-%d %I:%M:%S"))
# print(datetime.fromtimestamp(1550647550031).strftime('%Y-%m-%d %H:%M:%S:%Z'))


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":

    # Set configuration parameters
    init_params = sl.InitParameters(camera_resolution=sl.RESOLUTION.HD720,  # Use HD720 video mode (default fps: 60)
                                    coordinate_units=sl.UNIT.METER,
                                    coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP)

    # print(sys.argv)
    name = ''
    if len(sys.argv) >= 2:
        filepath = sys.argv[1]
        spl = filepath.split('/')
        vid_name = spl[len(spl) - 1]
        spl1 = vid_name.split('.')
        vname = spl1[0]
        print(vname)
        print("Using SVO file: {0}".format(filepath))
        init_params.set_from_svo_file(filepath)
        if len(sys.argv) == 3:  # quando voglio creare il json per le traiettorie passo come ultimo parametro il path alla cartella in cui voglio salvare il file
            pathToJson = sys.argv[2]
            name = pathToJson + vname + '.json'
            print("NAME: ", name)

    else:
        print("svo no read")

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

    camera_info = zed.get_camera_information()

    py_translation = sl.Translation()
    pose_data = sl.Transform()

    text_translation = ""
    text_rotation = ""

    nf = zed.get_svo_number_of_frames()
    print(nf)
    x_array = []
    z_array = []

    step = 100  # campionamento frames
    i = 0
    while i < 125:
        if zed.grab(runtime) == sl.ERROR_CODE.SUCCESS:  # frame

            # tracking_state = zed.get_position(camera_pose)
            tracking_state = zed.get_position(camera_pose, sl.REFERENCE_FRAME.WORLD)
            if tracking_state == sl.POSITIONAL_TRACKING_STATE.OK:

                print("FRAME: ", i)
                # Rotation
                rotation = camera_pose.get_rotation_vector()
                text_rotation = str((round(rotation[0], 2), round(rotation[1], 2), round(rotation[2], 2)))

                # Display the translation and timestamp
                # translation = sl.Translation()
                translation = py_translation
                tx = round(camera_pose.get_translation(translation).get()[0], 3)
                ty = round(camera_pose.get_translation(translation).get()[1], 3)
                tz = round(camera_pose.get_translation(translation).get()[2], 3)
                text_translation = str(
                    (round(translation.get()[0], 2), round(translation.get()[1], 2), round(translation.get()[2], 2)))
                print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz, camera_pose.timestamp.get_seconds()))
                x_array.append(tx)
                z_array.append(tz)

                if i % step == 0:
                    # salvo le coordinate x, z
                    # print("SALVO FRAME: ", i)
                    # mat_rot = camera_pose.get_rotation_matrix()
                    # print("Rot: ", mat_rot)

                    # x_array.append(tx)
                    # z_array.append(tz)
                    # print(datetime.fromtimestamp(camera_pose.timestamp.get_seconds()).strftime("%Y-%m-%d %I:%M:%S"))
                    # print("Text rotation: ", text_rotation)
                    # print("Translation: Tx: {0}, Ty: {1}, Tz {2}, Timestamp: {3}\n".format(tx, ty, tz,
                                                                                            # camera_pose.timestamp.get_seconds()))

                    # Display orientation quaternion
                    py_orientation = sl.Orientation()
                    ox = round(camera_pose.get_orientation(py_orientation).get()[0], 3)
                    oy = round(camera_pose.get_orientation(py_orientation).get()[1], 3)
                    oz = round(camera_pose.get_orientation(py_orientation).get()[2], 3)
                    ow = round(camera_pose.get_orientation(py_orientation).get()[3], 3)
                    # print("Orientation: ox: {0}, oy:  {1}, oz: {2}, ow: {3}\n".format(ox, oy, oz, ow))


                # print(type(camera_pose.timestamp.get_milliseconds()))
                # # print(camera_pose.timestamp.get_milliseconds())
                # var = camera_pose.timestamp.get_milliseconds()

            i += 1

    # JSON
    # name = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/prove_json/' + vname + '.json'

    if name:  # se name non è stringa vuota
        if not os.path.isfile(name):
            write_json({'X_array': x_array, 'Z_array': z_array}, name)  # lo creo
        else:
            print("Il file : ", name, " è già presente")

    # Disable positional tracking and close the camera
    zed.disable_positional_tracking()
    zed.close()
