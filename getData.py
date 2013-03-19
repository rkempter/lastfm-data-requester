import csv, codecs, cStringIO
import json
import requests

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

api_key = '0a511e37bb65b2d607af9400908654b8'
parameters = {'method': 'chart.gettopartists', 'api_key': '0a511e37bb65b2d607af9400908654b8', 'limit': '3000', 'format':'json'}
r = requests.get('http://ws.audioscrobbler.com/2.0/?', params=parameters)

data_json = r.text
data = json.loads(data_json)

artist_list = []

with open('charts_artists.csv', 'wb') as f:
    writer = UnicodeWriter(f)
    for artist in data['artists']['artist']:
        artist_list.append(artist["name"])
        writer.writerow([artist["name"],
                         artist["playcount"],
                         artist["listeners"]])

parameters = {'method': 'chart.getTopTracks', 'api_key': '0a511e37bb65b2d607af9400908654b8', 'limit': '3000', 'format':'json'}
r = requests.get('http://ws.audioscrobbler.com/2.0/?', params=parameters)

data_json = r.text
data = json.loads(data_json)

artists = {}

with open('charts_track.csv', 'wb') as f:
    writer = UnicodeWriter(f)
    for track in data['tracks']['track']:
        artist = track['artist']['name']
        if artist in artists:
            artists[artist] = artists[artist] + 1
        else:
            artists[artist] = 1
        writer.writerow([track["name"],
                         track["playcount"],
                         track["listeners"]])

# On how many artists the tracks are split?

print "The 1000 tracks are shared by " + repr(len(artists)) + " artists."

# how many of the top 1000 track artists are in the top 1000 artist list?

counter = 0

for i in range(0, len(artist_list)):
    if artist_list[i] in artists:
        counter = counter + 1

print "From the top 1000 track artists, " + repr(counter) + " are in the top 1000 artist list."


