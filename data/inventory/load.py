'''
load search results from data/raw/ into db
'''

"""
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -73.97371465,
          40.7643971
        ]
      },
      "properties": {
        "bike_angels": {
          "score": 1
        },
        "station": {
          "id": "281",
          "name": "Grand Army Plaza & Central Park S",
          "terminal": "6839.10",
          "installed": true,
          "last_reported": 1540911115,
          "accepts_dockable_bikes": true,
          "accepts_lockable_bikes": false,
          "capacity": 57,
          "bikes_available": 24,
          "docks_available": 30,
          "bikes_disabled": 1,
          "docks_disabled": 2,
          "renting": true,
          "returning": true,
          "valet_status": "available",
          "valet_summary": "Valet Service",
          "valet_description": "Citi Bike Valet station attendant service available ",
          "valet_schedule": "",
          "valet_link": "https://www.citibikenyc.com/valet",
          "sponsor": {
            "name": "New York Road Runners",
            "image": "https://s3.amazonaws.com/mot-static-feeds-prod/nyc/a_1539272509836_638695.png",
            "link": "https://dggt.app.link/hzCe0UdZKG"
          }
        },
        "bikes": [],
        "icon_pin_bike_layer": "pin-valet",
        "icon_pin_dock_layer": "pin-valet",
        "icon_dot_bike_layer": "pin-valet",
        "icon_dot_dock_layer": "pin-valet",
        "keys_available": true,
        "bike_angels_action": "give",
        "bike_angels_points": 1,
        "bike_angels_digits": 1
      }
    },
"""

import datetime
import gzip
import json
import os
from pprint import pprint

import psycopg2
from psycopg2.extras import Json


def do_file(infilepath, cursor, conn):

    inpath = os.path.dirname(infilepath)
    infilename = os.path.basename(infilepath)
    outpath = inpath.replace('data/raw', 'data/loaded')
    outfilepath = os.path.join(outpath, infilename)

    ts = datetime.datetime.strptime(infilename[0:19], '%Y-%m-%d-%H-%M-%S')
    print('ts', ts)

    os.makedirs(outpath, exist_ok=True)

    c.execute('''
insert into citibike_inventory_log (ts) values (%s)
''', (ts,))

    with gzip.open(infilepath) as f:
        js = json.load(f)
    if 'error' in js:
        print('error', js)
        return
    features = js['features']
    if features:
        for feat in features:
            # pprint(feat)
            geo = feat['geometry']
            prop = feat['properties']
            st = prop.get('station') or {}
            f = dict(station_id=st.get('id'),
                     terminal=st.get('terminal'),
                     name=st.get('name'),
                     coord_long=geo['coordinates'][0],
                     coord_lat=geo['coordinates'][1],
                     installed=st.get('installed'),
                     accepts_dockable_bikes=st.get('accepts_dockable_bikes'),
                     accepts_lockable_bikes=st.get('accepts_lockable_bikes'),
                     capacity=st.get('capacity'),
                     renting=st.get('renting'),
                     returning_=st.get('returning'),
                     valet_status=st.get('valet_status'),
                     docks_disabled=st.get('docks_disabled'),
                     bikes_available=st.get('bikes_available'),
                     docks_available=st.get('docks_available'),
                     bikes_disabled=st.get('bikes_disabled'),
                     bikes=prop.get('bikes'),
                     last_reported=st.get('last_reported'),
                     ts=ts)
            if f['bikes']:
                f['bikes'] = Json(f['bikes'])
            cursor.execute('''
insert into citibike_inventory_raw (
    station_id, terminal, name, coord_long, coord_lat,
    installed, accepts_dockable_bikes, accepts_lockable_bikes,
    capacity, renting, returning_, valet_status, docks_disabled,
    bikes_available, docks_available, bikes_disabled, bikes,
    last_reported, ts
) values (
    %(station_id)s, %(terminal)s, %(name)s, %(coord_long)s, %(coord_lat)s,
    %(installed)s, %(accepts_dockable_bikes)s, %(accepts_lockable_bikes)s,
    %(capacity)s, %(renting)s, %(returning_)s, %(valet_status)s, %(docks_disabled)s,
    %(bikes_available)s, %(docks_available)s, %(bikes_disabled)s, %(bikes)s,
    %(last_reported)s, %(ts)s
)''', f)
    return outfilepath


if __name__ == '__main__':

    import sys

    dbargs = dict(host=os.getenv('PGHOST') or 'localhost',
                  port=os.getenv('PGPORT') or 5432,
                  dbname=os.getenv('PGDATABASE') or 'citibike',
                  user=os.getenv('PGUSER') or 'postgres',
                  password=os.getenv('PGPASSWORD') or 'password')
    connstr = ' '.join('{}={}'.format(k, v) for k, v in dbargs.items())
    conn = psycopg2.connect(connstr)
    c = conn.cursor()

    moves = []
    for infilepath in sys.argv[1:]:
        print('{}'.format(infilepath))
        sys.stdout.flush()
        outfilepath = do_file(infilepath, c, conn)
        moves.append((infilepath, outfilepath))

    # raise NotImplementedError

    for infilepath, outfilepath in moves:
        os.rename(infilepath, outfilepath)

    conn.commit()

    c.close()
    conn.close()
