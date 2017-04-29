import csv
import pandas as pd
from geopy.geocoders import Nominatim
import re
import numpy as np
import math
import urllib.request as ul
from bs4 import BeautifulSoup
from geopy.exc import GeocoderTimedOut
import time
import requests
import io
from geopy.distance import great_circle

df = pd.read_csv('df_zipcode.csv')

### Subway stations within
url = 'https://raw.githubusercontent.com/jonthornton/MTAPI/master/data/stations.csv'
content = requests.get(url).content
stations = pd.read_csv(io.StringIO(s.decode('utf-8')))

def find_subway(lat, lon, stations):
    counter = 0
    for _, row in stations.iterrows():
        if great_circle((lat, lon), (row['lat'], row['lon'])).kilometers < 0.5:
            counter += 1
    return counter
df_merged['num_stations'] = df_merged.apply(lambda x:
    find_subway(x['latitude'], x['longitude'], stations), axis = 1)
# done with latitude and longitude


df_merged = df_merged.drop(['latitude','longitude'] , axis = 1)

### number of photos
df_merged['num_photos'] = df_merged['photos'].apply(len)
df_merged = df_merged.drop('photos', axis = 1)

### date created
df_merged['created'] = pd.to_datetime(df_merged['created'])
# df_merged['month'] = df_merged['created'].dt.month
df_merged['weekday'] = df_merged['created'].dt.weekday
df_merged['weekend'] = ((df_merged['weekday'] == 5) & (df_merged['weekday'] == 6))
df_merged['wd'] = ((df_merged['weekday'] != 5) & (df_merged['weekday'] != 6))
df_merged = df_merged.drop('weekday', axis = 1)
df_merged = df_merged.drop('created', axis = 1)


### text minning
# extract feature list from "features" column
df_features = df_merge['features'].tolist()
df_features = [item for sublist in df_features for item in sublist]
