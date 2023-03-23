#!/bin/sh

# todo [liran] - remove this. git clone check if folder exists before clonning. I use https so no need to ssh
#cp -r /root/_ssh /root/.ssh
#cd detector_files
#if [ -d "/detector_files/tensorflow-yolov4-tflite" ]; then
#    echo "REPO EXISTS"
#else
#  echo "Cloning"
#  git clone https://github.com/llivne/tensorflow-yolov4-tflite.git
#fi

echo "Cloning"
git clone https://github.com/llivne/tensorflow-yolov4-tflite.git

cd /detector_files/tensorflow-yolov4-tflite
git pull origin master
pip install -r requirements.txt

echo "ALL DONE"

exec "$@"   