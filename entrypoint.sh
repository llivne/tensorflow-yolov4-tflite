#!/bin/sh

echo "Cloning"
cd /detector_files
git clone https://github.com/llivne/tensorflow-yolov4-tflite.git

cd /detector_files/tensorflow-yolov4-tflite
git pull origin master
pip install -r requirements.txt

echo "ALL DONE"

exec "$@"   