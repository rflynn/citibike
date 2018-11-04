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

nyc = [s for s in shape if s['properties']['City'] == 'New York' and s['properties']['Name'] == 'Midtown']
#print('len(nyc)', len(nyc))

for s in nyc:
    print(s['id'], s['type'], s['properties'])
    print(s['geometry']['coordinates'])
    print(s['geometry']['coordinates'][0])
