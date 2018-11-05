'''
load and play with shapefile
'''

from pprint import pprint

import fiona


def dump(shape):
    #print('len(nyc)', len(nyc))
    for s in shape:
        print(s['id'], s['type'], s['properties'])
        # print(s['geometry']['coordinates'])
        # print(s['geometry']['coordinates'][0])


if __name__ == '__main__':
    import sys
    # shppath='ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp'
    shppath = sys.argv[1]
    shape = fiona.open(shppath)
    # nyc = [s for s in shape if s['properties']['City'] == 'New York' and s['properties']['Name'] == 'Midtown']
    dump(shape)
