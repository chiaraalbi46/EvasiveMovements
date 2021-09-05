import cv2
import os
import argparse
from create_csv_file import right_slash
from configs.config import cfg

SCALE_PERCENT = 12.5
ext = '.png'


# TODO: voglio avere images_dataset e images_dataset_processed

def preprocess_frames(dir_video):
    images_path = dir_video + '/left_frames/'
    output = dir_video + "/left_frames_processed/"
# def preprocess_frames(origin_folder, dest_folder):  # Secondo me conviene che siano insieme ...
#     images_path = right_slash(origin_folder + '/left_frames/')
#     output = right_slash(dest_folder + '/left_frames/')

    if not os.path.exists(output):
        os.makedirs(output)

    for image in sorted(os.listdir(images_path)):
        print('Image: ' + image)
        if image.endswith(ext):
            img = cv2.imread(images_path + image)  # Returns matrix
            height = img.shape[0]  # Returns a tuple of the number of rows, columns, and channels
            width = img.shape[1]
            crop_img = img[60:-25, :, :]  # img[margin:-margin, margin:-margin]
            new_width = int(width * SCALE_PERCENT / 100)
            new_height = int(height * SCALE_PERCENT / 100)
            dim = (new_width, new_height)
            resized = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(output, image), resized)


# sempre scansione svo_cut/normal o svo_cut/sx_*/dx_*


def main(folder):  # images_dataset
    print(os.listdir(folder))
    dirs = os.listdir(folder)
    # process_folder = folder + '_processed/'  # cartella del dataset pre processato (images_dataset_processed)
    for d in dirs:
        print("Subdir: ", d)  # normal / sx_* / dx_*
        sub_dir = os.listdir(folder + d)
        for s in sub_dir:
            # spl1 = s.split('.')
            # vname = spl1[0]
            # print(vname)
            vid_path = right_slash(os.path.join(folder, d, s))
            print("\t Video folder path: ", vid_path)
            preprocess_frames(vid_path)
            # proc_path = right_slash(os.path.join(process_folder, d, s))
            # print("\t Video processed folder path: ", proc_path)
            preprocess_frames(vid_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preprocessing of the left frames.")

    # parser.add_argument("--folder", dest="input",
    #                     default='D:/Dataset_Evasive_Movements/datasets/images_dataset/',
    #                     help="Path of the folder containing normal and sx_*, dx_* subfolders")
    # rivedere ...
    parser.add_argument("--folder", dest="input",
                        default=cfg.DATASET_PATH,
                        help="Path of the folder containing normal and sx_*, dx_* subfolders")
    args = parser.parse_args()
    main(folder=args.input)
