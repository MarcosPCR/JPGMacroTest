import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

key = 'chave'
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
id = 'CUUR0000SA0L1E'

payload = {
    "seriesid": [id],
    "startyear": "2018",
    "endyear": "2024",
    "registrationkey": key
}

response = requests.post(url, json=payload)
data = response.json()
result = []

for serie in data['Results']['series']:
    for item in serie['data']:
        date = f"{item['year']}-{item['period'][1:]}"
        value = float(item['value'])
        result.append((date, value))


df = pd.DataFrame(result, columns=['Date', 'CPI'])
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m')
df = df.sort_values(by='Date')
df['YoY_Percent_Change'] = df['CPI'].pct_change(periods=12) * 100

fig = px.line(df, x='Date', y='YoY_Percent_Change', title='Year-over-Year Percentage Change',
              labels={'YoY_Percent_Change': 'Year-over-Year Percentage Change', 'Date': 'Date'})

fig.update_layout(
    xaxis_title='Date',
    yaxis_title='%'+' change',
    template='plotly_dark'
)
fig.show()