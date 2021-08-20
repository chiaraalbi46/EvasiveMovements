import json
import argparse
import numpy as np
import math
import os


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# array origine
def origin_traj(i_start, xdata, zdata, angle, point_future):
    # Origini
    origin = []
    angle_o = []
    # num_vectors = 10 #quanti vettori per origine
    # i_start = 0 # posso cambiare il punto di partenza
    count = 0  # step per selezionare origini
    while i_start < len(xdata):
        while count < point_future and i_start + count < len(xdata):
            origin.append([xdata[i_start], zdata[i_start], 0])  # vedere se mettere z = y o z = z
            angle_o.append(angle[i_start])  # vedere se mettere z = y o z = z
            count += 1
        count = 0
        i_start += point_future  # num_vectors
    # print("Origin: ", origin)
    return origin, angle_o


# def create_traj_json(i_start, point_past, point_future):
#     with open('C:/Users/ninad/Desktop/video_guida/json/video16.json') as json_file:
def create_traj_json(video_json_path, i_start, point_past, point_future, dest_folder):
    i_start = int(i_start)
    point_past = int(point_past)
    point_future = int(point_future)
    with open(video_json_path) as json_file:
        d = json.load(json_file)
        # print(d)
        xdata = []
        zdata = []
        angle = []

        step = 0
        for i in range(len(d)):
            if i == step:
                xdata.append(d[i]['cords'][0])
                zdata.append(d[i]['cords'][2])  # vedere se mettere z = y o Z = z
                angle.append(d[i]['angle'])
                step += 50  # passare in input ?

    # angolo dei soli origini
    origin, angle_o = origin_traj(i_start, xdata, zdata, angle, point_future)  # crea origini

    # futuro, presente, passato
    future = []
    present = []
    past = []
    array = []
    frame = 0
    first = True

    dic_traj = {'Frame': [], 'Past': [], 'Present': [], 'Future': [], }
    matrix = []
    for i in range(len(origin) - 1):
        # matrice di rotazione
        mR = np.array(
            [[math.cos(angle_o[i]), -math.sin(angle_o[i]), 0], [math.sin(angle_o[i]), math.cos(angle_o[i]), 0, ],
             [0, 0, 1]])
        new_point = origin[i] + np.dot(mR, ([xdata[i] - origin[i][0], zdata[i] - origin[i][1], 1]))
        matrix.append(new_point)
        print(matrix)
        if origin[i] == origin[i + 1]:
            if first:  # salvo l'indice dell'origine
                present.append([matrix[i][0], matrix[i][1]])
                frame = i
                first = False
                count = point_past  # numero punti del passato
                while i - count > 0 and count > 0:
                    past.append([matrix[i - count][0], matrix[i - count][1]])
                    count -= 1

            if i != frame:  # non inserisco l'origine nel futuro
                future.append([matrix[i][0], matrix[i][1]])
            if i + 1 == len(origin) - 1:  # prendo l'ultimo punto
                future.append([matrix[i][0], matrix[i][1]])

                dic_traj['Frame'] = frame  # indice dell'origine
                dic_traj['Past'] = past
                dic_traj['Present'] = present
                dic_traj['Future'] = future
                array.append(dic_traj)
        else:
            future.append([matrix[i][0], matrix[i][1]])
            new_origin = origin[i + 1] + np.dot(mR,
                                                ([xdata[i + 1] - origin[i + 1][0], zdata[i + 1] - origin[i + 1][1], 1]))
            future.append([new_origin[0], new_origin[1]])  # inserisco nel futuro l'origine futuro ( serve ??)

            first = True
            dic_traj['Frame'] = frame  # indice dell'origine
            dic_traj['Past'] = past
            dic_traj['Present'] = present
            dic_traj['Future'] = future

            array.append(dic_traj)
            dic_traj = {}
            future = []
            present = []
            past = []
            frame = 0
    for i in range(len(array)):
        print(array[i], '\n')

    # write_json(array, 'C:/Users/ninad/Desktop/video_guida/json/video16_traj.json')

    spl = video_json_path.split(os.sep)  # '/'
    vid_name = spl[len(spl) - 1]
    spl1 = vid_name.split('.')
    vname = spl1[0]
    print(vname)
    final_name = vname + '_traj.json'
    pathToTrajFile = dest_folder + final_name  # devo avere messo lo slah in pathToTrajDir !
    print(pathToTrajFile)

    write_json(array, pathToTrajFile)


def main():
    parser = argparse.ArgumentParser(description="Create the trajectories' file from a json file of a video sequence")

    parser.add_argument("--video_json_path", dest="input", default=None, help="Path of the json file of a video")
    parser.add_argument("--i_start", dest="start", default=0, help="Initial system origin")
    parser.add_argument("--point_past", dest="past", default=None,
                        help="Number of past points to remap in the new reference system")
    parser.add_argument("--point_future", dest="future", default=None,
                        help="Number of future points to remap in the new reference system")
    parser.add_argument("--dest_folder", dest="dest", default=None,
                        help="Path to the destination folder for the trajectories' file")

    args = parser.parse_args()

    create_traj_json(video_json_path=args.input, i_start=args.start, point_past=args.past, point_future=args.future, dest_folder=args.dest)


if __name__ == '__main__':
    # create_traj_json(0, 5, 10)  # i_start, point_past, point_future
    main()
