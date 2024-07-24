import requests
import pandas as pd


API_KEY = 'chave'
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

ids = {
    "all" : "CUUR0000SA0",
    'less_food_energy': 'CUUR0000SA0L1E',
    'gasoline': 'CUUR0000SETB01',
}

payload = {
    "seriesid": list(ids.values()),
    "startyear": "2014",
    "endyear": "2023",
    "registrationkey": API_KEY
}

response = requests.post(url, json=payload)
data = response.json()
alldata = {}
for result in data['Results']['series']:
    series_id = result['seriesID']
    for key, value in ids.items():
        if series_id == value:
            series_name = key
    for item in result['data']:
        date = f"{item['year']}-{item['period'][1:]}"
        if date not in alldata:
            alldata[date] = {}
        alldata[date][series_name] = item['value']

df = pd.DataFrame.from_dict(alldata, orient='index')
df.to_csv('data_question1.csv', index_label='Date')