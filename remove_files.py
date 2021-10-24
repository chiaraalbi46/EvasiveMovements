# Remove files

import os
from net_utilities import right_slash
import argparse


def folder_process(folder, element):
    print(folder)
    print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:  # normal / sx_* / dx_*
        print("Subdir: ", d)
        sub_dir = os.listdir(folder + d)

        for s in sub_dir:  # video*
            json_folder = right_slash(os.path.join(folder, d, s)) + '/'
            js = os.listdir(json_folder)
            for j in js:
                if j.endswith('.json'):
                    file_json = json_folder + j
                    print("FILE: ", file_json)
                    if element in file_json:
                        print("remove file !!")
                        os.remove(file_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Remove redundant files")

    parser.add_argument("--folder", dest="input", default=None, help="Path image dataset")
    parser.add_argument("--el", dest="el", default=0, help="Element to look for in video folders")

    args = parser.parse_args()

    folder_process(folder=args.input, element=args.el)  # per noi ora _11_ (con gli underscore)
