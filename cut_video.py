"""
input: file json in cui per ogni video da tagliare nome video, frame di inizio e fine del video da tagliare
"""

import os
import json
import argparse
import platform
import subprocess


def main(videos_file):
    with open(videos_file) as json_file:
        d = json.load(json_file)

    win = 0
    if platform.system() == 'Windows':
        print("Windows")
        tools_path = 'C:/Program Files (x86)/ZED SDK/tools/'
        zed_path = "ZED SVOEditor.exe"
        # zed_path = "C:/Program Files (x86)/ZED SDK/tools/'ZED SVOEditor.exe'"
        path_video_new = "D:/Dataset_Evasive_Movements/video/svo_cut/"
        os.chdir(tools_path)
        print(os.getcwd())
        win = 1
    else:
        zed_path = '../../../usr/local/zed/tools/ZED_SVO_Editor'
        path_video_new = "../Video_dataset/svo_cut/"

    if os.path.exists(path_video_new):
        print("La cartella e' gia' presente")
    else:
        print("Path video new: ", path_video_new)
        os.mkdir(path_video_new)

    for i in range(len(d)):
        start = d[i]['Start']
        end = d[i]['End']
        path_video_old = d[i]['Path'] + '.svo'  # path video manovre .. prende in input

        spl = path_video_old.split('/')
        # nome video
        vid_name = spl[len(spl) - 1]
        print("Vname: ", vid_name)

        subdir_name = spl[len(spl) - 2]
        print("Subdir: ", subdir_name)

        # controllo se la cartella esiste sennò la creo
        final_dir_path = path_video_new + subdir_name + '/'

        if subdir_name.startswith('d', 0, 1) or subdir_name.startswith('s', 0, 1):
            print("Manovre --> tengo la sottocartella")
        else:
            print("Video guida normale --> non considero la sottocartella, metto tutto in normal")
            final_dir_path = path_video_new + 'normal/'

        if os.path.exists(final_dir_path):
            print("La cartella e' gia' presente")
        else:
            print("Final dir path: ", final_dir_path)
            os.mkdir(final_dir_path)

        cut_video_path = final_dir_path + vid_name
        print("NAME: ", cut_video_path)

        # if win == 1:  # Windows
        #     cut_video_path = cut_video_path.replace('/', '\\')  # \
        #     path_video_old = path_video_old.replace('/', '\\')

        if os.path.exists(cut_video_path):
            print("File gia' tagliato")
        else:
            subprocess.call([zed_path, '-cut', path_video_old, '-s', str(start), '-e', str(end), cut_video_path])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cut a group of video given a json file.")

    parser.add_argument("--videos_file", dest="input", default='/home/aivdepth/json/cut_video_j.json',
                        help="Path of the json file to cut videos")
    args = parser.parse_args()
    main(videos_file=args.input)