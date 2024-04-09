FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt install  openssh-server sudo -y
RUN apt-get update \
      && apt-get install --no-install-recommends --no-install-suggests -y gnupg2 ca-certificates \
            git build-essential ffmpeg libsm6 libxext6  \
      && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get upgrade -y

RUN apt-get install -y libmagic-dev
RUN apt-get install -y openssh-server
RUN apt-get install  -y python3-pip
RUN apt-get install  -y vim

ARG SOURCE_BRANCH=master
ENV SOURCE_BRANCH $SOURCE_BRANCH

COPY . /detector_files/

# install requirements so it will be part of the image and speed up container reloading. if the requirements changes only the changes will be install as part of the entrypoint.sh script.
RUN pip install -r /detector_files/requirements.txt

COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]