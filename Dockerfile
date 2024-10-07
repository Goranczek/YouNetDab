# Dockerfile, Image, Container

FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3 -y

WORKDIR **PATH**

COPY ./Connectors ./Connectors
COPY ./Databases ./Databases

ADD main.py .
ADD downloader.py .
ADD gui.py .
ADD requirements.txt .
ADD config.cfg .

RUN python3 --version
RUN python3 -m pip install -r requirements.txt

CMD ["python", "./main.py"]
