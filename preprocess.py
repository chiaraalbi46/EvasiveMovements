import cv2
import os

SCALE_PERCENT = 12.5
ext = '.jpg'


def adjustImages(dir_video):
    image_path = dir_video + '/frames'
    output = dir_video + "/processed"

    if not os.path.exists(output):
        os.makedirs(output)

    for image in sorted(os.listdir(image_path)):
        print('Image: ' + image)
        if image.endswith(ext):
            img = cv2.imread(image_path + '/' + image)  # Returns matrix
            height = img.shape[0]  # Returns a tuple of the number of rows, columns, and channels
            width = img.shape[1]
            crop_img = img[60:-25, :, :]  # img[margin:-margin, margin:-margin]
            new_width = int(width * SCALE_PERCENT / 100)
            new_height = int(height * SCALE_PERCENT / 100)
            dim = (new_width, new_height)
            resized = cv2.resize(crop_img, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(os.path.join(output, image), resized)
