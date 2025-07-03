FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ffmpeg git curl python3 python3-pip
RUN pip3 install torch transformers musicnn librosa==0.10.1 ffmpeg-python cryptography

CMD ["bash", "entrypoint.sh"]
