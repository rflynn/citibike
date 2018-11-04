'''
load and play with shapefile
'''
# ref: https://gis.stackexchange.com/questions/113799/how-to-read-a-shapefile-in-python
import fiona
shppath='ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp'
shape = fiona.open(shppath)
#print(shape.schema)
# {'geometry': 'LineString', 'properties': OrderedDict([(u'FID', 'float:11')])}
#first feature of the shapefile
# first = shape.next()  # XXX: deprecated
# first = next(iter(shape))
# print(first) # (GeoJSON format)
# {'geometry': {'type': 'LineString', 'coordinates': [(0.0, 0.0), (25.0, 10.0), (50.0, 50.0)]}, 'type': 'Feature', 'id': '0', 'properties': OrderedDict([(u'FID', 0.0)])}

from pprint import pprint

nyc = [s for s in shape if s['properties']['City'] == 'New York']
#print('len(nyc)', len(nyc))

import csv
with open('nyc_neighborhoods.csv', 'w') as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(['state', 'county', 'city', 'name', 'regionid', 'shape'])
    for s in nyc:
        # print(i, s)
        # print(s['id'], s['type'], s['properties'])
        # print(tuple(s['geometry']['coordinates'][0]))
        p = s['properties']
        g = s['geometry']
        c = tuple(g['coordinates'][0])
        if isinstance(c[0], list):
            # pprint(g)
            c = tuple(c[0])
        w.writerow([p['State'], p['County'], p['City'], p['Name'], p['RegionID'], str(c)[1:-1]])
