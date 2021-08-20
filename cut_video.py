# import pyzed.sl as sl
import os, shutil
import subprocess, sys


def main():
    # value = input('prova')
    # print(f'{value}')
    # relative = "../../"
    # print(os.path.abspath(relative))
    # print(os.path.exists('../../usr/local/zed/tools/'))

    dir_name = os.path.dirname('Video_dataset/svo/video/')  # path video manovre
    count_len = len(os.listdir(dir_name))

    zed_path = '../../usr/local/zed/tools/ZED_SVO_Editor'
    video_path = 'Video_dataset/svo/video/'
    dest_path = "Video_dataset/svo/cut/"  # path video tagliati
    # os.system(f"{zed_path} -inf {video_path}")
    print(count_len)
    for i in range(count_len):  # if frame > ...
        old_name = ("video%d" % (i + 1))  # parte da 1
        new_name = ("cut_video%d" % (i + 1))  # nome video tagliato
        os.system(f"{zed_path} -cut {video_path}{old_name}.svo -s 100 -e 300 Video_dataset/svo/cut/{new_name}.svo")


if __name__ == "__main__":
    main()
