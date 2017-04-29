import json
import pandas as pd
from geopy.geocoders import Nominatim
import re
from geopy.exc import GeocoderTimedOut
import time

### loading data from train.json
df = pd.read_json('train.json')
# list(df)
# df_manager = (df.groupby(['manager_id'], as_index = False).size()/len(df)).reset_index()
# df_manager.columns = ['manager_id', 'manager_pct']
# df_merge = pd.merge(df, df_manager, on = 'manager_id', how = 'inner')
# col_to_drop = ['display_address']
df = df[['listing_id', 'latitude', 'longitude']]

### convert address to zipcode then to neighborhood
geolocator = Nominatim()
reg = re.compile('^.*(?P<zipcode>\d{5}).*$')

def convert_to_zipcode(lat, lon, recursion = 0):
    coordinate = str(lat) + ', ' + str(lon)
    try:
        location = geolocator.reverse(coordinate, timeout=None)
        match = reg.match(location.address.strip())
        return match.groupdict()['zipcode']
    except GeocoderTimedOut as e:
        if recursion > 10:      # max recursions
            raise e
        time.sleep(1) # wait a bit
        # try again
        return convert_to_zipcode(lat, lon, recursion=recursion + 1)

df['zip_code'] = df.apply(lambda x: convert_to_zipcode(x['latitude'], x['longitude']), axis=1)

### save intermediate results
df[['listing_id', 'zip_code']].to_csv('zipcode_lookup.csv')
