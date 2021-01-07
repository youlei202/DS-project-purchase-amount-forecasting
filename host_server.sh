#!/usr/bin/env bash

# build docker image
cd docker_server
sh build_image.sh

# run container
cd ..
docker run -t -p 9998:9998 purchase-amount-forecasting python3.7 /opt/program/serve.py

# send request to docker server
python send_request.py -i data.csv -o data_forecast.csv -u http://localhost:9998
