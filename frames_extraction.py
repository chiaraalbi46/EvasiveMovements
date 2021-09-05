import cv2
import os
# from preprocess import preprocess_frames

ext = '.png'
dir_name = os.path.dirname('sequences/')
count_len = len(os.listdir(dir_name))

for c in range(count_len):
    dir_video = os.path.dirname(dir_name + '/seq%d/' % (c + 1))
    vid_cap = cv2.VideoCapture(dir_video + '/sequenza%d.mp4' % (c + 1))
    count = 0
    dir_frames = os.path.join(dir_video, "frames")
    if not os.path.exists(dir_frames):
        os.mkdir(dir_frames)
    # print(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while vid_cap.isOpened():  # Returns true if video capturing has been initialized
        success, image = vid_cap.read()
        if success:
            cv2.imwrite(dir_frames + "/seq%dframe%d" % (c + 1, count) + ext, image)  # save frame as ext file
            count += 10
            vid_cap.set(1, count)
        else:
            vid_cap.release()
            break
    # preprocess_frames(dir_video)
