# Prove split dataset
import os
import numpy as np
from create_video_json import write_json
import argparse
from configs.config import cfg

# NB: lo split va fatto sui video (nel senso di nomi delle cartelle)

# TODO: rinominare video con 0*
# TODO: mettere qui controllo per avere video0* se ho video3 ad esempio oppure rinominare anche video con una sola cifra


# def dataset_split(folder, train_perc, test_perc, config_folder):
    # base_dest = cfg.C.JSON_DATASET_PATH
def dataset_split(folder, train_perc, test_perc, base_dest, config_folder):

    dataset = os.listdir(folder)
    size = len(dataset)  # numero di cartelle video* con i frame e i json
    indices = np.arange(size)
    print(indices)

    train_size = int(round((train_perc * size) / 100, 0))
    test_size = int(round((test_perc * size) / 100, 0))
    # validation_size

    print("TRAIN SIZE: ", train_size)
    print("TEST SIZE: ", test_size)

    # SPLIT
    np.random.shuffle(indices)
    train, test, validation = np.sort(indices[:train_size]), np.sort(indices[train_size:(train_size + test_size)]), \
                                 np.sort(indices[(train_size + test_size):])
    print("TRAINING: ", train)
    print("TEST: ", test)
    print("VAL: ", validation)

    train_a = []
    test_a = []
    val_a = []
    for i in range(size):
        el = dataset[i]
        # poi non ci sarà
        # spl = el.split('.')
        # vid_name = spl[0]
        # path = folder + vid_name
        path = folder + el
        print("I: ", i)
        print("PATH: ", path)

        if i in train:
            dic = {'Path': path, 'ind': dataset.index(el)}
            train_a.append(dic)
        elif i in test:
            dic = {'Path': path, 'ind': dataset.index(el)}
            test_a.append(dic)
        else:
            dic = {'Path': path, 'ind': dataset.index(el)}
            val_a.append(dic)

    print("TRAIN ARRAY: ", train_a)
    print("TEST ARRAY: ", test_a)
    print("VALIDATION ARRAY: ", val_a)

    if not os.path.exists(base_dest + config_folder):
        os.mkdir(base_dest + config_folder)

    write_json(train_a, base_dest + config_folder + '/train.json')
    write_json(test_a, base_dest + config_folder + '/test.json')
    write_json(val_a, base_dest + config_folder + '/validation.json')


if __name__ == '__main__':
    # folder = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/images_dataset/sx_bla/'
    # base_dest = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/json_dataset/'  # argomento
    # config_folder = 'config2'
    # dataset_split(folder, 70, 20, base_dest, config_folder)

    parser = argparse.ArgumentParser(description="Split dataset")

    parser.add_argument("--folder", dest="input", default=cfg.DATASET_PATH['original'],
                        help="Path to the folder that contains the dataset (video folders with frames and json)")
    parser.add_argument("--train_p", dest="train_p", default='',
                        help="% of training samples, expressed as integer")
    parser.add_argument("--test_p", dest="test_p", default='',
                        help="% of testing samples, expressed as integer")
    parser.add_argument("--base", dest="base", default=cfg.JSON_DATASET_PATH,
                        help="Path to the json_dataset folder")
    parser.add_argument("--conf", dest="conf", default='', help="Name of the desired config folder")
    args = parser.parse_args()

    dataset_split(folder=args.input, train_perc=int(args.train_p), test_perc=int(args.test_p),
                  base_dest=args.base, config_folder=args.conf)

    # dataset_split(folder=args.input, train_perc=int(args.train_p), test_perc=int(args.test_p),
    # config_folder=args.conf)











# path_to_dataset_dir = 'D:/Dataset_Evasive_Movements/video/svo/23luglio/'
# dataset = os.listdir(path_to_dataset_dir)
# print(type(dataset))
# Create indices for the split
# dataset = [0, 1, 2, 3, 4, 5, 6, 7]
# dataset_size = len(dataset)
# test_size = int(test_split)  # int(test_split * dataset_size)
# train_size = dataset_size - test_size
# print("Test size: ", test_size)
# print("Train size: ", train_size)
#
# # 4,3, 1 paramentri
# np.random.shuffle(dataset)
# training, test, validation = np.sort(dataset[:4]), np.sort(dataset[4:(4+3)]), np.sort(dataset[(4+3):])
# print("TRAINING: ", training)
# print("TEST: ", test)
# print("VAL: ", validation)







# train_dataset, test_dataset = torch.utils.data.random_split(dataset,
#                                            [train_size, test_size])


# path_to_dataset_dir = 'D:/Dataset_Evasive_Movements/video/svo/23luglio/'  # sarà
# dataset = os.listdir(path_to_dataset_dir)
# print(type(dataset))

# train_dataset, test_dataset = torch.split(torch.FloatTensor(dataset), [train_size, test_size])
# torch.split(torch.Tensor(dataset), [5, 3])  # no perchè la lista è di str !
# print(torch.split(torch.Tensor(dataset), [5, 3]))
# a questo punto avrei i 'video' del train e del test
# però mi devo andare a prendere i frame di questi video

# print("TRAIN: ", train_dataset)
# print("TEST: ", test_dataset)



    # batch_size = 2
    # train_loader = torch.utils.data.DataLoader(
    #     train_dataset,
    #     batch_size=batch_size,
    #     shuffle=True)
    # test_loader = torch.utils.data.DataLoader(
    #     test_dataset,  # test_dataset.dataset
    #     batch_size=batch_size,
    #     shuffle=True)
    #
    # for data in train_loader:
    #     print("Train: ", data)
    #
    # print('')
    #
    # for d in test_loader:
    #     print("Test: ", d)

    # return train_dataset, test_dataset
    # return train_loader, test_loader
