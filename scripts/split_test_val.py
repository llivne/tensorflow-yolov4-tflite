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

class SplitImages(object):
    def __init__(self, dataset_path, target_path):
        self.dataset_path = dataset_path
        self.target_path = target_path

        self.do_split()

    def do_split(self):
        # create target directories if needed
        if not os.path.exists(os.path.join(self.target_path, 'train')):
            os.makedirs(os.path.join(self.target_path, 'train'))

        if not os.path.exists(os.path.join(self.target_path, 'validation')):
            os.makedirs(os.path.join(self.target_path, 'validation'))

        # run on all files in path
        counter = 0
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if os.path.exists(txt_file):
                        print("{}moving {}{}".format(TGREEN, txt_file, ENDC))
                        counter += 1
                        if counter % 5:
                            os.replace(img_file, os.path.join(self.target_path, 'train', pre + ext))
                            os.replace(txt_file, os.path.join(self.target_path, 'train', pre + ".txt"))
                        else:
                            os.replace(img_file, os.path.join(self.target_path, 'validation', pre + ext))
                            os.replace(txt_file, os.path.join(self.target_path, 'validation', pre + ".txt"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "datasets-modified", "handicap_parking"))
    parser.add_argument('-t', '--target_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "datasets-modified", "cars_spiltted"))

    args = parser.parse_args()

    SplitImages(args.dataset_path, args.target_path)
