#!/bin/bash

set -xe

echo check docker installed...
docker --version

echo ensure postgres:10.5 exists or pull it...
docker inspect postgres:10.5 >/dev/null || docker pull postgres:10.5

echo ensure pgdata volume
docker inspect pgdata >/dev/null || docker create volume pgdata

echo ensure psql client installed...
psql --version

echo ok
