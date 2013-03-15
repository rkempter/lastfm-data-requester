import csv
import json
import requests

api_key = '0a511e37bb65b2d607af9400908654b8'
parameters = {'method': 'chart.gettopartists', 'api_key': '0a511e37bb65b2d607af9400908654b8', 'format':'json'}
r = requests.get('http://ws.audioscrobbler.com/2.0/?', params=parameters)

data_json = r.text

data = json.loads(data_json)

with open('charts.csv', 'wb') as f:
    writer = csv.writer(f)
    for artist in data['artists']['artist']:
        writer.writerow([artist["name"],
                   artist["playcount"],
                   artist["listeners"]])
