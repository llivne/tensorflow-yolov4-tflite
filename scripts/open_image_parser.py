import argparse
import csv
import itertools
import os
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
           'bird',
           'owl',
           'snake']

class CreateAnnotation(object):
    def __init__(self, dataset_path):
        print(f"Doing annotation for {dataset_path}")

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
        # open the csv label file only once, we will slice it during the run because it is huge
        with open(os.path.join(self.dataset_path, "labels", "detections.csv")) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            sliced_csv_reader = itertools.islice(csv_reader, 0, None)
            line_num = 0
            total_line = 0

            # run on all files in path
            for root, dirs, files in os.walk(os.path.join(self.dataset_path, "data")):
                sliced_csv_reader = itertools.islice(sliced_csv_reader, line_num, None)

                for file in files:
                    pre, ext = os.path.splitext(file)
                    if ext[1:].lower() in SUPPORT_EXTENSIONS:
                        img_file = os.path.join(root, file)
                        txt_file = os.path.join(root, pre + ".txt")
                        if not os.path.exists(txt_file):

                            # call create_anotation()
                            line_num = self.create_annotation(txt_file, pre, sliced_csv_reader)
                            total_line += line_num

                            # if we get error then reset the csv and retry.
                            if line_num == 0:
                                csv_file.seek(0)
                                csv_reader = csv.reader(csv_file, delimiter=',')
                                if total_line > 1000:
                                    total_line -= 1000
                                else:
                                    total_line = 0
                                sliced_csv_reader = itertools.islice(csv_reader, total_line, None)
                                print("retrying...")
                                self.create_annotation(txt_file, pre, sliced_csv_reader)

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

    def create_annotation(self, txt_file, file_name, sliced_csv_reader):
        content = ""
        line_num = 0
        start = time.time()

        for row in sliced_csv_reader:

            # for large dataset we get stuck. monkypatch to reset
            if time.time() - start > 2:
                content = ""
                break

            if row[0] == file_name:
                if row[2] in self.classes_label:
                    obj_class = self.classes_label.index(row[2])
                    annotation = self.get_yolo_annotation(row)
                    if annotation:
                        if content:
                            content += "\n{} {}".format(obj_class, annotation)
                        else:
                            content += "{} {}".format(obj_class, annotation)

            # if we found the image_filename then once we finish running on it we can quit because all of the other records are not relevant
            elif content != "":
                with open(txt_file, "w") as outFile:
                    outFile.write(content)
                break

            line_num += 1

        if content == "":
            print("{}failed to create annotation for: {}{}".format(TRED, file_name, ENDC))
            return 0
        else:
            print("{}created annotation img file for: {}{}".format(TGREEN, file_name, ENDC))
            return line_num

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "data"))
    #
    # args = parser.parse_args()
    #
    # CreateAnnotation(args.dataset_path)

    # CreateAnnotation(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "validation"))
    # CreateAnnotation(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "test"))
    CreateAnnotation(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "train"))
