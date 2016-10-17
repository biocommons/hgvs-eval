FROM python:2.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


ADD .  /usr/src/app/

# PROTOBUF
RUN apt-get update
RUN apt-get install -y autoconf automake libtool curl make g++ unzip vim


RUN pip install pip --upgrade

RUN mkdir $HOME/.python-eggs \
  && chmod og-w $HOME/.python-eggs \
  && pip install ipython \
  && pip install pdb

RUN pip install bokeh \
  && pip install pandas \
  && pip install jupyter


# untested ... yet
RUN pip install protobuf
RUN wget https://github.com/google/protobuf/releases/download/v3.1.0/protoc-3.1.0-linux-x86_64.zip
RUN unzip  protoc-3.1.0-linux-x86_64.zip
# now add ./bin to your path
