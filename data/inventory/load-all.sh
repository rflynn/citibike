#!/bin/bash

set -x

for f in $(find data/raw -type f | sort)
do
    echo $f
    ../../venv/bin/python load.py "$f"
done

PGPASSWORD=password psql -h localhost -U postgres -d citibike -f raw-to-updates.sql
PGPASSWORD=password psql -h localhost -U postgres -d citibike -f updates-to-station-status.sql
PGPASSWORD=password psql -h localhost -U postgres -d citibike -f updates-to-station-inventory.sql
