#!/bin/bash

PATH=$PATH:/usr/local/bin

(cd data/inventory/ && /bin/bash hourly.sh)
