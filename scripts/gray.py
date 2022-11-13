# https://machinelearningknowledge.ai/ways-to-convert-image-to-grayscale-in-python-using-skimage-pillow-and-opencv/

import argparse
import os
import cv2
import shutil

TGREEN =  '\033[32m'
TRED =  '\033[31m'
ENDC = '\033[m'

SUPPORT_EXTENSIONS = ['jpg', 'jpeg', 'png']

class MoveBG(object):
    def __init__(self, dataset_path, target_path):
        self.dataset_path = dataset_path
        self.target_path = target_path

        self.do_gray()

    def do_gray(self):
        # create target directories if needed
        if not os.path.exists(os.path.join(self.target_path)):
            os.makedirs(os.path.join(self.target_path))

        # run on all files in path
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if not os.path.exists(txt_file):
                        print("{}creating gray img file without annotation: {}{}".format(TGREEN, file, ENDC))
                        img_gray=cv2.imread(img_file,0)
                        cv2.imwrite(os.path.join(self.target_path, 'gray-' + pre + ext), img_gray)
                    elif os.stat(txt_file).st_size == 0:
                        print("{}creating gray img file: {}{}".format(TGREEN, file, ENDC))
                        img_gray=cv2.imread(img_file,0)
                        cv2.imwrite(os.path.join(self.target_path, 'gray-' + pre + ext), img_gray)
                        shutil.copy(txt_file, os.path.join(self.target_path, 'gray-' + pre + ".txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "train"))
    parser.add_argument('-t', '--target_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "gray-images", "warehouse"))

    args = parser.parse_args()

    MoveBG(args.dataset_path, args.target_path)
