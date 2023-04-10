import flask_detect
import gdown
import os
import tensorflow as tf

from flask import Flask, flash, request, redirect, url_for, jsonify
from pathlib import Path
from tensorflow.python.saved_model import tag_constants


app = Flask(__name__)

# download model if it's not located in the model folder
if not os.path.exists('./checkpoints/yolov4-416'):
    url = "https://drive.google.com/drive/folders/1Kpcsza2ray22Y2RkT9ehcYHLNI4jZuwH"
    gdown.download_folder(url, output='./checkpoints/yolov4-416', quiet=True, use_cookies=False)

saved_model_loaded = tf.saved_model.load('./checkpoints/yolov4-416', tags=[tag_constants.SERVING])


@app.route('/detect', methods=['POST', 'GET'])
def do_detection():
    '''
    perform inference for a single image.
    :return:
    '''
    if request.method == 'POST':
        content = request.json
        file_path = content['file_path']
        # file_name = os.path.basename(file_path)
        # file_path = f'{IMAGES_DIR}/{file_name}'
        response = flask_detect.run([file_path], saved_model_loaded, save_labeled_img=True) # save_labeled_img is for debugging only. remove in prod
        if len(response) > 0:
            _, _, classes_list, scores_list, res_boxes = response[0]
            return jsonify({"resp": "OK", "boxes": res_boxes, "clz_list": classes_list, "scores_list": scores_list}), 200
        else:
            return jsonify({"resp": "NO_DETECTION", "boxes": [], "clz_list": [], "scores_list": []}), 200
    if request.method == 'GET':
        return jsonify({"status": "detection server running"}), 200


if __name__ == "__main__":
    # Quick test configuration. Please use proper Flask configuration options
    # in production settings, and use a separate file or environment variables
    # to manage the secret key!
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=8888)