FROM ubuntu:20.04
USER root

WORKDIR /workspace
COPY requirements.txt ${pwd}

ENV TZ=Asia/Tokyo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \

    apt-get update -y && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \

# Python 3.10用のPPAを追加してインストール
    apt-get install -y gnupg2 curl && \
    apt-get install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa -y && \

    apt-get install python3.10 -y && \
    apt-get update -y && \
    apt-get install vim -y && \
    apt-get remove python-pip && \
    apt-get install python3.10-distutils -y && \
    apt-get update && \
    apt-get install -y ffmpeg && \
    
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10 && \
    pip install -r requirements.txt && \

# pythonコマンドの参照先をPython3.10に変更
    update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

CMD ["/bin/bash"]
