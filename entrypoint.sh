#!/bin/sh

cp -r /root/_ssh /root/.ssh
cd detector_files
if [ -d "/detector_files/tensorflow-yolov4-tflite" ]; then
    echo "REPO EXISTS"
else
  echo "Cloning"
  git clone git@github.com:llivne/tensorflow-yolov4-tflite.git
fi

cd /detector_files/tensorflow-yolov4-tflite
git pull origin master
pip install -r requirements.txt

echo "ALL DONE"

exec "$@"   