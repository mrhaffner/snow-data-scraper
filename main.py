import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from dotenv import dotenv_values
config = dotenv_values(".env")

f = open('resorts.json')
data = json.load(f)

snow_data = {'data': []}

for key, val in data.items():
    page = requests.get(val)
    soup = BeautifulSoup(page.content, "html.parser")
    yesterday = soup.find_all('div', string=config['STRING'])
    parent = yesterday[0].parent

    snow = parent.find('div', config['SNOW']).text.strip().replace('"', '')

    date = parent.find('div', config['DATE']).text.strip()
    converted_date = str(datetime.strptime(date + ' 2021', '%b %d %Y')).split(" ")[0]

    current_date = datetime.today().strftime('%Y-%m-%d')
    snow_data['data'].append({
        'name': key,
        'snow': snow,
        'date_snowfall': converted_date,
        'date_collected': current_date
    })
    time.sleep(1)

print(snow_data)

#schedule this to run once per day
#probably want a header with security code
# r = requests.post(config['POST_URI'], data=json.dumps(snow_data))
# print(r.status_code, r.reason)
# print(r.text[:300] + '...')

f.close()