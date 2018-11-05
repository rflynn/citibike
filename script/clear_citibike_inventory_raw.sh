#!/bin/bash

PGPASSWORD=password psql -h localhost -U postgres -d citibike -c 'delete from citibike_inventory_raw;'
PGPASSWORD=password psql -h localhost -U postgres -d citibike -c 'vacuum full citibike_inventory_raw;'
