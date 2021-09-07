##
import argparse
import json
import os
import math
from create_csv_file import right_slash


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def transform_RT(xdata, zdata, i, origin, angle_o, f, count):
    # Rotazione (angolo in radianti)
    x_rot = (xdata[i + count] - origin[f][0]) * math.cos(angle_o[f]) - (
            zdata[i + count] - origin[f][1]) * math.sin(angle_o[f])
    y_rot = (xdata[i + count] - origin[f][0]) * math.sin(angle_o[f]) + (
            zdata[i + count] - origin[f][1]) * math.cos(angle_o[f])
    print('i', i, 'count', count)
    # Traslazione
    x_rot_t = x_rot + origin[f][0]
    y_rot_t = y_rot + origin[f][1]
    new_point = [x_rot_t, y_rot_t]
    new_point[0] = round(x_rot_t, 3)
    new_point[1] = round(y_rot_t, 3)
    return new_point


# array origine
def origin_traj(i_start, xdata, zdata, angle, origin_distance):
    # Origini
    origin = []
    angle_o = []
    while i_start < len(xdata):
        origin.append([xdata[i_start], zdata[i_start]])
        angle_o.append(angle[i_start])
        i_start += origin_distance  # num_vectors
    return origin, angle_o


def create_traj_json(video_json_path, i_start, point_past, point_future, origin_distance, dest_folder):

    point_future = point_future + 1  # +1 punto futuro (origine da escludere)

    with open(video_json_path) as json_file:
        d = json.load(json_file)
        xdata = []
        zdata = []
        angle = []

        # step = 0
        for i in range(len(d)):
            # if i == step:
            xdata.append(d[i]['cords'][0])
            zdata.append(d[i]['cords'][2])
            angle.append(d[i]['angle'])
            #     step += sample

    # angolo dei soli origini
    origin, angle_o = origin_traj(i_start, xdata, zdata, angle, origin_distance)  # crea origini

    # futuro, presente, passato
    future = []
    present = []
    past = []
    array = []
    dic_traj = {'Frame': [], 'Past': [], 'Present': [], 'Future': [], }

    f = 0
    for i in range(len(xdata)):
        if xdata[i] == origin[f][0] and zdata[i] == origin[f][1] and f < len(origin) - 1 and i % origin_distance == 0:
            present.append(origin[f])

            # Punti futuri
            count_future = 1
            while count_future < point_future and i + count_future < len(xdata):
                new_point = transform_RT(xdata, zdata, i, origin, angle_o, f, count_future)
                future.append(new_point)
                count_future += 1

            # Punti passati
            count = point_past
            while i - count > 0 and count > 0:
                new_point = transform_RT(xdata, zdata, i, origin, angle_o, f, (-count))
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
        final_name = vname + '_traj.json'
        pathToTrajFile = dest_folder + final_name  # devo avere messo lo slah in pathToTrajDir !

        write_json(array, pathToTrajFile)


# folder = 'D:\Dataset_Evasive_Movements\datasets\images_dataset\'
def folder_process(folder, i_start, point_past, point_future, origin_distance):
    print(folder)
    print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:  # normal / sx_* / dx_*
        print("Subdir: ", d)
        sub_dir = os.listdir(folder + d)

        for s in sub_dir:  # video*
            json_folder = right_slash(os.path.join(folder, d, s)) + '/'  # + '/json/'
            print("\t json folder: ", json_folder)
            video_json_path = json_folder + s + '.json'  # .../video*.json
            print("\t video json path: ", video_json_path)
            create_traj_json(video_json_path, i_start, point_past, point_future, origin_distance, json_folder)


def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video_json_path", dest="input", default=None, help="Path of the json file of a video")
    parser.add_argument("--i_start", dest="start", default=0, help="Initial system origin")
    parser.add_argument("--point_past", dest="past", default=5,
                        help="Number of past points to remap in the new reference system")
    parser.add_argument("--point_future", dest="future", default=30,
                        help="Number of future points to remap in the new reference system")
    parser.add_argument("--origin_distance", dest="origin_distance", default=10,
                        help="Distance between two successive origins")

    parser.add_argument("--dest_folder", dest="dest", default=None,
                        help="Path to the destination folder for the trajectories' file")

    args = parser.parse_args()

    # folder_process(folder=args.input, i_start=int(args.start), point_past=int(args.past),
    # point_future=int(args.future),origin_distance=int(args.origin_distance))
    if os.path.isdir(args.input):
        # esecuzione su cartella (e sottocartelle)
        folder_process(folder=args.input, i_start=int(args.start), point_past=int(args.past),
                       point_future=int(args.future), origin_distance=int(args.origin_distance))
    else:
        # esecuzione singolo video
        create_traj_json(video_json_path=args.input, i_start=int(args.start), point_past=int(args.past),
                         point_future=int(args.future), origin_distance=int(args.origin_distance), dest_folder=args.dest)


if __name__ == '__main__':
    main()