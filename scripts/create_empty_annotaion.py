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
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        self.do_annotate()

    def do_annotate(self):
        # run on all files in path
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if not os.path.exists(txt_file):
                        print("{}creating empty annotation img file for: {}{}".format(TGREEN, file, ENDC))
                        open(txt_file, 'a').close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "train"))

    args = parser.parse_args()

    MoveBG(args.dataset_path)
