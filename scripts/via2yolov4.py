# downloaded from https://github.com/mjhassan/VIA-to-YOLO-annotation-converter
# How to use:
# - Export VIA annotations as json, into the images directory. It will save as via_region_data.json.
# - Download and copy this script into that directory.
# - Create a text file with all the attributes are used in VIA annotations; let's call it via.names.
# - Run the following command: python via2dark.py via_region_data.json via.names

# info about yolo annotation:
# https://towardsdatascience.com/image-data-labelling-and-annotation-everything-you-need-to-know-86ede6c684b1
# https://cloudxlab.com/blog/label-custom-images-for-yolo/
# https://github.com/AlexeyAB/Yolo_mark/issues/60

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

class ViaToDart(object):
    def __init__(self, dataset_path, names_path):
        self.dataset_path = dataset_path
        self.names_path = names_path

        self.do_convert()

    def do_convert(self):
        # load the names for the classes
        names = open(self.names_path).read().split('\n')

        # run on all json files in path
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith(".json"):
                    json_file = os.path.join(root, file)
                    print("{}Parsing {}{}".format(TGREEN, json_file, ENDC))
                    self.ParseJson(json_file, root, names)

    def ParseJson(self, json_file, dir_path, names):
        with open(json_file) as file:
            via_dict = json.load(file)

            images_data = via_dict["_via_img_metadata"]
            for img in images_data:
                data = images_data[img]
                imageName = data['filename']
                filename = imageName.rsplit('.', 1)[0]
                regions = data['regions']
                try:
                    img = Image.open(os.path.join(dir_path, imageName))
                    print("Converting img{}".format(imageName))
                except IOError:
                    print("{}{} No such file {}{}".format(TRED, sys.stderr,imageName, ENDC))
                    continue

                content = ""
                for region in regions:
                    obj_class = self.get_object_class(region, imageName, names)
                    annotation = self.get_yolo_annotation(region, os.path.join(dir_path, imageName))
                    if annotation:
                        if content:
                            content += "\n{} {}".format(obj_class, annotation)
                        else:
                            content += "{} {}".format(obj_class, annotation)

                with open("{}.txt".format(os.path.join(dir_path, filename)), "w") as outFile:
                    outFile.write(content)

    def get_object_class(self, region, file, names):
        # todo [liran] - we dont have label on the trash dataset so just return trash
        # try:
        #     for attribute in region['region_attributes']:
        #         annotation = region['region_attributes'][attribute]
        # except KeyError:
        #     print >> sys.stderr, "annotation info is missing in ", file

        annotation = "waste"

        index = [item.lower() for item in names].index(annotation.lower())
        return index

    def get_yolo_annotation(self, region, img_path):
        x_min = min(region['shape_attributes']['all_points_x'])
        y_min = min(region['shape_attributes']['all_points_y'])
        x_max = max(region['shape_attributes']['all_points_x'])
        y_max = max(region['shape_attributes']['all_points_y'])

        image = cv2.imread(img_path)

        coords = [x_min, y_min, x_max, y_max]
        coords[2] -= coords[0]
        coords[3] -= coords[1]
        x_diff = int(coords[2]/2)
        y_diff = int(coords[3]/2)
        coords[0] = coords[0]+x_diff
        coords[1] = coords[1]+y_diff
        coords[0] /= int(image.shape[1])
        coords[1] /= int(image.shape[0])
        coords[2] /= int(image.shape[1])
        coords[3] /= int(image.shape[0])
        return "{} {} {} {}".format(str(coords[0]), str(coords[1]), str(coords[2]), str(coords[3]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "datasets"))
    parser.add_argument('-f', '--names_path', help='Path to classes names file', default=os.path.join(os.getcwd(), "datasets", "cthal.names"))

    args = parser.parse_args()

    ViaToDart(args.dataset_path, args.names_path)
