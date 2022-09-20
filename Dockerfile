FROM mundialis/grass-py3-pdal:stable-ubuntu

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update \
    && apt -y install nano
#     && apt -y install python3-pip
#     && apt -y install libgeos-dev \
#     && apt -y install gdal-bin python3-gdal

# RUN apt -y install libexpat1

ENV LANG=C.UTF-8

RUN pip3 install --no-cache-dir -r requirements.txt

ENV mount /mnt

COPY . .


ENTRYPOINT  ["python3","-m", "main"]

# CMD  ["python", "main.py"]