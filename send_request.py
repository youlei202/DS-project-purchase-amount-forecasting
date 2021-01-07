import requests
import json
import pandas as pd
import argparse

if __name__ == "__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument("--input-data", "-i", required=True)
    argparser.add_argument("--output-data", "-o", required=True)
    argparser.add_argument("--url", "-u", required=True)
    args = argparser.parse_args()

    # read data
    df = pd.read_csv(args.input_data, sep=';', parse_dates=['date'])
    print('Data {} has been read'.format(args.input_data))

    # send request to server
    print('Request sent to server, waiting for response... ')
    message = df.to_json()
    r = requests.post(args.url, json=json.loads(message))
    r_json = json.loads(r.content)
    data_forecast = pd.read_json(r.content.decode('utf-8'))

    # save forecasting result
    data_forecast.to_csv(args.output_data, index=False, sep=';')
    print('File {} has been generated'.format(args.output_data))
