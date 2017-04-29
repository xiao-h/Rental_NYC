
import shapefile
import pandas as pd

df = pd.read_json('train.json')
df = df[['listing_id', 'latitude', 'longitude']].set_index('listing_id').T.to_dict('list')

reader = shapefile.Reader('ZillowNeighborhoods-NY.shp')
# print dict((d[0],d[1:]) for d in reader.fields[1:])
fields = [field[0] for field in reader.fields[1:]]
geoms_nyc = {} # dictionary of neighborhood and list of coordinates
for feature in reader.shapeRecords():
    atr = dict(zip(fields, feature.record))
    if (atr['County'] in ['New York','Kings','Queens']): # 170 records
        geom = feature.shape.__geo_interface__
        geoms_nyc[atr['Name']] = list(geom['coordinates'][0])

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return insides

for name, coord in enumerate(geoms_nyc):
    
