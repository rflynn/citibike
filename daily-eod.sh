#!/bin/bash

PATH=$PATH:/usr/local/bin
(cd script/ && /bin/bash clear_citibike_inventory_raw.sh)
(cd script/ && /bin/bash pgdump.sh)
