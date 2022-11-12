import argparse
import cv2
import json
import os
import sys

from PIL import Image
from decimal import *

TGREEN =  '\033[32m'
TRED =  '\033[31m'
ENDC = '\033[m'

SUPPORT_EXTENSIONS = ['jpg', 'jpeg', 'png']

class MoveBG(object):
    def __init__(self, dataset_path, target_path):
        self.dataset_path = dataset_path
        self.target_path = target_path

        self.do_move_bg()

    def do_move_bg(self):
        # create target directories if needed
        if not os.path.exists(os.path.join(self.target_path, 'bg')):
            os.makedirs(os.path.join(self.target_path, 'bg'))

        if not os.path.exists(os.path.join(self.target_path, 'not-labeled')):
            os.makedirs(os.path.join(self.target_path, 'not-labeled'))

        # run on all files in path
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if not os.path.exists(txt_file):
                        print("{}moving img file without annotation: {}{}".format(TGREEN, file, ENDC))
                        os.replace(img_file, os.path.join(self.target_path, 'not-labeled', file))
                    elif os.stat(txt_file).st_size == 0:
                        print("{}moving bg img file: {}{}".format(TGREEN, file, ENDC))
                        os.replace(img_file, os.path.join(self.target_path, 'bg', pre + ext))
                        os.replace(txt_file, os.path.join(self.target_path, 'bg', pre + ".txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "datasets", "cardboard_garbage_bags-new"))
    parser.add_argument('-t', '--target_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "datasets", "cardboard_garbage_bags-new"))

    args = parser.parse_args()

    MoveBG(args.dataset_path, args.target_path)
