# https://machinelearningknowledge.ai/ways-to-convert-image-to-grayscale-in-python-using-skimage-pillow-and-opencv/

import argparse
import os
import cv2
import shutil

TGREEN =  '\033[32m'
TRED =  '\033[31m'
ENDC = '\033[m'

SUPPORT_EXTENSIONS = ['jpg', 'jpeg', 'png']

class Gray(object):
    def __init__(self, dataset_path, target_path):
        self.dataset_path = dataset_path
        self.target_path = target_path

        self.do_gray()

    def do_gray(self):
        # run on all files in path
        for root, dirs, files in os.walk(self.dataset_path):
            save_path = os.path.join(self.target_path, root.split("\\")[-1])
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for file in files:
                pre, ext = os.path.splitext(file)
                if ext[1:].lower() in SUPPORT_EXTENSIONS:
                    img_file = os.path.join(root, file)
                    txt_file = os.path.join(root, pre + ".txt")
                    print("{}creating gray img file: {}{}".format(TGREEN, file, ENDC))
                    img_gray=cv2.imread(img_file,0)
                    cv2.imwrite(os.path.join(save_path, 'gray-' + pre + ext), img_gray)
                    if os.path.exists(txt_file):
                        print("{}creating gray img annotation file: {}{}".format(TGREEN, file, ENDC))
                        shutil.copy(txt_file, os.path.join(save_path, 'gray-' + pre + ".txt"))


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "train"))
    # parser.add_argument('-t', '--target_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "gray-images", "warehouse"))
    #
    # args = parser.parse_args()
    #
    # Gray(args.dataset_path, args.target_path)

    Gray(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "crowdhuman-2"),
         os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "crowdhuman-gray"))
    # Gray(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "test"),
    #      os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "test-gray"))
    # Gray(os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "train"),
    #      os.path.join(os.getcwd(), "..", "..", "..", "fiftyone", "open-images-v6", "train-gray"))
