#!/bin/bash

set -xe

test -n "$1" || { echo "Usage: $0 <pgdump-dir>"; exit 1; }
test -d "$1" || { echo "$1 does not exist..."; exit 1; }

time PGPASSWORD=password pg_restore --verbose -h localhost -U postgres -d citibike -j 2 -Fd "$1"

