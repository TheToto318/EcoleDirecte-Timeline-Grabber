FROM ubuntu:latest

RUN apt-get -y update 
RUN apt-get --assume-yes install python3-pip
RUN pip3 install requests datetime apscheduler
USER root
RUN cd /
RUN mkdir calendar

WORKDIR /
COPY timeline.py /

CMD ["python3.8", "./timeline.py"]