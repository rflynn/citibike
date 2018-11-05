#!/bin/bash

(cd data/script/ && /bin/bash clear_citibike_inventory_raw.sh)
(cd data/script/ && /bin/bash pgdump.sh)
