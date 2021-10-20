from create_csv_file import right_slash

import os
import cv2
import argparse
import json
from net_utilities import write_json


def flip_image(path_frame):
    img = cv2.imread(path_frame.strip(), -1)
    img_flip_lr = cv2.flip(img, 1)
    nf = path_frame.split('/')
    path_save = '/'.join(nf[:len(nf)-1]) + '_flip/'
    #print('\f path_save', path_save)
    if not os.path.exists(path_save):
        os.mkdir(path_save)
    #image_path = path_save + 'flip_' + nf[len(nf)-1] #todo filp si o no nel nome dell'immagine
    image_path = path_save + nf[len(nf) - 1]
    print('\f image_path: ', image_path)
    cv2.imwrite(image_path, img_flip_lr)

# path = '/home/aivdepth/datasets/images_dataset'
# /home/aivdepth/datasets/images_dataset/sx_walk_sx/video270/left_frames


#/home/aivdepth/datasets/images_dataset/sx_walk_sx/video270/video270_traj.json
def create_json(path_json):
    with open(path_json) as json_file:
        d = json.load(json_file)

        for i in range(len(d)):
            for j in range(len(d[i]['Past'])):
                d[i]['Past'][j][0] = -1*d[i]['Past'][j][0]
            for j in range(len(d[i]['Future'])):
                d[i]['Future'][j][0] = -1*d[i]['Future'][j][0]
            #print(d[i]['Past'][0][0])

    ap = path_json.split('/')

    name_json = ap[len(ap)-1].split('.')[0] +'_flip.json'
    #print(name_json)
    path_save = '/'.join(path_json.split('/')[:len(ap) - 1]) + '/' + name_json
    write_json(d, path_save)


def dir_process(folder, vid_name):

    print(folder)
    #print(os.listdir(folder))
    dirs = os.listdir(folder)
    for d in dirs:  # normal / sx_* / dx_*
        #print("Subdir: ", d)
        sub_dir = os.listdir(folder + d)

        for s in sub_dir:  # video*
            path_dir_frame = folder + d + '/' + s + '/left_frames/'
            #TODO rivedere nome : o passi elementi in input o scrivi manualmente
            path_json = folder + d + '/' + s + '/' + s + '/' + vid_name + '_traj.json'
            create_json(path_json)
            print("\t folder: ", folder + d + '/' + s )
            ssub_dir = os.listdir(path_dir_frame)

            for l in ssub_dir:  # frame*
                path_frame = path_dir_frame + l
                flip_image(path_frame)
                #print(path_frame)


def main():
    parser = argparse.ArgumentParser(description="Image augmentation: flipping the image vertically")
    parser.add_argument("--folder_path", dest="folder_p", default=None, help="Path of the dataset")
    parser.add_argument("--vid_name", dest="vid_name", default=None,
                        help="Name of json file with origin_distance and future points")

    args = parser.parse_args()
    dir_process(folder=args.folder_p, vid_name=args.vid_name)


if __name__ == "__main__":
#    # create_json()
     main()
#     folder = 'C:/Users/ninad/Desktop/frame_dataset/datasets/images_dataset/'
#     dir_process(folder)
