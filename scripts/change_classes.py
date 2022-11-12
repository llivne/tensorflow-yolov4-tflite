import argparse
import os

TGREEN =  '\033[32m'
TRED =  '\033[31m'
ENDC = '\033[m'

class ChangeClass(object):
    def __init__(self, dataset_path, class_number, original_class, remove):
        self.dataset_path = dataset_path
        self.class_number = class_number
        self.original_class = original_class
        self.remove = remove

        self.do_convert()

    def do_convert(self):
        # run on all files in path
        for root, dirs, files in os.walk(self.dataset_path):
            for file in files:
                if file.endswith(".txt"):
                    txt_file = os.path.join(root, file)
                    print("{}Parsing {}{}".format(TGREEN, txt_file, ENDC))
                    self.ParseTxt(txt_file, root)

    def ParseTxt(self, txt_file, dir_path):
        new_annotation = ""
        with open(txt_file) as file:
            Lines = file.readlines()

            for line in Lines:
                splitted_line = line.split()
                if splitted_line[0] == self.original_class:
                    if not self.remove:
                        splitted_line[0] = self.class_number
                        new_annotation += line[:0] + ' '.join(splitted_line) + '\n'
                        print("{}Changing annotation in file {}{}".format(TRED, txt_file, ENDC))
                    else:
                        print(f'removing this line {splitted_line}')
                else:
                    new_annotation += line


                # splitted_line = line.split()
                # splitted_line[0] = str(int(splitted_line[0]) + 6)
                # new_annotation += line[:0] + ' '.join(splitted_line) + '\n'

                # test we dont have class above the max classes
                # if int(line.split()[0]) > 10:
                #     print (f"wrong labling: {line}")

        with open(txt_file, 'w') as outFile:
            outFile.write(new_annotation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--dataset_path', help='Path to the dataset root directory', default=os.path.join(os.getcwd(), "datasets", "cardboard_garbage_bags_and_containers", "data", "labels"))
    parser.add_argument('-n', '--class_number', help='the new class number', default="5")
    parser.add_argument('-o', '--original_class', help='the original class number', default="0")
    parser.add_argument('-r', '--remove', help='remove class from file', action="store_true")

    args = parser.parse_args()

    ChangeClass(args.dataset_path, args.class_number, args.original_class, args.remove)
