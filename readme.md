# Purchase-Amount-Forecasting

## Quick Run
First, host the server by running:
```
sh host_server.sh
```
Then, send request to obtain the forecasting results by running:
```
sh send_request.sh
```

The first command will build the docker image, and run the corresponding container as a server. The second command takes "data.csv" as input, send the data to the container server, and gives "data_forecast.csv" as output. The file "data_forecast.csv" has the same amount of rows with "data.csv", but the column "purchase_amount" is replaced with fitted (for the history) and forecasted (for the future) values.

## Folder Structure
.
├──analysis.ipynb                   The notebook for data analysis and algorithm prototype development.
├──host_server.sh                   The script to host server.
├──send_request.sh                  The script to send request to server to obtain forecast result.
├──data.csv                         Input data.
├──data_forecast.csv                Output data. (Obtained after executing send_request.sh)
├──send_requset.py                  The program to send client's request.
│
├──docker_server                    The server program, wrapped by docker.
│   ├──build_image.sh               Script for building the docker image.
│   ├─-Dockerfile                   Docker configuration file
│   ├──serve.py                     The program to run http server. 
│   ├──purchase_amount_forecasting  The package of purchase amount forecasting, which is implemented based on FBProphet.
