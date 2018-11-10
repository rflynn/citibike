#!/bin/bash

# rsync entire tree w/ external storage

rsync -avzt --delete --size-only --exclude='.DS_Store' ~/src/citibike/ /Volumes/BLACK4A/src/citibike/
