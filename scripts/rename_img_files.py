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

class RenameFiles(object):
    def __init__(self, dataset_path, target_path, number):
        self.dataset_path = dataset_path
        self.target_path = target_path
        self.number = number

        self.do_rename()

    def do_rename(self):
        # create target directories if needed
        if not os.path.exists(self.target_path):
            os.makedirs(self.target_path)

        # run on all files in path
        number = self.number
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    # rename jpeg to jpg because training need jpg NOT jpeg
                    if ext.lower() == ".jpeg":
                        ext = ".jpg"

                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    print("{}moving img file: {}{}".format(TGREEN, file, ENDC))
                    os.replace(img_file, os.path.join(self.target_path, self.dataset_path.split("\\")[-1] + "_" + str(number) + ext))
                    if os.path.exists(txt_file):
                        os.replace(txt_file, os.path.join(self.target_path, self.dataset_path.split("\\")[-1] + "_" + str(number) + ".txt"))
                    number += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "datasets-modified", "green_waste"))
    parser.add_argument('-t', '--target_path', help='Path to the dataset target directory', default=os.path.join(os.getcwd(), "..", "datasets-modified", "sewage"))
    parser.add_argument('-n', '--number', help='Start number', default=1)

    args = parser.parse_args()

    RenameFiles(args.dataset_path, args.target_path, args.number)
