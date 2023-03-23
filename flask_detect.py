import os
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.config import cfg
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from PIL import Image
import cv2
import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession


DETECTIONS_PATH = os.environ.get('DETECTIONS_PATH', '/images_common/image_upload_folder/detections/')


physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


def parseFlags():
    flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                        'path to weights file')
    flags.DEFINE_integer('size', 416, 'resize images to')
    flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
    flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
    flags.DEFINE_list('images', './data/images/kite.jpg',
                      'path to input image')


def get_detections_data(boxes, scores, classes, valid_detections):
    dlen = valid_detections.numpy()[0]
    classes_list = []
    scores_list = []
    for i in range(dlen):
        classes_list.append(int(classes.numpy()[0][i]))
        scores_list.append(float(scores.numpy()[0][i]))

    return classes_list, scores_list


def run(imagePath, saved_model_loaded):
    size = 416
    tiny = False
    model = 'yolov4'
    images = imagePath
    output = DETECTIONS_PATH
    iou = 0.45
    score = 0.25
    dont_show = os.environ.get('DO_NOT_SHOW_IMAGE', 'True') == 'True'

    config = ConfigProto()
    config.gpu_options.allow_growth = True
    input_size = size
    images = images

    for count, image_path in enumerate(images, 1):
        print(f"PATH {image_path}")
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.

        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)

        infer = saved_model_loaded.signatures['serving_default']
        batch_data = tf.constant(images_data)
        pred_bbox = infer(batch_data)
        for key, value in pred_bbox.items():
            boxes = value[:, :, 0:4]
            pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=iou,
            score_threshold=score
        )

        if valid_detections.numpy()[0] == 0:
            return None, -1, set(), []

        pred_bbox = [boxes.numpy(), scores.numpy(), classes.numpy(), valid_detections.numpy()]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())

        # custom allowed classes (uncomment line below to allow detections for only people)
        # allowed_classes = ['person']

        image, class_ind, res_boxes = utils.draw_bbox(
            original_image, pred_bbox, allowed_classes=allowed_classes, show_label=False, no_actual_draw=True)

        image = Image.fromarray(image.astype(np.uint8))
        if not dont_show:
            image.show()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

        import os
        imageName = os.path.basename(image_path)
        imagePath = output + imageName
        cv2.imwrite(imagePath, image)

        classes_list, scores_list = get_detections_data(
            boxes, scores, classes, valid_detections)

        return imagePath, class_ind, classes_list, scores_list, res_boxes


if __name__ == '__main__':
    try:
        saved_model_loaded = tf.saved_model.load('./checkpoints/yolov4-416', tags=[tag_constants.SERVING])
        run(["test.jpg"], saved_model_loaded)
    except SystemExit:
        pass
