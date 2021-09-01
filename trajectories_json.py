import argparse
import json
import os
import numpy as np
import math


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# array origine
def origin_traj(i_start, xdata, zdata, angle, origin_distance):
    # Origini
    origin = []
    angle_o = []
    # i_start = 0 # posso cambiare il punto di partenza
    while i_start < len(xdata):
        origin.append([xdata[i_start], zdata[i_start]])
        angle_o.append(angle[i_start])
        i_start += origin_distance  # num_vectors
    return origin, angle_o


def create_traj_json(video_json_path, i_start, point_past, point_future, origin_distance, dest_folder):
    with open(video_json_path) as json_file:
        d = json.load(json_file)
        xdata = []
        zdata = []
        angle = []

        # # Controllo sul numero dei punti_future che ha l'ultimo origine
        # num_origin = int((len(d) / sample) / point_future)  # (per eccesso)
        # point_end = int((len(d) / sample) - (point_future * num_origin))  # punti ultima origine
        # point_add = point_future - point_end - 1  # punti che mancano nell'ultimo origine per arrivare a future
        # # -1 tolgo origine

        # step = 0
        for i in range(len(d)):
            # if i == step:
            xdata.append(d[i]['cords'][0])
            zdata.append(d[i]['cords'][2])
            angle.append(d[i]['angle'])
            #     step += sample
            # elif point_add > 0 and step == (i + 1):  # aggiungo il frame successivo a quello step = i
            #     xdata.append(d[i]['cords'][0])
            #     zdata.append(d[i]['cords'][2])  # dipende da quanti punti campiono
            #     angle.append(d[i]['angle'])
            #     point_add -= 1

        # angolo dei soli origini

    origin, angle_o = origin_traj(i_start, xdata, zdata, angle, origin_distance)  # crea origini

    # futuro, presente, passato
    future = []
    present = []
    past = []
    array = []
    dic_traj = {'Frame': [], 'Past': [], 'Present': [], 'Future': [], }

    f = 0
    for i in range(len(xdata) - 10):
        if xdata[i] == origin[f][0] and zdata[i] == origin[f][1] and f < len(origin) - 1 and i % origin_distance == 0:

            present.append(origin[f])
            # print('i', i , 'data', xdata[i], zdata[i], 'origin',  origin[f] )

            # Punti futuri
            count_future = 1
            while count_future < point_future:
                # Rotazione        #angolo in radianti
                x_rot = (xdata[i + count_future] - origin[f][0]) * math.cos(angle_o[f]) - (
                        zdata[i + count_future] - origin[f][1]) * math.sin(angle_o[f])
                y_rot = (xdata[i + count_future] - origin[f][0]) * math.sin(angle_o[f]) + (
                        zdata[i + count_future] - origin[f][1]) * math.cos(angle_o[f])

                # traslazione
                x_rot_t = x_rot + origin[f][0]
                y_rot_t = y_rot + origin[f][1]
                new_point = [x_rot_t, y_rot_t]
                new_point[0] = round(x_rot_t, 3)
                new_point[1] = round(y_rot_t, 3)
                future.append(new_point)
                count_future += 1
            # print('Futrue', future)

            # Punti passati
            count = point_past  # numero punti del passato
            while i - count > 0 and count > 0:
                # Rotazione
                x_rot = (xdata[i - count] - origin[f][0]) * math.cos(angle_o[f]) - (
                        zdata[i - count] - origin[f][1]) * math.sin(angle_o[f])
                y_rot = (xdata[i - count] - origin[f][0]) * math.sin(angle_o[f]) + (
                        zdata[i - count] - origin[f][1]) * math.cos(angle_o[f])

                # Traslazione
                x_rot_t = x_rot + origin[f][0]
                y_rot_t = y_rot + origin[f][1]
                new_point = [x_rot_t, y_rot_t]
                new_point[0] = round(x_rot_t, 2)
                new_point[1] = round(y_rot_t, 2)
                past.append(new_point)
                count -= 1

            if len(past) == point_past and len(future) == point_future - 1:  # se hanno meno punti non salvo
                dic_traj['Frame'] = i  # indice dell'origine
                dic_traj['Past'] = past
                dic_traj['Present'] = present
                dic_traj['Future'] = future
                array.append(dic_traj)

            dic_traj = {}
            future = []
            present = []
            past = []
            f += 1

        spl = video_json_path.split(os.sep)  # '/'
        vid_name = spl[len(spl) - 1]
        spl1 = vid_name.split('.')
        vname = spl1[0]
        # print(vname)
        final_name = vname + '_traj.json'
        pathToTrajFile = dest_folder + final_name  # devo avere messo lo slah in pathToTrajDir !
        # #print(pathToTrajFile)
        # pathToTrajFile = 'C:/Users/ninad/Desktop/video_guida/json/video.json'
        write_json(array, pathToTrajFile)


# video_json_path, i_start, point_past, point_future, origin_distance, dest_folder
def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video_json_path", dest="input", default=None, help="Path of the json file of a video")
    parser.add_argument("--i_start", dest="start", default=0, help="Initial system origin")
    parser.add_argument("--point_past", dest="past", default=None,
                        help="Number of past points to remap in the new reference system")
    parser.add_argument("--point_future", dest="future", default=None,
                        help="Number of future points to remap in the new reference system")
    parser.add_argument("--origin_distance", dest="origin_distance", default=10,
                        help="Distance between two successive origins")

    parser.add_argument("--dest_folder", dest="dest", default=None,
                        help="Path to the destination folder for the trajectories' file")

    args = parser.parse_args()

    create_traj_json(video_json_path=args.input, i_start=args.start, point_past=args.past, point_future=args.future,
                     origin_distance=args.origin_distance, dest_folder=args.dest)


if __name__ == '__main__':
    main()
