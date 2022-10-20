FROM mundialis/grass-py3-pdal:7.8.5-ubuntu

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update \
    && apt -y install nano \
    && apt-get -y install grass-dev

ENV LANG=C.UTF-8

RUN pip3 install --no-cache-dir -r requirements.txt

ENV mount /mnt

COPY . .

ENTRYPOINT  ["python3","-m", "main"]