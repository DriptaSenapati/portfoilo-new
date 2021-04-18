FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get install python3-pip -y


COPY Flask /Flask/
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /Flask/

CMD ["gunicorn","-b","0.0.0.0:8000","run:app","--workers=3"]