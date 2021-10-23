import json
import os
import argparse
from configs.config import cfg
from net_utilities import right_slash
import csv

# CSV_DATASET_PATH = cfg.CSV_DATASET_PATH  # os.path.join(DATASETS_PATH, 'csv_dataset')


def video_traj(filewriter, data, path, flip):
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

        img_path = right_slash(os.path.join(path, "left_frames" + flip + "processed/", name + '.png'))
        # print('path: ', img_path)
        past.append(data[i]['Present'])  # past = past + present
        lines = [path, img_path, past, future]  # rivedere se serve path
        filewriter.writerow(lines)
    # return filewriter


def create_csv(csv_path, config_path, config_f, data_type, len_seq, flip, od, fp, project):  # origin_distance, future_points
    config_path = config_path + config_f
    # file_path = config_path + data_type + '.json'
    file_path = right_slash(os.path.join(config_path, data_type + '.json'))
    print('filepath: ', file_path)

    with open(file_path, 'r') as jsonfile:
        d = json.load(jsonfile)

    # save_dir = right_slash(os.path.join(csv_path, data_type))
    save_dir = right_slash(os.path.join(csv_path, project, data_type))
    print("save_dir: ", save_dir)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = right_slash(os.path.join(save_dir, data_type + '_' + config_f + '_' + str(len_seq) + '_sequence.csv'))
    print("save_path: ", save_path)

    with open(save_path, 'w') as csvfile:
        filewriter = csv.writer(csvfile)
        for j in range(len(d)):  # ciclo sul json
            path = d[j]['Path']  # path alla cartella video j-esimo
            print("PATH: ", path)

            spl = path.split('/')
            vid_name = spl[len(spl) - 1]

            json_folder = path + '/'
            # print("json folder: ", json_folder)

            data = json.load(open(json_folder + vid_name + '_' + od + '_' + fp + '_traj.json'))  # apro il file con le traiettorie
            video_traj(filewriter, data, path, '_')

            if flip == 1:
                data_flip = json.load(
                    open(json_folder + vid_name + '_' + od + '_' + fp + '_traj_flip.json'))  # apro il file con le traiettorie
                video_traj(filewriter, data_flip, path, '_flip_')


def main():

    parser = argparse.ArgumentParser(description="Create the CSV file from video sequences.")
    parser.add_argument("--csv_path", dest="csv", default=cfg.CSV_DATASET_PATH,
                        help="Path to the json folder where 'splitting' files are contained")
    parser.add_argument("--config_path", dest="input", default=cfg.JSON_DATASET_PATH,
                        help="Path to the json folder where 'splitting' files are contained")
    parser.add_argument("--config_f", dest="folder", default='', help="Name of the config folder desired")
    parser.add_argument("--type", dest="data_type", default=None, help="Choose the dataset: train, validation, test")
    parser.add_argument("--len_seq", dest="len_seq", default=None,
                        help="Define the number of predicted coords to consider")
    parser.add_argument("--flip", dest="flip", default=0, help="0 no flip, 1 flip")
    parser.add_argument("--od", dest="od", default=None, help="Origin distance")
    parser.add_argument("--fp", dest="fp", default=None, help="Number of future points")
    parser.add_argument("--project", dest="project", default=None, help="Name of the project folder.")


    args = parser.parse_args()

    create_csv(csv_path=args.csv, config_path=args.input, config_f=args.folder, data_type=args.data_type,
               len_seq=int(args.len_seq), flip=int(args.flip), od=args.od, fp=args.fp, project=args.project)


if __name__ == '__main__':
    main()
