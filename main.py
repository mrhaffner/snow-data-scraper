import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from dotenv import dotenv_values
config = dotenv_values(".env")

#once daily (can serve to wake up java api as well)
#loop over list of resorts
    #get snow, and date reported
    #add slug, snow, date reported and current date (date collected) to object
        #jsonify object, send to java api

f = open('resorts.json')
data = json.load(f)

snow_data = {}

for key, val in data.items():
    page = requests.get(val)
    soup = BeautifulSoup(page.content, "html.parser")
    yesterday = soup.find_all('div', string=config['STRING'])
    parent = yesterday[0].parent

    snow = parent.find('div', config['SNOW']).text.strip().replace('\"', '')

    date = parent.find('div', config['DATE']).text.strip()
    converted_date = str(datetime.strptime(date + ' 2021', '%b %d %Y')).split(" ")[0]

    current_date = datetime.today().strftime('%Y-%m-%d')
    snow_data[key] = {
        'snow': snow,
        'date_reported': converted_date,
        'date_collected': current_date
    }
    time.sleep(1) 
print(snow_data)

f.close()