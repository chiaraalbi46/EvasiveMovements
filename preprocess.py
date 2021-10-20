import cv2
import os
import argparse
from net_utilities import right_slash
from configs.config import cfg

SCALE_PERCENT = 12.5
ext = '.png'


def preprocess_frames(dir_video, flip):
    images_path = dir_video + '/left_frames/'
    output = dir_video + "/left_frames_processed/"
    if flip == 1:
        images_path = dir_video + '/left_frames_flip/'
        output = dir_video + "/left_frames_flip_processed/"

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


def main(folder, flip):  # images_dataset
    print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:
        print("Subdir: ", d)  # normal / sx_* / dx_*
        sub_dir = os.listdir(folder + d)
        for s in sub_dir:
            vid_path = right_slash(os.path.join(folder, d, s))
            print("\t Video folder path: ", vid_path)
            preprocess_frames(vid_path, flip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Preprocessing of the left frames.")

    parser.add_argument("--folder", dest="input",
                        default=cfg.DATASET_PATH,
                        help="Path of the folder containing normal and sx_*, dx_* subfolders")
    parser.add_argument("--flip", dest="flip",
                        default=0,
                        help="0 no flip, 1 if flip")
    args = parser.parse_args()
    main(folder=args.input, flip=int(args.flip))
