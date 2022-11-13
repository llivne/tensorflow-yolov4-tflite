import fiftyone as fo
import keyboard
import time


# split = "train" or "test" or "validation" or None for all
# classes=['Person',
#          'Dog',
#          'Cat',
#          'Raccoon',
#          'Squirrel',
#          'Bat (Animal)',
#          'Mouse',
#          'Bird',
#          'Owl',
#          'Snake'],


dataset = fo.zoo.load_zoo_dataset(
    "open-images-v6",
    split=None,
    label_types=["detections"],
    classes=["Mouse"],
    max_samples=10000,
)

# # load the images in gui
bla = input("Load GUI [y]: ")
if bla == "y":
    session = fo.launch_app(dataset)
    while True:
        print("To exit type q\n")
        keyboard.wait('q')
        keyboard.send('ctrl+6')
        time.sleep(0.025)
        break