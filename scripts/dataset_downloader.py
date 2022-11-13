import fiftyone as fo
import keyboard
import time

dataset = fo.zoo.load_zoo_dataset(
    "open-images-v6",
    split="validation",
    label_types=["detections", "segmentations"],
    classes=["Cat", "Dog"],
    max_samples=2,
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