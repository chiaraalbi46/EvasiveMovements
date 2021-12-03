""" Rename files """

import os
from net_utilities import right_slash
import argparse


def folder_process(folder, od, fp, pp):
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
                    stri = '_' + od + '_' + fp
                    if stri in file_json:
                        print("rename file !!")
                        new_stri = stri + '_' + pp
                        j_new = j.replace(stri, new_stri)
                        new_file_json = json_folder + j_new
                        print('NEW NAME: ', new_file_json)
                        os.rename(file_json, new_file_json)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Rename files with no pp")

    parser.add_argument("--folder", dest="input", default=None, help="Path image dataset")
    parser.add_argument("--od", dest="od", default=None, help="Origin distance")
    parser.add_argument("--fp", dest="fp", default=None, help="Future points")
    parser.add_argument("--pp", dest="pp", default=None, help="Past points")  # l'info che vogliamo aggiungere ai nomi

    args = parser.parse_args()

    folder_process(folder=args.input, od=args.od, fp=args.fp, pp=args.pp)
    # vogliamo aggiungere pp prima di traj ai file che non lo hanno ...
    # forse meglio farlo per casi specifici ... tipo voglio rinominare i file con futuri 20 e basta
    # quindi dovrei specificare qualche parametro in più, od e fp mi sa

    # python rename_files.py --folder D:\Dataset_Evasive_Movements\datasets\img_dataset\ --fp 10 --od 4 --pp 5
    # se ci sono file uguali con flip rinomina anche quelli ... ma è ok
