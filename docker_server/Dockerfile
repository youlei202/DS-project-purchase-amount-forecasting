FROM ubuntu:16.04 as purchase-amount-forecasting

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get -y update && apt-get install -y python3.7 curl

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         python3-pip \
         python3-setuptools \
         python3.7-dev \
         build-essential \
         cmake \
         apt-utils \
         gcc-5 \ 
         g++-5 \
    && rm -rf /var/lib/apt/lists/*

RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --upgrade setuptools

RUN python3.7 -m pip install numpy \
        pandas==1.1.2 \ 
        scikit-learn \
        scipy 

COPY purchase_amount_forecasting /usr/local/lib/purchase_amount_forecasting
RUN python3.7 -m pip install -e /usr/local/lib/purchase_amount_forecasting

RUN mkdir /opt/program
COPY serve.py /opt/program
