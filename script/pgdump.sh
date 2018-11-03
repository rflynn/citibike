#!/bin/bash

set -x

# delete old backups
find . -type d -name 'pgdump-*' -ctime +0 | xargs rm -rf

declare -r destdir=pgdump-$(date +%Y-%m-%d-%H-%M-%S)
time PGPASSWORD=password pg_dump --verbose -h localhost -U postgres -d citibike -Fd -j 2 -f $destdir
