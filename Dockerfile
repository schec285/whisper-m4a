FROM ubuntu:20.04
USER root

WORKDIR /workspace
COPY requirements.txt ${pwd}

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get dist-upgrade -y
RUN apt-get autoremove -y
RUN apt-get autoclean -y

# Python 3.10用のPPAを追加してインストール
RUN apt-get install -y gnupg2 curl
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install python3.10 -y
RUN apt-get update -y
# RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install vim -y
RUN apt-get remove python-pip
RUN apt-get install python3.10-distutils -y
RUN apt-get install -y ffmpeg
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install -r requirements.txt

# pythonコマンドの参照先をPython3.10に変更
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

CMD ["/bin/bash"]
