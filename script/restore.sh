#!/bin/bash

set -x

time PGPASSWORD=password pg_restore --verbose -h localhost -U postgres -d citibike -j 2 -Fd "$1"

