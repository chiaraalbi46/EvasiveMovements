import csv
import json
import platform
import os
import argparse

if platform.system() == 'Windows':
    DATASETS_PATH = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/'
else:
    DATASETS_PATH = '/home/aivdepth/datasets/'

CSV_DATASET_PATH = os.path.join(DATASETS_PATH, 'csv_dataset')


def create_csv(config_path, data_type, len_seq):
    # file_path = config_path + data_type + '.json'
    file_path = os.path.join(config_path, data_type + '.json')
    print('filepath: ', file_path)

    if platform.system() is 'Windows' and '\\' in file_path:
        file_path = file_path.replace('\\', '/')
        print("path traformato: ", file_path)

    with open(file_path, 'r') as jsonfile:
        d = json.load(jsonfile)

    spl = config_path.split('/')
    conf = spl[len(spl) - 1]  # se metto lo slash finale devo mettere 2
    print("CONFIG: ", conf)

    # dir_name = os.path.dirname(os.path.abspath('__file__'))
    # print("dir_name: ", dir_name)

    save_dir = os.path.join(CSV_DATASET_PATH, data_type)
    print("save_dir: ", save_dir)
    save_path = right_slash(os.path.join(save_dir, data_type + '_' + conf + '_' + str(
        len_seq) + '_sequence.csv'))
    print("save_path: ", save_path)

    with open(save_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        for j in range(len(d)):  # ciclo sul json
            path = d[j]['Path']  # path alla cartella video j-esimo
            print("PATH: ", path)

            spl = path.split('/')
            vid_name = spl[len(spl) - 1]

            json_folder = path + '/json/'
            # print("json folder: ", json_folder)

            data = json.load(open(json_folder + vid_name + '_traj.json'))  # apro il file con le traiettorie
            for i in range(len(data)):

                past = data[i]['Past']
                future = data[i]['Future']

                ind_frame = data[i]['Frame']
                print("\t FRAME: ", ind_frame)

                name = 'frame' + str(ind_frame)
                if ind_frame < 10:
                    name = 'frame000' + str(ind_frame)
                elif 10 <= ind_frame < 100:
                    name = 'frame00' + str(ind_frame)
                elif 100 <= ind_frame < 1000:
                    name = 'frame0' + str(ind_frame)

                img_path = os.path.join(path, "left_frames/", name + '.png')
                if platform.system() is 'Windows' and '\\' in img_path:
                    img_path = img_path.replace('\\', '/')
                    print("path traformato: ", img_path)
                # print("img_path: ", img_path)

                past.append(data[i]['Present'])  # past = past + present
                lines = [path, img_path, past, future]  # rivedere se serve path
                filewriter.writerow(lines)


# per path di windows creati con join che hanno slash \

def right_slash(path):
    if platform.system() is 'Windows' and '\\' in path:
        path = path.replace('\\', '/')
        print("Changing '\\' slashes")
        # print("path traformato: ", path)

    return path


def main():
    # vedere se tenere path e passare solo config_0 o numero
    # config_path = 'C:/Users/chiar/PycharmProjects/EvasiveMovements/datasets/json_dataset/config2'
    # create_csv(config_path, 'train', 10)

    parser = argparse.ArgumentParser(description="Create the CSV file from video sequences")
    parser.add_argument("--config_path", dest="input", default=None, help="Path to the json 'splitting' file")
    parser.add_argument("--type", dest="data_type", default=None, help="Choose the dataset: train, validation, test")
    parser.add_argument("--len_seq", dest="len_seq", default=None, help="Define the number of predicted coords to consider")

    args = parser.parse_args()

    create_csv(config_path=args.input, data_type=args.data_type, len_seq=int(args.len_seq))


if __name__ == '__main__':
    main()



# with open(save_path, 'w') as csvfile:
#     filewriter = csv.writer(csvfile)
#     for seq in os.listdir(video_path):
#         print("SEQ: ", seq)
#         path = video_path + seq + '/'  # path to i-th sequence
#         print("PATH: ", path)
#         if platform.system() is 'Windows' and '\\' in path:
#             path = path.replace('\\', '/')
#             print("path traformato: ", path)
#
#         json_folder = path + seq + '/json/'
#         if not os.path.exists(json_folder):
#             print("Crea la cartella json")
#             os.mkdir(json_folder)
#         data = json.load(open(json_folder + '_traj.json'))  # apro il file con le traiettorie
#         for i in range(len(data)):
#             past = data[i]['Past']
#             future = data[i]['Future']
#
#             ind_frame = data[i]['Frame']
#
#             name = 'frame' + str(ind_frame)
#             if ind_frame < 10:
#                 name = 'frame000' + str(ind_frame)
#             elif 10 <= ind_frame < 100:
#                 name = 'frame00' + str(ind_frame)
#             elif 100 <= ind_frame < 1000:
#                 name = 'frame0' + str(ind_frame)
#
#             img_path = os.path.join(path, "left_frames/", name + '.png')
#             print("img_path: ", img_path)
#
#             new_past = past.append(data[i]['Present'])  # past = past + present
#             lines = [path, img_path, new_past, future]  # rivedere se serve path
#             filewriter.writerow(lines)