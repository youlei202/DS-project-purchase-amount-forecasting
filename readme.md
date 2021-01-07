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


