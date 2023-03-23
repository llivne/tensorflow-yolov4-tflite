import flask_detect
import os
import tensorflow as tf

from flask import Flask, flash, request, redirect, url_for, jsonify
from pathlib import Path
from tensorflow.python.saved_model import tag_constants


IMAGES_DIR = os.environ.get('IMAGES_DIR', '/images_common/image_upload_folder/')
DETECTIONS_PATH = os.environ.get('DETECTIONS_PATH', '/images_common/image_upload_folder/detections/')
Path(DETECTIONS_PATH).mkdir(parents=True, exist_ok=True)


app = Flask(__name__)

saved_model_loaded = tf.saved_model.load('./checkpoints/yolov4-416', tags=[tag_constants.SERVING])


@app.route('/detect', methods=['POST', 'GET'])
def do_detection():
    if request.method == 'POST':
        content = request.json
        file_path = content['file_path']
        file_name = os.path.basename(file_path)
        file_path = f'{IMAGES_DIR}/{file_name}'
        _, _, classes_list, scores_list, res_boxes = flask_detect.run([file_path], saved_model_loaded)
        return jsonify({"resp": "OK", "boxes": res_boxes, "clz_list": classes_list, "scores_list": scores_list}), 200
    if request.method == 'GET':
        return jsonify({"status": "detection server running"}), 200


if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=8888)
