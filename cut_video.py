'''''''''
input: nome video, nome del video tagliato, frame di inizio e fine del video tagliato
'''
# import pyzed.sl as sl
import os, shutil
import subprocess, sys
import json


def main():
    with open('/home/aivdepth/json/cut_video_j.json') as json_file:
        d = json.load(json_file)

    zed_path = '../../../usr/local/zed/tools/ZED_SVO_Editor'
    path_video_new = "../Video_dataset/svo/cut/"  # path video tagliati .. prende in input

    for i in range(len(d)):
        path_video_old = d[i]['Path']  # path video manovre .. prende in input
        new_name = ("cut_video%d" % (i))  # nome video tagliato
        start = d[i]['Start']
        end = d[i]['End']
	#print('path_video_new', path_video_new, 'new_name', new_name)
        os.system(f"{zed_path} -cut {path_video_old} -s {start} -e {end} {path_video_new}{new_name}.svo")

    # old_name = ("video%d" % (i + 1))  # parte da 1
    # new_name = ("cut_video%d" % (i + 1))  # nome video tagliato
    # os.system(f"{zed_path} -cut {video_path}{old_name}.svo -s 100 -e 300 /Video_dataset/svo/cut/{new_name}.svo")

    # count_len = len(os.listdir(dir_name))
    # os.system(f"{zed_path} -inf {video_path}")
    # print(count_len)
    # for i in range(count_len):  # if frame > ...
    #    old_name = ("video%d" % (i + 1))  # parte da 1
    #    new_name = ("cut_video%d" % (i + 1))  # nome video tagliato
    #    os.system(f"{zed_path} -cut {video_path}{old_name}.svo -s 100 -e 300 Video_dataset/svo/cut/{new_name}.svo")


if __name__ == "__main__":
    main()
