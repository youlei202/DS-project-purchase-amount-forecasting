import socket
import sys
import threading
import json

import numpy as np
import pandas as pd

import paf.model as pafm

VIRTUAL_IP = '0.0.0.0'
PORT = 9998

def recvall(sock: socket.socket):
    BUFF_SIZE = 4096 * 1024 # 4 MiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data


def forecast(df: pd.DataFrame):
    # train/test split
    train_test_split_date = df[df.purchase_amount.notnull()]['date'].max()
    train_ = df[df.date <= train_test_split_date]
    test_  = df[df.date > train_test_split_date]
    train = train_.rename(columns={'date':'ds', 'purchase_amount':'y'})
    test  = test_.rename(columns={'date':'ds', 'purchase_amount':'y'})

    # fit model
    training_results, params_set, m = pafm.ForecastingModel().fit(train)

    # make forecasting
    future_months = len(test)
    future = m.make_future_dataframe(periods=future_months, freq='m')
    forecast = m.predict(future)

    data_forecast = forecast[['ds','yhat']].rename(columns={'ds':'date', 'yhat':'purchase_amount'})

    return data_forecast



if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((VIRTUAL_IP, PORT))
    s.listen(5)

    print('Waiting for connection...')
    while True:

        # listening
        sock, addr=s.accept()

        # handle request
        data_recv = recvall(sock)
        data_json = data_recv.decode('utf-8').split('\n')[-1]
        df = pd.read_json(data_json)

        df_forecast = forecast(df)

        # send result back
        response_body = df_forecast.to_json()
        response_line = "HTTP/1.1 200 OK\r\n"
        response_header = "Server: Python-server\r\n"
        response_data = response_line + response_header + "\r\n" + response_body
        sock.send(bytes(response_data, encoding='utf-8'))

        # close connection
        sock.close()
        print('Connection from {}:{} closed.'.format(addr[0], addr[1]))
