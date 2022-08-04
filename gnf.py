import requests
import json

def greed_and_fear(daysback):
    value = []
    value_classification = []
    timestamp = []
    data = requests.get(f'https://api.alternative.me/fng/?limit={daysback}&date_format=world').json()

    for i in range(daysback):
            value.append(data['data'][i]['value'])
            value_classification.append(data['data'][i]['value_classification'])
            timestamp.append(data['data'][i]['timestamp'])
    return value, value_classification, timestamp


