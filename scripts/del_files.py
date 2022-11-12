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

SUPPORT_EXTENSIONS = ['jpg', 'jpeg']

class SplitImages(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path

        self.do_del()

    def do_del(self):

        # run on all files in path
        counter = 0
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if os.path.exists(txt_file):
                        counter += 1

                        dont_del = False
                        with open(txt_file) as file:
                            Lines = file.readlines()

                            for line in Lines:
                                if int(line.split()[0]) != 7:
                                    print (line)
                                    dont_del = True
                                    break

                        if not dont_del:
                            print("{}deleting {}{}".format(TGREEN, txt_file, ENDC))
                            os.remove(img_file)
                            os.remove(txt_file)
                            pass



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "datasets-modified", "handicap_parking"))

    args = parser.parse_args()

    SplitImages(args.dataset_path)
