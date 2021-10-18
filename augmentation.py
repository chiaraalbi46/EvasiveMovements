from create_csv_file import right_slash

import os
import cv2
import argparse


def flip_image(path_frame):
   # path_frame = 'C:/Users/ninad/Desktop/video_guida/178/result/resultleft000090.png'
    img = cv2.imread(path_frame.strip(), -1)
    img_flip_lr = cv2.flip(img, 1)
    nf = path_frame.split('/')
    path_save = '/'.join(nf[:len(nf)-1]) + '/image_flip/'
    #print(path_save)
    if not os.path.exists(path_save):
        os.mkdir(path_save)
    image_path = path_save + 'flip_' + nf[len(nf)-1]
    cv2.imwrite(image_path, img_flip_lr)

# path = '/home/aivdepth/datasets/images_dataset'
# /home/aivdepth/datasets/images_dataset/sx_walk_sx/video270/left_frames

def dir_process(folder):

    print(folder)
    #print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:  # normal / sx_* / dx_*
        #print("Subdir: ", d)
        sub_dir = os.listdir(folder + d)

        for s in sub_dir:  # video*
            path_dir_frame  = folder + d + '/' + s + '/left_frames/'
            #print("\t json folder: ", path_frame)
            ssub_dir = os.listdir(path_dir_frame)
            for l in ssub_dir:
                path_frame = path_dir_frame + l
                flip_image(path_frame)
                #print(path_frame)

def main():
    parser = argparse.ArgumentParser(description="Image augmentation: flipping the image vertically")
    parser.add_argument("--folder_path", dest="folder_p", default=None, help="Path of the dataset")

    args = parser.parse_args()
    dir_process(folder=args.folder_p)


if __name__ == "__main__":
    main()
    # folder = 'C:/Users/ninad/Desktop/frame_dataset/datasets/images_dataset/'
    # dir_process(folder)
