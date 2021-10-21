import argparse
import json
import os
import math
from net_utilities import right_slash
from net_utilities import write_json


def transform_RT(xdata, zdata, i, origin, angle_o, f, count):
    # Rotazione (angolo in radianti)
    x_rot = round((xdata[i + count] - origin[f][0]) * math.cos(angle_o[f]) - (
            zdata[i + count] - origin[f][1]) * math.sin(angle_o[f]), 3)
    y_rot = round((xdata[i + count] - origin[f][0]) * math.sin(angle_o[f]) + (
            zdata[i + count] - origin[f][1]) * math.cos(angle_o[f]), 3)
    # print('i', i, 'count', count)
    # Traslazione ? .. presente devesse essere [0, 0] ?
    #x_rot_t = x_rot + origin[f][0]
    #y_rot_t = y_rot + origin[f][1]
    new_point = [x_rot, y_rot]
    return new_point


# array origine
def origin_traj(i_start, xdata, zdata, angle, origin_distance, frame_index):
    # Origini
    origin = []
    angle_o = []
    origin_index = []
    origine_i = []
    while i_start < len(xdata):
        origin.append([xdata[i_start], zdata[i_start]])
        angle_o.append(angle[i_start])
        origin_index.append(frame_index[i_start])
        origine_i.append(i_start)
        i_start += origin_distance  # num_vectors

    return origin, angle_o, origin_index, origine_i


def create_json_flip(path_json):
    with open(path_json) as json_file:
        d = json.load(json_file)

        for i in range(len(d)):
            for j in range(len(d[i]['Past'])):
                d[i]['Past'][j][0] = -1*d[i]['Past'][j][0]
            for j in range(len(d[i]['Future'])):
                d[i]['Future'][j][0] = -1*d[i]['Future'][j][0]
            #print(d[i]['Past'][0][0])

    ap = path_json.split('/')

    name_json = ap[len(ap)-1].split('.')[0] +'_flip.json'
    print(name_json)
    path_save = '/'.join(path_json.split('/')[:len(ap) - 1]) + '/' + name_json
    write_json(d, path_save)


def get_path_json(video_json_path, origin_distance, point_future, dest_folder):
    spl = video_json_path.split(os.sep)  # '/'
    vid_name = spl[len(spl) - 1]
    spl1 = vid_name.split('.')
    vname = spl1[0]
    final_name = vname + '_' + str(origin_distance) + '_' + str(point_future)  + '_traj.json'
    pathToTrajFile = dest_folder + final_name  # devo avere messo lo slah in pathToTrajDir !
    return pathToTrajFile


def create_traj_json(video_json_path, i_start, point_past, point_future, origin_distance, dest_folder):
    point_future = point_future + 1  # +1 punto futuro (origine da escludere)

    with open(video_json_path) as json_file:
        d = json.load(json_file)
        xdata = []
        zdata = []
        angle = []
        frame_index = []

        for i in range(len(d)):
            xdata.append(d[i]['cords'][0])
            zdata.append(d[i]['cords'][2])
            angle.append(d[i]['angle'])
            frame_index.append(d[i]['Frame'])

    # angolo dei soli origini
    origin, angle_o, origin_index, origine_i = origin_traj(i_start, xdata, zdata, angle, origin_distance,
                                                           frame_index)  # crea origini

    # futuro, presente, passato
    future = []
    present = []
    past = []
    array = []
    dic_traj = {'Frame': [], 'Past': [], 'Present': [], 'Future': [], }

    f = 0
    for i in range(len(xdata)):

        if origine_i[f] == i and f < len(
                origin) - 1:  # (i*step ) == origin_index[f] , and xdata[i] == origin[f][0] and zdata[i] == origin[f][1] and f < len(origin) - 1 :#and frame_index[i] % origin_distance == 0:
            #present.append(origin[f])
            # new_point = [xdata[i], zdata[i]]
            new_point = transform_RT(xdata, zdata, i, origin, angle_o, f, 0)
            present.append(new_point)

            # Punti futuri
            count_future = 1
            while count_future < point_future and i + count_future < len(xdata):
                # new_point = [xdata[i+count_future], zdata[i+count_future]]
                new_point = transform_RT(xdata, zdata, i, origin, angle_o, f, count_future)
                future.append(new_point)
                count_future += 1

            # Punti passati
            count = point_past
            while i - count >= 0 and count > 0:  # and i - count != 0:
                # new_point = [xdata[i-count], zdata[i-count]]
                new_point = transform_RT(xdata, zdata, i, origin, angle_o, f, (-count))
                past.append(new_point)
                count -= 1

            if len(past) == point_past and len(future) == point_future - 1:  # se hanno meno punti non salvo
                dic_traj['Frame'] = origin_index[f]  # indice dell'origine
                dic_traj['Past'] = past
                dic_traj['Present'] = present
                dic_traj['Future'] = future
                array.append(dic_traj)

            dic_traj = {}
            future = []
            present = []
            past = []
            f += 1

    pathToTrajFile = get_path_json(video_json_path, origin_distance, point_future, dest_folder)

    write_json(array, pathToTrajFile)
    for i in range(len(array)):
        print(array[i], '\n')


# folder = 'D:\Dataset_Evasive_Movements\datasets\images_dataset\'
def folder_process(folder, i_start, point_past, point_future, origin_distance, flip):
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
            #print("\t video json path: ", video_json_path)

            if flip == 0 or flip == 2:
                print('flip', type(flip), flip)
                create_traj_json(video_json_path, i_start, point_past, point_future, origin_distance, json_folder)
            if flip == 1 or flip == 2:
                pathToTrajFile = get_path_json(video_json_path, origin_distance, point_future, json_folder)
                create_json_flip(pathToTrajFile)



def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video_json_path", dest="input", default=None, help="Path of the json file of a video")
    parser.add_argument("--i_start", dest="start", default=0, help="Initial system origin")
    parser.add_argument("--step", dest="step", default=10, help="Step")

    parser.add_argument("--point_past", dest="past", default=5,
                        help="Number of past points to remap in the new reference system")
    parser.add_argument("--point_future", dest="future", default=10,
                        help="Number of future points to remap in the new reference system")
    parser.add_argument("--origin_distance", dest="origin_distance", default=4,
                        help="Distance between two successive origins")

    parser.add_argument("--dest_folder", dest="dest", default=None,
                        help="Path to the destination folder for the trajectories' file")

    parser.add_argument("--flip", dest="flip", default=0, help="0 no flip, 1 flip")

    args = parser.parse_args()

    # folder_process(folder=args.input, i_start=int(args.start), point_past=int(args.past),
    # point_future=int(args.future),origin_distance=int(args.origin_distance))
    if os.path.isdir(args.input):
        # esecuzione su cartella (e sottocartelle)
        folder_process(folder=args.input, i_start=int(args.start), point_past=int(args.past),
                       point_future=int(args.future), origin_distance=int(args.origin_distance), flip=int(args.flip))
    else:
        # esecuzione singolo video
        create_traj_json(video_json_path=args.input, i_start=int(args.start), point_past=int(args.past),
                         point_future=int(args.future), origin_distance=int(args.origin_distance),
                         dest_folder=args.dest)


if __name__ == '__main__':
    main()
