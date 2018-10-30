#!/bin/bash

declare -r url='https://layer.bicyclesharing.net/map/v1/nyc/map-inventory'

declare -r ua='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
#declare -r ua='Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
declare -r referer=''

declare -r ts=$(date +%Y-%m-%d-%H-%M-%S)
declare -r yyyy=${ts:0:4}
declare -r mm=${ts:5:2}
declare -r dd=${ts:8:2}

declare -r destdir=./data/raw/$yyyy/$mm/$dd
mkdir -p $destdir

declare -r destfile=$destdir/$ts-nyc-map-inventory.json
echo "url=$url destfile=$destfile"

mkdir -p ./data/tmp/
declare -r tmpfile=$(mktemp "./data/tmp/${ts}-XXXX")
if curl --retry 3 -L --max-time 20 --max-filesize 10000000 --user-agent "$ua"  -H 'Accept-Language: en-us' -H 'Accept-Encoding: gzip' --referer "$referer" -o $tmpfile "$url"
then
    stat -f%z $tmpfile
    if od -x -N 2 $tmpfile | grep 8b1f; then
        # already gzip'd
        mv $tmpfile $destfile.gz
    else
        gzip $tmpfile
        mv $tmpfile.gz $destfile.gz
        stat -f%z $destfile.gz
    fi
else
    exit 1
fi
