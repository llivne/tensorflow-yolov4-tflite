import csv
import argparse
import os
import cv2
import shutil
import time


TGREEN =  '\033[32m'
TRED =  '\033[31m'
ENDC = '\033[m'

SUPPORT_EXTENSIONS = ['jpg', 'jpeg', 'png']

CLASSES = ['person',
           'dog',
           'cat',
           'raccoon',
           'squirrel',
           'bat (animal)',
           'mouse',
           'Bird',
           'owl',
           'snake']

class CreateAnnotation(object):
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.classes_label = self.get_classes_labels()

        self.do_annotate()

    def get_classes_labels(self):
        classes_labels = [None] * len(CLASSES)

        with open(os.path.join(self.dataset_path, "metadata", "classes.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[1].lower() in CLASSES:
                    classes_labels[CLASSES.index(row[1].lower())] = row[0]

        print ("this is the classes we are going to work on:")
        for count, value in enumerate(CLASSES):
            print (f"{value}: {classes_labels[count]}")

        time.sleep(1)
        return classes_labels

    def do_annotate(self):
        # run on all files in path
        for root, dirs, files in os.walk(os.path.join(self.dataset_path, "data")):
            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    if not os.path.exists(txt_file):
                        print("{}creating annotation img file for: {}{}".format(TGREEN, file, ENDC))
                        self.create_annotation(txt_file, pre, img_file)

    def get_yolo_annotation(self, row):
        x_min = float(row[4])
        y_min = float(row[6])
        x_max = float(row[5])
        y_max = float(row[7])

        coords = [x_min, y_min, x_max, y_max]

        coords[0] = str(round((x_max+x_min)/2, 6))
        coords[1] = str(round((y_max+y_min)/2, 6))
        coords[2] = str(round(x_max-x_min, 6))
        coords[3] = str(round(y_max-y_min, 6))

        return "{} {} {} {}".format(str(coords[0]), str(coords[1]), str(coords[2]), str(coords[3]))

    # def get_yolo_annotation_old_not_good(self, row, img_path):
    #     x_min = float(row[4]) * 1000
    #     y_min = float(row[6]) * 1000
    #     x_max = float(row[5]) * 1000
    #     y_max = float(row[7]) * 1000
    #
    #     image = cv2.imread(img_path)
    #
    #     coords = [x_min, y_min, x_max, y_max]
    #     coords[2] -= coords[0]
    #     coords[3] -= coords[1]
    #     x_diff = int(coords[2]/2)
    #     y_diff = int(coords[3]/2)
    #     coords[0] = coords[0]+x_diff
    #     coords[1] = coords[1]+y_diff
    #     coords[0] /= int(image.shape[1])
    #     coords[1] /= int(image.shape[0])
    #     coords[2] /= int(image.shape[1])
    #     coords[3] /= int(image.shape[0])
    #     return "{} {} {} {}".format(str(coords[0]), str(coords[1]), str(coords[2]), str(coords[3]))

    def create_annotation(self, txt_file, file_name, img_file):
        content = ""

        with open(os.path.join(self.dataset_path, "labels", "detections.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    # skip first title line
                    line_count += 1
                else:
                    if row[0] == file_name:
                        if row[2] in self.classes_label:
                            obj_class = self.classes_label.index(row[2])
                            annotation = self.get_yolo_annotation(row, img_file)
                            if annotation:
                                if content:
                                    content += "\n{} {}".format(obj_class, annotation)
                                else:
                                    content += "{} {}".format(obj_class, annotation)
                    line_count += 1

            if content != "":
                with open(txt_file, "w") as outFile:
                    outFile.write(content)
            else:
                print("{}creating No annotation were found for: {}. no file was created{}".format(TRED, file_name, ENDC))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "validation"))

    args = parser.parse_args()

    CreateAnnotation(args.dataset_path)