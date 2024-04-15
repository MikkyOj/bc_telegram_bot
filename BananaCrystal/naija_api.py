import requests

with open("naija-api.txt") as file:
    url = file.read()

response = requests.get(url)
json = response.json()


if json['status'] == 'success':
    data = json['data']
    
    # Create dictionary
    exchange_rate = {entry['toCurrency']: float(entry['overrideRate']) for entry in data}
else:
    exchange_rate = {}