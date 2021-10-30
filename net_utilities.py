# Prove split dataset
import os
import numpy as np
import argparse
import json
from configs.config import cfg
import platform

# NB: lo split va fatto sui video (nel senso di nomi delle cartelle)

# non sta qui !


def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


# per path di windows creati con join che hanno slash \
def right_slash(path):
    if platform.system() is 'Windows' and '\\' in path:
        path = path.replace('\\', '/')
        print("Changing '\\' slashes")
        # print("path traformato: ", path)

    return path


# def dataset_split(folder, train_perc, test_perc, config_folder):
    # base_dest = cfg.C.JSON_DATASET_PATH
def dataset_split(folder, train_perc, test_perc):  # base_dest, config_folder

    dataset = os.listdir(folder)
    size = len(dataset)  # numero di cartelle video* con i frame e i json
    indices = np.arange(size)
    print(indices)

    train_size = int(round((train_perc * size) / 100, 0))
    test_size = int(round((test_perc * size) / 100, 0))
    # validation_size

    print("\tTRAIN SIZE: ", train_size)
    print("\tTEST SIZE: ", test_size)

    # SPLIT
    np.random.shuffle(indices)
    train, test, validation = np.sort(indices[:train_size]), np.sort(indices[train_size:(train_size + test_size)]), \
                                 np.sort(indices[(train_size + test_size):])
    print("\tTRAINING: ", train)
    print("\tTEST: ", test)
    print("\tVAL: ", validation)

    train_a = []
    test_a = []
    val_a = []
    for i in range(size):
        el = dataset[i]
        path = folder + '/' + el
        print("\tI: ", i)
        print("\tPATH: ", path)

        if i in train:
            dic = {'Path': path, 'ind': dataset.index(el)}
            train_a.append(dic)
        elif i in test:
            dic = {'Path': path, 'ind': dataset.index(el)}
            test_a.append(dic)
        else:
            dic = {'Path': path, 'ind': dataset.index(el)}
            val_a.append(dic)

    print("\tTRAIN ARRAY: ", train_a)
    print("\tTEST ARRAY: ", test_a)
    print("\tVALIDATION ARRAY: ", val_a)

    # if not os.path.exists(base_dest + config_folder):
    #     os.mkdir(base_dest + config_folder)

    # write_json(train_a, base_dest + config_folder + '/train.json')
    # write_json(test_a, base_dest + config_folder + '/test.json')
    # write_json(val_a, base_dest + config_folder + '/validation.json')
    return train_a, test_a, val_a


def folder_process(dataset_folder, train_perc, test_perc, base_dest, config_folder):
    train_array = []
    test_array = []
    val_array = []
    print(os.listdir(dataset_folder))
    dirs = os.listdir(dataset_folder)
    for d in dirs:
        print("Subdir: ", d)  # normal / sx_* / dx_*
        # sub_dir = os.listdir(dataset_folder + d)
        # for s in sub_dir:
        vid_path = right_slash(os.path.join(dataset_folder, d))  # s
        print("\t Video folder path: ", vid_path)
        train_a, test_a, val_a = dataset_split(vid_path, train_perc, test_perc)  # base_dest, config_folder
        # Concateno gli array
        # TODO: scrivere meglio ...
        for t in train_a:
            train_array.append(t)
        for t in test_a:
            test_array.append(t)
        for t in val_a:
            val_array.append(t)

    if not os.path.exists(base_dest + config_folder):
        os.mkdir(base_dest + config_folder)

    write_json(train_array, base_dest + config_folder + '/train.json')
    write_json(test_array, base_dest + config_folder + '/test.json')
    write_json(val_array, base_dest + config_folder + '/validation.json')


if __name__ == '__main__':
    # folder = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/images_dataset/sx_bla/'
    # base_dest = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/json_dataset/'  # argomento
    # config_folder = 'config2'
    # dataset_split(folder, 70, 20, base_dest, config_folder)

    parser = argparse.ArgumentParser(description="Split dataset")

    parser.add_argument("--folder", dest="input", default=cfg.DATASET_PATH,
                        help="Path to the folder that contains the dataset (normal / sx_* / dx_* folders)")
    parser.add_argument("--train_p", dest="train_p", default='',
                        help="% of training samples, expressed as integer")
    parser.add_argument("--test_p", dest="test_p", default='',
                        help="% of testing samples, expressed as integer")
    parser.add_argument("--base", dest="base", default=cfg.JSON_DATASET_PATH,
                        help="Path to the json_dataset folder")
    parser.add_argument("--conf", dest="conf", default='', help="Name of the desired config folder")
    args = parser.parse_args()

    folder_process(dataset_folder=args.input, train_perc=int(args.train_p), test_perc=int(args.test_p),
                   base_dest=args.base, config_folder=args.conf)

    # dataset_split(folder=args.input, train_perc=int(args.train_p), test_perc=int(args.test_p),
    #               base_dest=args.base, config_folder=args.conf)


