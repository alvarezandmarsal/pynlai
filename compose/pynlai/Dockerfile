
FROM debian:latest
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV TERM xterm

# update, upgrade, and install packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y apt-utils \
    && apt-get install -y curl git less man nano sudo wget \
    && apt-get install -y build-essential \
    && apt-get install -y python python-dev python3 python3-dev \
    && apt-get install -y libssl-dev libffi-dev

# configure apt-utils (fixes warnings)
RUN dpkg-reconfigure apt-utils

# set some useful defaults
RUN echo "alias ls='ls --color'" >> /etc/bash.bashrc
RUN echo "alias grep='grep --color=auto'" >> /etc/bash.bashrc

# download get-pip and install for python 2.x and 3.x
RUN wget -P /tmp https://bootstrap.pypa.io/get-pip.py
RUN python /tmp/get-pip.py
RUN python3 /tmp/get-pip.py

# install ipython for python 2.x and 3.x
RUN python -m pip install ipython
RUN python3 -m pip install ipython

# install requirements for python 2.x and 3.x
COPY ./requirements /requirements
RUN python -m pip install -r /requirements/base.txt
RUN python3 -m pip install -r /requirements/base.txt

WORKDIR /app
