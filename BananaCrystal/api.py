import requests

with open("api.txt") as file:
    url = file.read()

response = requests.get(url)
json = response.json()

if json['status'] == 'success':
    data = json['data']
    
    # Create dictionary
    exchange_rates = {entry['code']: float(entry['rateToUsd']) for entry in data}
else:
    exchange_rates = {}

